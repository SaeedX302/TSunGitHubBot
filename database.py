"""
Database service for TSunGitHubBot using Google Firestore
Handles user data persistence and quote subscriptions
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None
    firestore = None

from config import FIREBASE_CREDENTIALS

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db = None
        self.collection_name = "users_quotes_subscription"
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Initialize Firestore connection"""
        try:
            if not firebase_admin or not FIREBASE_CREDENTIALS:
                logger.warning("Firebase credentials not found, using fallback storage")
                self.db = None
                return
            
            # Parse credentials from environment variable
            if isinstance(FIREBASE_CREDENTIALS, str):
                cred_dict = json.loads(FIREBASE_CREDENTIALS)
            else:
                cred_dict = FIREBASE_CREDENTIALS
            
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info("✅ Firestore initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            self.db = None
    
    async def add_user(self, user_id: int, chat_id: int, username: str) -> bool:
        """Add or update user in database"""
        try:
            if not self.db:
                logger.warning("Database not available, skipping user storage")
                return False
            
            user_data = {
                "user_id": user_id,
                "chat_id": chat_id,
                "username": username,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "quotes_enabled": True
            }
            
            # Use user_id as document ID
            doc_ref = self.db.collection(self.collection_name).document(str(user_id))
            doc_ref.set(user_data, merge=True)
            
            logger.info(f"User {user_id} added to database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add user to database: {e}")
            return False
    
    async def get_all_users(self) -> List[Dict]:
        """Get all users for quote broadcasting"""
        try:
            if not self.db:
                logger.warning("Database not available, returning empty user list")
                return []
            
            users = []
            docs = self.db.collection(self.collection_name).stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                if user_data.get("quotes_enabled", True):
                    users.append(user_data)
            
            logger.info(f"Retrieved {len(users)} users from database")
            return users
            
        except Exception as e:
            logger.error(f"Failed to get users from database: {e}")
            return []
    
    async def disable_quotes_for_user(self, user_id: int) -> bool:
        """Disable quotes for a specific user"""
        try:
            if not self.db:
                return False
            
            doc_ref = self.db.collection(self.collection_name).document(str(user_id))
            doc_ref.update({"quotes_enabled": False, "updated_at": datetime.now()})
            
            logger.info(f"Disabled quotes for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable quotes for user {user_id}: {e}")
            return False
    
    async def enable_quotes_for_user(self, user_id: int) -> bool:
        """Enable quotes for a specific user"""
        try:
            if not self.db:
                return False
            
            doc_ref = self.db.collection(self.collection_name).document(str(user_id))
            doc_ref.update({"quotes_enabled": True, "updated_at": datetime.now()})
            
            logger.info(f"Enabled quotes for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable quotes for user {user_id}: {e}")
            return False
    
    async def get_user_count(self) -> int:
        """Get total number of users"""
        try:
            if not self.db:
                return 0
            
            docs = self.db.collection(self.collection_name).stream()
            count = sum(1 for _ in docs)
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get user count: {e}")
            return 0
    
    async def update_user_activity(self, user_id: int) -> bool:
        """Update user's last activity timestamp"""
        try:
            if not self.db:
                return False
            
            doc_ref = self.db.collection(self.collection_name).document(str(user_id))
            doc_ref.update({"last_activity": datetime.now()})
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user activity for {user_id}: {e}")
            return False
    
    async def cleanup_inactive_users(self, days_threshold: int = 30) -> int:
        """Remove users who haven't been active for specified days"""
        try:
            if not self.db:
                return 0
            
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_threshold)
            
            docs = self.db.collection(self.collection_name).where(
                "last_activity", "<", cutoff_date
            ).stream()
            
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} inactive users")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup inactive users: {e}")
            return 0
