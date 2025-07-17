# TSunGitHubBot

A comprehensive Telegram bot that fetches, compresses, and delivers GitHub repositories with advanced quote integration and automated user interactions.

## Features

- 🚀 **Repository Cloning**: Clone and compress GitHub repositories
- 📱 **Telegram Integration**: Full Telegram bot with interactive commands
- 🔐 **Authentication**: Support for both public and private repositories via PAT
- 💬 **Quote System**: AI-powered quote delivery every 10 minutes
- 🌐 **Web Interface**: Beautiful web frontend with GitHub user info display
- 📊 **Database**: Firebase Firestore for user management
- 🎨 **Premium UI**: Glass morphism design with dark/light theme

## Tech Stack

- **Backend**: Python with Flask
- **Bot Framework**: python-telegram-bot
- **Database**: Google Firestore
- **Frontend**: HTML5, CSS3, JavaScript with Tailwind CSS
- **APIs**: GitHub API, Custom Quote API
- **Deployment**: Replit hosting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TSunGitHubBot.git
cd TSunGitHubBot
```

2. Install dependencies:
```bash
pip install python-telegram-bot[all] PyGithub GitPython firebase-admin flask requests APScheduler
```

3. Set up environment variables:
```bash
export BOT_TOKEN="your_telegram_bot_token"
export GITHUB_TOKEN="your_github_token"
export FIREBASE_CREDENTIALS="your_firebase_credentials_json"
```

4. Run the bot:
```bash
python main.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `GITHUB_TOKEN` | GitHub personal access token |
| `FIREBASE_CREDENTIALS` | Firebase service account JSON string |
| `FLASK_PORT` | Web server port (default: 5000) |

## File Structure

```
TSunGitHubBot/
├── main.py                 # Main application entry point
├── bot_handlers.py         # Telegram bot command handlers
├── github_service.py       # GitHub API integration
├── database.py            # Firestore database operations
├── scheduler.py           # Quote scheduling and profile updates
├── config.py             # Configuration management
├── utils.py              # Utility functions
├── web/
│   └── index.html        # Web interface
├── templates/
│   └── quotes.json       # Local quote storage
├── media/
│   └── anime/           # Profile pictures
└── replit.md            # Project documentation

```

## Usage

### Telegram Bot Commands

- `/start` - Initialize the bot
- `/help` - Show available commands
- `/about` - Bot information
- `/quotes` - Toggle quote notifications
- `/cancel` - Cancel current operation

### Web Interface

1. Visit the hosted website
2. Enter GitHub username or PAT token
3. Click "Get User Info" to view profile and repositories
4. Use the Telegram bot for repository cloning

## API Endpoints

- `GET /` - Web interface
- `GET /api/quote` - Get random quote
- `GET /api/user/<username>` - Get public GitHub user info
- `POST /api/user-with-token` - Get authenticated user info
- `POST /api/clone` - Repository cloning (demo)
- `GET /health` - Health check

## Features in Detail

### Quote System
- Fetches quotes from https://tsunquotes.vercel.app/quotes
- Broadcasts every 10 minutes to subscribed users
- Supports Roman Urdu and English mix
- Fallback to local quotes if API unavailable

### Repository Management
- Supports both public and private repositories
- GitHub PAT authentication for private access
- Repository compression and delivery
- Progress tracking and user notifications

### Web Interface
- Ultra-premium glass morphism design
- Dark/light theme toggle
- Real-time quote updates every 20 seconds
- Responsive design for all devices
- GitHub user profile display with statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, contact the bot administrator or create an issue in the GitHub repository.

---

Created with ❤️ by 〆༯𝙎คAEED✘🫀