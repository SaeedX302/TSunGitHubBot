# TSunGitHubBot

## Overview

TSunGitHubBot is a feature-rich Telegram bot designed to fetch GitHub repositories, compress them into zip files, and deliver them to users. The bot supports both public repository access via GitHub username and private repository access via Personal Access Token (PAT). It includes additional features like scheduled quote broadcasting and profile updates.

## User Preferences

Preferred communication style: Simple, everyday language.
Bot personality: Friendly, informal mix of Roman Urdu and English with extensive emoji usage.
Quote system: Send quotes every 10 minutes to all users who have started the bot once, using https://tsunquotes.vercel.app/quotes API.
Website design: Ultra-premium look with glass morphism, quotes in header updating every 20 seconds, dark/light theme toggle, improved visibility for light theme.
Website layout: Header with quotes, TSunGitHubBot title, GitHub Repository Manager section, GitHub Repository User Details, and feature boxes at the bottom.
User interaction: Single input field for username/PAT with smart detection, highlight box directing to @githubuserclonerbot for actual cloning.
External storage: Use DevUpload API for storing cloned repositories instead of local storage, provide download links to users, clean up local files after upload.

## System Architecture

### Core Architecture
- **Bot Framework**: Python-based Telegram bot using `python-telegram-bot` library
- **Web Server**: Flask integration for 24/7 hosting and health checks
- **Database**: Google Firestore for user data persistence and quote subscriptions
- **GitHub Integration**: PyGithub and GitPython for repository operations
- **Scheduler**: JobQueue-based scheduling system for automated tasks

### Key Components

#### 1. Bot Handler System (`bot_handlers.py`)
- Command handlers for user interactions (`/start`, `/help`, `/about`)
- Callback query handlers for inline keyboard interactions
- Message handlers for username and PAT input processing
- State management for user authentication flow

#### 2. GitHub Service (`github_service.py`)
- GitHub API client management
- Repository fetching (public and private)
- Git operations (clone, pull) using GitPython
- Repository compression and file delivery
- Progress tracking and user notifications

#### 3. Database Layer (`database.py`)
- Firestore client initialization and management
- User data persistence (ID, chat ID, username)
- Quote subscription management
- Fallback storage mechanism when Firestore is unavailable

#### 4. Scheduler Service (`scheduler.py`)
- Automated quote broadcasting to subscribed users
- Profile update scheduling
- Job queue management using Telegram's JobQueue
- External API integration for quote fetching

#### 5. Configuration Management (`config.py`)
- Environment variable handling
- Bot token and API key management
- Admin user configuration
- Message templates and constants

#### 6. Utility Functions (`utils.py`)
- PAT validation (GitHub Personal Access Token format)
- Filename sanitization for filesystem compatibility
- Admin notification formatting
- Random poetry selection from local JSON files

#### 7. DevUpload Service (`devupload_service.py`)
- External file storage integration with DevUpload API
- Automatic file upload after repository compression
- Download link generation for users
- Local file cleanup after successful upload
- Error handling for upload failures

## Data Flow

### User Authentication Flow
1. User starts bot with `/start` command
2. Bot presents authentication options (username or PAT)
3. User selects method and provides credentials
4. Bot validates input and notifies administrators
5. Authentication state is stored for repository processing

### Repository Processing Flow
1. Initialize GitHub client (authenticated or public)
2. Fetch user repositories based on authentication method
3. Create user-specific directory structure
4. Clone/pull repositories with progress updates
5. Compress repositories into timestamped zip file
6. Upload zip file to DevUpload service
7. Generate download link for user
8. Send download link to user via Telegram
9. Clean up temporary files and directories

### Scheduled Tasks Flow
1. JobQueue triggers scheduled functions
2. Fetch quotes from external API or local storage
3. Retrieve subscribed users from Firestore
4. Broadcast quotes to all subscribed users
5. Update bot profile information periodically

## External Dependencies

### Required Libraries
- `python-telegram-bot`: Telegram bot framework
- `PyGithub`: GitHub API client
- `GitPython`: Git operations
- `firebase-admin`: Firestore database client
- `Flask`: Web server for hosting
- `requests`: HTTP client for external APIs

### External Services
- **Telegram Bot API**: Core bot functionality
- **GitHub API**: Repository access and operations
- **Google Firestore**: User data persistence
- **External Quote API**: `https://tsunquotes.vercel.app/quotes`
- **DevUpload API**: External file storage and download links (`https://devuploads.com/api`)

### File System Dependencies
- `cloned_repos/`: Directory for temporary repository storage
- `media/`: Static assets including anime images
- `templates/`: Quote templates and static data
- `poetry.json`: Local poetry collection for fallback quotes

## Deployment Strategy

### Hosting Configuration
- Flask web server runs on configurable port (default: 5000)
- Health check endpoint at `/health`
- Background thread management for concurrent operations
- Environment variable configuration for sensitive data

### Environment Variables
- `BOT_TOKEN`: Telegram bot authentication token
- `GITHUB_TOKEN`: Bot's GitHub token for profile updates
- `FIREBASE_CREDENTIALS`: JSON string of Firebase service account
- `FLASK_PORT`: Web server port configuration

### Administrator Configuration
- Hardcoded admin IDs for notification system
- Admin notification system for user activity monitoring
- Markdown-formatted admin alerts with user details

### Error Handling and Logging
- Comprehensive logging throughout all modules
- Error recovery mechanisms for API failures
- Fallback storage when Firestore is unavailable
- User-friendly error messages and progress updates

### Security Considerations
- PAT validation to ensure proper GitHub token format
- Filename sanitization to prevent filesystem attacks
- Temporary file cleanup after processing
- Admin-only notification system for monitoring

The bot is designed to be resilient, scalable, and maintainable with clear separation of concerns across different service layers.