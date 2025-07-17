"""
DevUpload service for TSunGitHubBot
Handles file uploads to DevUpload and provides download links
"""

import os
import requests
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class DevUploadService:
    def __init__(self):
        self.api_key = "6308159g1fkik7yhiud5e"
        self.base_url = "https://devuploads.com/api"
        self.upload_url = f"{self.base_url}/upload"
        self.account_info_url = f"{self.base_url}/account/info"
        
    async def check_account_info(self) -> Dict[str, Any]:
        """Check DevUpload account information"""
        try:
            response = requests.get(f"{self.account_info_url}?key={self.api_key}")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ DevUpload account info: {data}")
                return data
            else:
                logger.error(f"❌ Failed to get account info: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error checking account info: {e}")
            return {}
    
    async def upload_file(self, file_path: str, filename: str = None) -> Optional[str]:
        """
        Upload file to DevUpload and return download link
        
        Args:
            file_path: Path to the file to upload
            filename: Optional custom filename
            
        Returns:
            Download link if successful, None otherwise
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"❌ File does not exist: {file_path}")
                return None
            
            if not filename:
                filename = file_path.name
                
            # Get file size
            file_size = file_path.stat().st_size
            logger.info(f"📁 Uploading file: {filename} ({file_size} bytes)")
            
            # Prepare upload data
            files = {
                'file': (filename, open(file_path, 'rb'), 'application/octet-stream')
            }
            
            data = {
                'key': self.api_key,
                'action': 'upload'
            }
            
            # Upload file
            response = requests.post(self.upload_url, files=files, data=data, timeout=300)
            
            # Close file handle
            files['file'][1].close()
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    download_link = result.get('data', {}).get('file', {}).get('url', {}).get('full')
                    logger.info(f"✅ File uploaded successfully: {download_link}")
                    return download_link
                else:
                    logger.error(f"❌ Upload failed: {result}")
                    return None
            else:
                logger.error(f"❌ Upload request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error uploading file: {e}")
            return None
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    async def get_upload_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information before upload"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {}
            
            file_size = file_path.stat().st_size
            return {
                'filename': file_path.name,
                'size': file_size,
                'size_formatted': self.format_file_size(file_size),
                'path': str(file_path)
            }
        except Exception as e:
            logger.error(f"❌ Error getting file info: {e}")
            return {}
    
    async def cleanup_local_file(self, file_path: str) -> bool:
        """Delete local file after successful upload"""
        try:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                logger.info(f"🗑️ Local file deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error deleting local file: {e}")
            return False
    
    async def cleanup_directory(self, dir_path: str) -> bool:
        """Delete directory and all its contents"""
        try:
            import shutil
            dir_path = Path(dir_path)
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                logger.info(f"🗑️ Directory deleted: {dir_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error deleting directory: {e}")
            return False