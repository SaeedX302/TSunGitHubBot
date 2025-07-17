"""
GitHub service for TSunGitHubBot
Handles GitHub API interactions and repository operations
"""

import os
import json
import zipfile
import shutil
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
import logging

from github import Github, GithubException
from git import Repo, GitCommandError
from telegram import Bot

from config import CLONED_REPOS_DIR
from utils import sanitize_filename
from devupload_service import DevUploadService

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.github_client = None
        self.user_info = None
        self.devupload_service = DevUploadService()
    
    async def process_user_repos(self, user_id: int, username: str = None, pat: str = None, 
                               update_callback: Optional[Callable] = None) -> Optional[str]:
        """
        Process user repositories - fetch, clone, compress and upload to DevUpload
        Returns download link if successful, None otherwise
        """
        try:
            # Initialize GitHub client
            if pat:
                self.github_client = Github(pat)
                github_user = self.github_client.get_user()
                username = github_user.login
            else:
                self.github_client = Github()
                github_user = self.github_client.get_user(username)
            
            # Create user directory
            user_dir = Path(CLONED_REPOS_DIR) / str(user_id) / username
            user_dir.mkdir(parents=True, exist_ok=True)
            
            # Save user info if using username method
            if not pat:
                await self._save_user_info(github_user, user_dir)
            
            # Get repositories
            if update_callback:
                await update_callback("🔍 *Repositories fetch kar raha hun...* 📋")
            
            repos = list(github_user.get_repos())
            total_repos = len(repos)
            
            if total_repos == 0:
                if update_callback:
                    await update_callback("❌ *Koi repository nahi mili!* 😔")
                return None
            
            # Clone repositories
            repos_dir = user_dir / "repos"
            repos_dir.mkdir(exist_ok=True)
            
            successful_clones = 0
            
            for i, repo in enumerate(repos, 1):
                try:
                    progress_percentage = (i / total_repos) * 100
                    progress_msg = (
                        f"🔄 *Repo {i} of {total_repos}:* `{repo.name}`\n"
                        f"📊 *Progress:* {progress_percentage:.2f}% 🚀"
                    )
                    
                    if update_callback:
                        await update_callback(progress_msg)
                    
                    # Clone or update repository
                    await self._clone_or_update_repo(repo, repos_dir, pat)
                    successful_clones += 1
                    
                except Exception as e:
                    logger.error(f"Failed to clone repo {repo.name}: {e}")
                    continue
            
            if successful_clones == 0:
                if update_callback:
                    await update_callback("❌ *Koi repository clone nahi ho saki!* 😰")
                return None
            
            # Compress repositories
            if update_callback:
                await update_callback("📦 *Repositories compress kar raha hun...* 🗜️")
            
            zip_path = await self._compress_repos(user_dir, username)
            
            if not zip_path:
                if update_callback:
                    await update_callback("❌ *Compression failed!* 😔")
                return None
            
            # Upload to DevUpload
            if update_callback:
                await update_callback("☁️ *DevUpload par upload kar raha hun...* 📤")
            
            download_link = await self.devupload_service.upload_file(zip_path, f"{username}_repos.zip")
            
            if not download_link:
                if update_callback:
                    await update_callback("❌ *DevUpload upload failed!* 😔")
                return None
            
            # Send download link
            if update_callback:
                await update_callback(
                    f"✅ *{successful_clones} repositories successfully processed!* 🎉\n"
                    f"📁 *Download your repos:* [Click here]({download_link}) 📦\n"
                    f"🌐 *Link:* `{download_link}`"
                )
            
            return download_link
            
        except GithubException as e:
            logger.error(f"GitHub API error: {e}")
            if update_callback:
                if e.status == 404:
                    await update_callback("❌ *User not found!* 🤷‍♂️\nUsername check karein.")
                else:
                    await update_callback("❌ *GitHub API error!* 🚫\nToken ya username check karein.")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error in process_user_repos: {e}")
            if update_callback:
                await update_callback("❌ *Unexpected error occurred!* 😰")
            return None
        
        finally:
            # Cleanup - Remove local files after successful upload
            try:
                if os.path.exists(user_dir):
                    await self.devupload_service.cleanup_directory(str(user_dir))
                    logger.info(f"🗑️ Cleaned up user directory: {user_dir}")
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
    
    async def _save_user_info(self, github_user, user_dir: Path):
        """Save GitHub user information to JSON file"""
        try:
            user_info = {
                "login": github_user.login,
                "name": github_user.name,
                "bio": github_user.bio,
                "location": github_user.location,
                "email": github_user.email,
                "followers": github_user.followers,
                "following": github_user.following,
                "public_repos": github_user.public_repos,
                "company": github_user.company,
                "blog": github_user.blog,
                "created_at": github_user.created_at.isoformat() if github_user.created_at else None,
                "updated_at": github_user.updated_at.isoformat() if github_user.updated_at else None,
                "avatar_url": github_user.avatar_url,
                "html_url": github_user.html_url
            }
            
            with open(user_dir / "userinfo.json", "w", encoding="utf-8") as f:
                json.dump(user_info, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save user info: {e}")
    
    async def _clone_or_update_repo(self, repo, repos_dir: Path, pat: str = None):
        """Clone or update a single repository"""
        repo_name = sanitize_filename(repo.name)
        repo_path = repos_dir / repo_name
        
        # Prepare clone URL
        if pat:
            clone_url = f"https://{pat}@github.com/{repo.full_name}.git"
        else:
            clone_url = repo.clone_url
        
        try:
            if repo_path.exists():
                # Repository exists, try to pull
                try:
                    local_repo = Repo(repo_path)
                    origin = local_repo.remotes.origin
                    origin.pull()
                    logger.info(f"Updated repository: {repo.name}")
                except Exception as e:
                    logger.warning(f"Failed to update {repo.name}, re-cloning: {e}")
                    shutil.rmtree(repo_path)
                    await self._clone_repository(clone_url, repo_path)
            else:
                # Clone new repository
                await self._clone_repository(clone_url, repo_path)
                
        except Exception as e:
            logger.error(f"Failed to clone/update repository {repo.name}: {e}")
            raise
    
    async def _clone_repository(self, clone_url: str, repo_path: Path):
        """Clone a repository"""
        try:
            # Run git clone in a thread to avoid blocking
            def clone_repo():
                Repo.clone_from(clone_url, repo_path)
            
            await asyncio.get_event_loop().run_in_executor(None, clone_repo)
            logger.info(f"Cloned repository to: {repo_path}")
            
        except GitCommandError as e:
            logger.error(f"Git clone error: {e}")
            raise
    
    async def _compress_repos(self, user_dir: Path, username: str) -> Optional[str]:
        """Compress user repositories into a zip file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            zip_filename = f"{username}_repos_{timestamp}.zip"
            zip_path = user_dir.parent / zip_filename
            
            def create_zip():
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(user_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(user_dir.parent)
                            zipf.write(file_path, arcname)
            
            await asyncio.get_event_loop().run_in_executor(None, create_zip)
            
            # Verify zip file was created
            if zip_path.exists() and zip_path.stat().st_size > 0:
                logger.info(f"Created zip file: {zip_path}")
                return str(zip_path)
            else:
                logger.error("Zip file creation failed or file is empty")
                return None
                
        except Exception as e:
            logger.error(f"Compression error: {e}")
            return None
    
    async def send_zip_file(self, bot: Bot, chat_id: int, zip_path: str):
        """Send zip file to user"""
        try:
            with open(zip_path, 'rb') as f:
                await bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename=os.path.basename(zip_path),
                    caption="🎉 *Aapki repositories ready hain!* 📦\n\n"
                           "*Made With 🫀 By 〆༯𝙎คAEED✘🫀*",
                    parse_mode="Markdown"
                )
            
            # Clean up zip file
            os.remove(zip_path)
            logger.info(f"Sent and cleaned up zip file: {zip_path}")
            
        except Exception as e:
            logger.error(f"Failed to send zip file: {e}")
            raise
