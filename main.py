"""
TSunGitHubBot - A feature-rich Telegram bot for GitHub repository management
Main entry point with Flask web server integration for 24/7 hosting
"""

import os
import threading
import logging
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot_handlers import (
    start_handler, help_handler, about_handler, quotes_handler, cancel_handler,
    button_handler, github_input_handler, handle_username_input, handle_pat_input
)
from scheduler import setup_scheduler
from config import BOT_TOKEN, FLASK_PORT

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for 24/7 hosting
app = Flask(__name__, static_folder='web', template_folder='web')

@app.route('/')
def home():
    return send_from_directory('web', 'index.html')

@app.route('/api/user/<username>')
def get_user_info(username):
    """API endpoint for getting GitHub user information"""
    try:
        import requests
        
        # Get user info from GitHub API
        user_url = f'https://api.github.com/users/{username}'
        user_response = requests.get(user_url)
        
        if user_response.status_code == 404:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = user_response.json()
        
        # Get repositories
        repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
        repos_response = requests.get(repos_url)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        return jsonify({
            'user': user_data,
            'repositories': repos_data,
            'repo_count': len(repos_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-with-token', methods=['POST'])
def get_user_info_with_token():
    """API endpoint for getting user info with PAT token"""
    try:
        data = request.json
        pat = data.get('pat')
        
        if not pat:
            return jsonify({'error': 'PAT token is required'}), 400
        
        headers = {'Authorization': f'token {pat}'}
        
        # Get authenticated user info
        user_url = 'https://api.github.com/user'
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code == 401:
            return jsonify({'error': 'Invalid token'}), 401
        
        user_data = user_response.json()
        
        # Get repositories (including private ones)
        repos_url = 'https://api.github.com/user/repos?per_page=100&type=all'
        repos_response = requests.get(repos_url, headers=headers)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        return jsonify({
            'user': user_data,
            'repositories': repos_data,
            'repo_count': len(repos_data),
            'private_repos': len([r for r in repos_data if r.get('private', False)])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clone', methods=['POST'])
def clone_repository():
    """API endpoint for cloning repositories"""
    try:
        data = request.json
        username = data.get('username')
        pat = data.get('pat', '')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Here you would integrate with your GitHub service
        # For demonstration, we'll simulate the process
        return jsonify({
            'success': True,
            'message': f'Repository cloning initiated for {username}',
            'filename': f'{username}_repos_{datetime.now().strftime("%Y%m%d-%H%M%S")}.zip',
            'note': 'Use the Telegram bot for actual repository processing and download'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quote')
def get_quote():
    """API endpoint for fetching quotes"""
    try:
        response = requests.get('https://tsunquotes.vercel.app/quotes')
        return response.json()
    except Exception as e:
        return jsonify({
            'quote': 'خود کو اتنا بھی مت بچایا کر بارشیں ہوں تو بھیگ جایا کر',
            'author': 'بشیر بدر'
        })

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "TSunGitHubBot"}, 200

def run_flask():
    """Run Flask server in a separate thread"""
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)

def main():
    """Main function to start the bot and Flask server"""
    try:
        # Start Flask server in background thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info(f"🌐 Flask server started on port {FLASK_PORT}")
        
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_handler))
        application.add_handler(CommandHandler("help", help_handler))
        application.add_handler(CommandHandler("about", about_handler))
        application.add_handler(CommandHandler("quotes", quotes_handler))
        application.add_handler(CommandHandler("cancel", cancel_handler))
        
        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Add message handlers for different input states
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            github_input_handler
        ))
        
        # Setup scheduler for quotes and profile updates
        setup_scheduler(application)
        
        logger.info("🚀 TSunGitHubBot started successfully!")
        logger.info("🎯 Bot is ready to handle GitHub repository requests")
        
        # Run the bot
        application.run_polling(allowed_updates=['message', 'callback_query'])
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
