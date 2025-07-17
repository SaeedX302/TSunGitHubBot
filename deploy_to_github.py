#!/usr/bin/env python3
"""
GitHub Deployment Helper Script for TSunGitHubBot
This script helps you deploy your bot to GitHub repository
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            print(f"Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_git_installed():
    """Check if git is installed"""
    return run_command("git --version", "Checking Git installation")

def initialize_git():
    """Initialize git repository"""
    if not os.path.exists('.git'):
        return run_command("git init", "Initializing Git repository")
    print("✅ Git repository already initialized")
    return True

def add_files():
    """Add all files to git"""
    return run_command("git add .", "Adding all files to Git")

def commit_files():
    """Commit files"""
    commit_message = "Initial commit: TSunGitHubBot with web interface and quote system"
    return run_command(f'git commit -m "{commit_message}"', "Committing files")

def add_remote(repo_url):
    """Add remote repository"""
    return run_command(f"git remote add origin {repo_url}", "Adding remote repository")

def push_to_github():
    """Push to GitHub"""
    return run_command("git push -u origin main", "Pushing to GitHub")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = """python-telegram-bot[all]==20.7
PyGithub==1.59.1
GitPython==3.1.40
firebase-admin==6.2.0
flask==3.0.0
requests==2.31.0
APScheduler==3.10.4"""
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        print("✅ requirements.txt created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 TSunGitHubBot GitHub Deployment Helper")
    print("=" * 50)
    
    # Get repository URL from user
    repo_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/TSunGitHubBot.git): ")
    if not repo_url.strip():
        print("❌ Repository URL is required")
        sys.exit(1)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first.")
        sys.exit(1)
    
    # Create requirements.txt
    if not create_requirements_file():
        print("❌ Failed to create requirements.txt")
        sys.exit(1)
    
    # Initialize git
    if not initialize_git():
        print("❌ Failed to initialize Git repository")
        sys.exit(1)
    
    # Add files
    if not add_files():
        print("❌ Failed to add files to Git")
        sys.exit(1)
    
    # Commit files
    if not commit_files():
        print("❌ Failed to commit files")
        sys.exit(1)
    
    # Add remote
    if not add_remote(repo_url):
        print("❌ Failed to add remote repository")
        print("💡 Note: This might fail if remote already exists")
    
    # Push to GitHub
    if not push_to_github():
        print("❌ Failed to push to GitHub")
        print("💡 Make sure you have push access to the repository")
        sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("📋 Next steps:")
    print("1. Go to your GitHub repository and verify all files are there")
    print("2. Set up environment variables (BOT_TOKEN, GITHUB_TOKEN, FIREBASE_CREDENTIALS)")
    print("3. Deploy to your hosting platform (Replit, Heroku, etc.)")
    print("4. Test the bot and web interface")
    print("\n📖 For detailed setup instructions, check DEPLOYMENT.md")

if __name__ == "__main__":
    main()