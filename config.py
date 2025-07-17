"""
Configuration settings for TSunGitHubBot
Contains all environment variables and constants
"""

import os

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))

# Admin Configuration
ADMIN_IDS = [5734967213, 5647704073]

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Bot's own GitHub token for profile updates

# Firestore Configuration
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS', '')  # JSON string of service account

# API Endpoints
QUOTES_API = "https://tsunquotes.vercel.app/quotes"

# File Paths
CLONED_REPOS_DIR = "cloned_repos"
MEDIA_DIR = "media"
ANIME_IMAGES_FILE = "media/anime/random.json"

# Job Schedule Intervals (in seconds)
QUOTES_INTERVAL = 600  # 10 minutes
PROFILE_UPDATE_INTERVAL = 86400  # 24 hours

# Message Templates
WELCOME_MESSAGE = """
🎉 *Assalam-o-Alaikum!* Welcome to TSunGitHubBot! 🚀

Main aapka *GitHub repositories* ka helper hun! 📂✨

*Kya kar sakta hun main:*
• 👤 GitHub username se public repos fetch kar sakta hun
• 🔑 Personal Access Token se private repos bhi le sakta hun
• 📦 Sab repos ko zip file mein compress kar ke send kar deta hun
• 🎯 Real-time progress updates deta hun

*Kaise shuru karein?*
Neeche se choose karein:
"""

HELP_MESSAGE = """
📚 *TSunGitHubBot Help Guide* 🤖

*Available Commands:*
• `/start` - Bot ko start karein aur GitHub repos fetch karein
• `/help` - Ye help message
• `/about` - Bot ki information
• `/quotes` - Random motivational quote
• `/cancel` - Current operation cancel karein

*How it works:*
1️⃣ `/start` command use karein
2️⃣ GitHub username ya PAT choose karein
3️⃣ Credentials provide karein
4️⃣ Bot aapke repos clone karega
5️⃣ Zip file ban ke aapko mil jayegi! 📦

*Features:*
• 🔄 Real-time progress tracking
• 🎯 Public + Private repos support
• 📊 User info included
• 🧹 Automatic cleanup
• 🎨 Scheduled quotes har 10 minutes

*Made With 🫀 By 〆༯𝙎คAEED✘🫀*
"""

ABOUT_MESSAGE = """
🤖 *TSunGitHubBot* - Your GitHub Companion

*Bot Description:*
Main aapka personal GitHub assistant hun! 🚀
Aapki saari repositories ko easily download kar sakta hun,
compress kar ke neat zip file mein deliver kar deta hun.

*Features:*
• 📂 Public & Private repos support
• 🔄 Real-time progress updates
• 🎯 Scheduled motivational quotes
• 🤖 Auto profile updates
• 💾 Persistent user data

*Version:* 1.0.0
*Language:* Python 🐍
*Database:* Firestore 🔥
*Hosting:* Replit 24/7 ⚡

*Creator:*
Made With 🫀 By 〆༯𝙎คAEED✘🫀

*Poetry Corner:*
_"Zindagi mein kuch to log mohabbat kar hi lete hain"_
_"Hum ne to mohabbat GitHub se kar li hai"_ 💕

— Jaun Elia (inspired) ✨
"""

# User states for conversation handling
USER_STATES = {
    'WAITING_USERNAME': 'waiting_username',
    'WAITING_PAT': 'waiting_pat',
    'PROCESSING': 'processing'
}

# Error messages
ERROR_MESSAGES = {
    'invalid_pat': '❌ *Invalid Personal Access Token!* 😔\nPAT should start with `ghp_`\nKripya valid token daalein.',
    'user_not_found': '❌ *GitHub user not found!* 🤷‍♂️\nUsername check kar ke phir try karein.',
    'api_error': '❌ *GitHub API Error!* 🚫\nKuch technical issue hai, thoda wait kar ke try karein.',
    'clone_error': '❌ *Repository clone failed!* 😰\nKuch repos clone nahi ho sake.',
    'general_error': '❌ *Kuch gadbad ho gayi!* 😔\nPlease try again later.'
}

# Success messages
SUCCESS_MESSAGES = {
    'repos_sent': '🎉 *Success!* Aapki repositories ready hain! 📦\n\n_"Safar khatam, manzil mil gayi"_ ✨\n— Jaun Elia',
    'quote_sent': '💡 *Quote delivered!* Hope you liked it! 🌟'
}
