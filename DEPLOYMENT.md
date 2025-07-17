# GitHub Deployment Guide for TSunGitHubBot

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New" to create a new repository
3. Name it `TSunGitHubBot` (or any name you prefer)
4. Make it public or private (your choice)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Prepare Local Files

Before pushing to GitHub, make sure you have these files ready:

### Core Files (Already Created)
- `main.py` - Main application
- `bot_handlers.py` - Telegram bot handlers
- `github_service.py` - GitHub integration
- `database.py` - Database operations
- `scheduler.py` - Quote scheduling
- `config.py` - Configuration
- `utils.py` - Utility functions
- `web/index.html` - Web interface
- `templates/quotes.json` - Quote templates
- `media/anime/` - Profile pictures
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules
- `replit.md` - Project architecture

### Dependencies File
Create a `requirements.txt` file with:
```
python-telegram-bot[all]==20.7
PyGithub==1.59.1
GitPython==3.1.40
firebase-admin==6.2.0
flask==3.0.0
requests==2.31.0
APScheduler==3.10.4
```

## Step 3: Initialize Git and Push

Run these commands in your project directory:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: TSunGitHubBot with web interface and quote system"

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/TSunGitHubBot.git

# Push to GitHub
git push -u origin main
```

## Step 4: Set Up Environment Variables

### For Local Development
Create a `.env` file (already in .gitignore):
```
BOT_TOKEN=your_telegram_bot_token_here
GITHUB_TOKEN=your_github_personal_access_token
FIREBASE_CREDENTIALS=your_firebase_service_account_json_string
FLASK_PORT=5000
```

### For Replit Deployment
In Replit, go to Secrets tab and add:
- `BOT_TOKEN` - Your Telegram bot token
- `GITHUB_TOKEN` - Your GitHub PAT
- `FIREBASE_CREDENTIALS` - Firebase service account JSON

### For Other Platforms
Add environment variables in your hosting platform's dashboard.

## Step 5: Test the Deployment

1. Clone your repository:
```bash
git clone https://github.com/yourusername/TSunGitHubBot.git
cd TSunGitHubBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables and run:
```bash
python main.py
```

## Step 6: Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing
3. Enable Firestore Database
4. Create a service account:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file
5. Copy the JSON content to `FIREBASE_CREDENTIALS` environment variable

## Step 7: Create Telegram Bot

1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the bot token to `BOT_TOKEN` environment variable
5. Set bot commands with @BotFather:
```
start - Initialize the bot
help - Show available commands
about - Bot information
quotes - Toggle quote notifications
cancel - Cancel current operation
```

## Step 8: GitHub Token Setup

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `user`, `read:user`
4. Copy token to `GITHUB_TOKEN` environment variable

## File Structure After Deployment

```
TSunGitHubBot/
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── requirements.txt
├── main.py
├── bot_handlers.py
├── github_service.py
├── database.py
├── scheduler.py
├── config.py
├── utils.py
├── replit.md
├── web/
│   └── index.html
├── templates/
│   └── quotes.json
└── media/
    └── anime/
        └── (profile pictures)
```

## Common Issues and Solutions

### 1. Import Errors
- Ensure all dependencies in `requirements.txt` are installed
- Check Python version compatibility (3.8+ recommended)

### 2. Environment Variables
- Double-check all environment variables are set correctly
- Firebase credentials should be valid JSON string

### 3. Port Issues
- Default port is 5000, change via `FLASK_PORT` if needed
- Ensure port is not blocked by firewall

### 4. Database Connection
- Verify Firebase project is active
- Check service account permissions
- Ensure Firestore is enabled

## Next Steps

1. Star the repository if you found it useful
2. Create issues for bugs or feature requests
3. Fork and contribute improvements
4. Share with the community

## Support

For help with deployment:
- Check the README.md for detailed usage
- Create an issue on GitHub
- Contact the bot administrator

Happy coding! 🚀