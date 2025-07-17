"""
Scheduler service for TSunGitHubBot
Handles scheduled quotes and profile updates using JobQueue
"""

import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
import requests

from telegram.ext import Application, ContextTypes
from telegram import Bot
from telegram.constants import ParseMode

from database import Database
from config import QUOTES_API, QUOTES_INTERVAL, PROFILE_UPDATE_INTERVAL, GITHUB_TOKEN, ANIME_IMAGES_FILE
from utils import get_random_poetry

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, application: Application):
        self.application = application
        self.db = Database()
        self.bot = application.bot
    
    async def send_quotes_job(self, context: ContextTypes.DEFAULT_TYPE):
        """Job to send quotes to all subscribed users"""
        try:
            logger.info("🎯 Starting scheduled quote broadcast")
            
            # Get all subscribed users
            users = await self.db.get_all_users()
            
            if not users:
                logger.warning("No users found for quote broadcast")
                return
            
            # Get random quote
            quote_data = await self.get_random_quote()
            if not quote_data:
                logger.error("Failed to fetch quote for broadcast")
                return
            
            # Send quotes to all users
            success_count = 0
            for user in users:
                try:
                    await self.send_quote_to_user(context.bot, user.get("chat_id"))
                    success_count += 1
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Failed to send quote to user {user.get('user_id')}: {e}")
                    continue
            
            logger.info(f"✅ Quote broadcast completed: {success_count}/{len(users)} users")
            
        except Exception as e:
            logger.error(f"Error in quotes job: {e}")
    
    async def update_profile_job(self, context: ContextTypes.DEFAULT_TYPE):
        """Job to update bot profile picture and bio"""
        try:
            logger.info("🤖 Starting profile update job")
            
            # Update profile picture
            await self.update_profile_picture(context.bot)
            
            # Update profile bio
            await self.update_profile_bio(context.bot)
            
            logger.info("✅ Profile update completed")
            
        except Exception as e:
            logger.error(f"Error in profile update job: {e}")
    
    async def get_random_quote(self) -> Dict[str, Any]:
        """Fetch random quote from API"""
        try:
            response = requests.get(QUOTES_API, timeout=10)
            response.raise_for_status()
            
            quote_data = response.json()
            logger.info(f"🔄 API Response: {quote_data}")
            
            return quote_data
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch quote from API: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing quote response: {e}")
            return None
    
    async def send_quote_to_user(self, bot: Bot, chat_id: int):
        """Send a random quote to a specific user"""
        try:
            quote_data = await self.get_random_quote()
            if not quote_data:
                # Fallback to local poetry
                poetry = get_random_poetry()
                quote_text = (
                    f"💡 *Daily Inspiration* ✨\n\n"
                    f"_\"{poetry['text']}\"_\n\n"
                    f"— {poetry['author']} 🌟\n\n"
                    f"*Made With 🫀 By 〆༯𝙎คAEED✘🫀*"
                )
            else:
                quote_text = (
                    f"💡 *Daily Inspiration* ✨\n\n"
                    f"_\"{quote_data.get('quote', 'Stay motivated!')}\"_\n\n"
                    f"— {quote_data.get('author', 'Unknown')} 🌟\n\n"
                    f"*Made With 🫀 By 〆༯𝙎คAEED✘🫀*"
                )
            
            await bot.send_message(
                chat_id=chat_id,
                text=quote_text,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Failed to send quote to chat {chat_id}: {e}")
            raise
    
    async def update_profile_picture(self, bot: Bot):
        """Update bot's profile picture from anime images"""
        try:
            # Load anime images
            with open(ANIME_IMAGES_FILE, 'r') as f:
                anime_data = json.load(f)
            
            import random
            random_image = random.choice(anime_data.get('images', []))
            image_url = random_image.get('url')
            
            if not image_url:
                logger.warning("No image URL found in anime data")
                return
            
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Set profile photo (disabled for now - requires special bot permissions)
            # await bot.set_chat_photo(chat_id=bot.id, photo=response.content)
            logger.info(f"Profile picture update skipped (requires special permissions)")
            logger.info(f"✅ Profile picture updated: {image_url}")
            
        except Exception as e:
            logger.error(f"Failed to update profile picture: {e}")
    
    async def update_profile_bio(self, bot: Bot):
        """Update bot's bio with a random quote"""
        try:
            quote_data = await self.get_random_quote()
            
            if quote_data:
                bio_text = f"🤖 TSunGitHubBot - {quote_data.get('quote', 'Your GitHub companion')} — {quote_data.get('author', 'Unknown')}"
            else:
                poetry = get_random_poetry()
                bio_text = f"🤖 TSunGitHubBot - {poetry['text']} — {poetry['author']}"
            
            # Telegram bio limit is 70 characters
            if len(bio_text) > 70:
                bio_text = bio_text[:67] + "..."
            
            await bot.set_my_description(description=bio_text)
            logger.info(f"✅ Profile bio updated: {bio_text}")
            
        except Exception as e:
            logger.error(f"Failed to update profile bio: {e}")

def setup_scheduler(application: Application):
    """Setup all scheduled jobs"""
    try:
        scheduler = SchedulerService(application)
        job_queue = application.job_queue
        
        # Schedule quote broadcasts every 10 minutes
        job_queue.run_repeating(
            scheduler.send_quotes_job,
            interval=QUOTES_INTERVAL,
            first=30  # Wait 30 seconds before first run
        )
        
        # Schedule profile updates every 24 hours
        job_queue.run_repeating(
            scheduler.update_profile_job,
            interval=PROFILE_UPDATE_INTERVAL,
            first=60  # Wait 1 minute before first run
        )
        
        logger.info("✅ Scheduler setup completed")
        logger.info(f"📅 Quotes interval: {QUOTES_INTERVAL}s")
        logger.info(f"📅 Profile update interval: {PROFILE_UPDATE_INTERVAL}s")
        
    except Exception as e:
        logger.error(f"Failed to setup scheduler: {e}")

# Export function for direct quote sending
async def send_quote_to_user(bot: Bot, chat_id: int):
    """Standalone function to send quote to user"""
    scheduler = SchedulerService(None)
    await scheduler.send_quote_to_user(bot, chat_id)
