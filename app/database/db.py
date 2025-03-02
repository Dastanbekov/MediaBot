import sqlite3
import aiosqlite
from datetime import datetime
from typing import List, Optional, Dict
from ..utils.logger import db_logger

class Database:
    def __init__(self, db_file: str = "app/database/bot.db"):
        self.db_file = db_file
        db_logger.info(f"Initializing database at {db_file}")
        self._init_db()

    def _init_db(self):
        """Initialize database with required tables"""
        try:
            db_logger.info("Creating database tables if they don't exist...")
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            # Create users table
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    total_downloads INTEGER DEFAULT 0,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            db_logger.debug("Users table created/verified")
            
            # Create broadcast messages history
            c.execute('''
                CREATE TABLE IF NOT EXISTS broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_text TEXT NOT NULL,
                    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sent_by INTEGER,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0
                )
            ''')
            db_logger.debug("Broadcasts table created/verified")
            
            # Create user analytics table (simplified)
            c.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action_type TEXT NOT NULL,
                    action_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            db_logger.debug("Analytics table created/verified")
            
            conn.commit()
            conn.close()
            db_logger.info("Database initialization completed successfully")
        except Exception as e:
            db_logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
            raise

    async def add_user(self, user_id: int, username: str = None, 
                      first_name: str = None, last_name: str = None) -> bool:
        """Add new user to database"""
        try:
            db_logger.info(f"Adding/updating user {user_id} ({username})")
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute(
                    """
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name, joined_date, is_active) 
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, TRUE)
                    """,
                    (user_id, username, first_name, last_name)
                )
                await db.commit()
                db_logger.debug(f"User {user_id} added/updated successfully")
                return True
        except Exception as e:
            db_logger.error(f"Error adding user {user_id}: {str(e)}", exc_info=True)
            return False

    async def get_user(self, user_id: int) -> Optional[dict]:
        """Get user information"""
        try:
            db_logger.debug(f"Fetching user info for {user_id}")
            async with aiosqlite.connect(self.db_file) as db:
                async with db.execute(
                    "SELECT * FROM users WHERE user_id = ?", (user_id,)
                ) as cursor:
                    user = await cursor.fetchone()
                    if user:
                        db_logger.debug(f"User {user_id} found")
                        return {
                            "user_id": user[0],
                            "username": user[1],
                            "first_name": user[2],
                            "last_name": user[3],
                            "joined_date": user[4],
                            "is_active": bool(user[5]),
                            "total_downloads": user[6],
                            "last_activity": user[7]
                        }
                    db_logger.debug(f"User {user_id} not found")
                    return None
        except Exception as e:
            db_logger.error(f"Error fetching user {user_id}: {str(e)}", exc_info=True)
            return None

    async def get_all_users(self) -> List[int]:
        """Get all active user IDs"""
        try:
            db_logger.debug("Fetching all active users")
            async with aiosqlite.connect(self.db_file) as db:
                async with db.execute(
                    "SELECT user_id FROM users WHERE is_active = TRUE"
                ) as cursor:
                    users = await cursor.fetchall()
                    user_ids = [user[0] for user in users]
                    db_logger.debug(f"Found {len(user_ids)} active users")
                    return user_ids
        except Exception as e:
            db_logger.error(f"Error fetching all users: {str(e)}", exc_info=True)
            return []

    async def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user (e.g., when they block the bot)"""
        try:
            db_logger.info(f"Deactivating user {user_id}")
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute(
                    "UPDATE users SET is_active = FALSE WHERE user_id = ?",
                    (user_id,)
                )
                await db.commit()
                db_logger.debug(f"User {user_id} deactivated successfully")
                return True
        except Exception as e:
            db_logger.error(f"Error deactivating user {user_id}: {str(e)}", exc_info=True)
            return False

    async def log_broadcast(self, message: str, sent_by: int, 
                          success_count: int, fail_count: int) -> bool:
        """Log broadcast message statistics"""
        try:
            db_logger.info(f"Logging broadcast message by user {sent_by}")
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute(
                    """
                    INSERT INTO broadcasts 
                    (message_text, sent_by, success_count, fail_count) 
                    VALUES (?, ?, ?, ?)
                    """,
                    (message, sent_by, success_count, fail_count)
                )
                await db.commit()
                db_logger.debug(f"Broadcast logged successfully. Success: {success_count}, Failed: {fail_count}")
                return True
        except Exception as e:
            db_logger.error(f"Error logging broadcast: {str(e)}", exc_info=True)
            return False

    async def log_action(self, user_id: int, action_type: str, 
                        action_data: str = None) -> bool:
        """Log user action for analytics"""
        try:
            db_logger.debug(f"Logging action '{action_type}' for user {user_id}")
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute(
                    """
                    INSERT INTO analytics 
                    (user_id, action_type, action_data) 
                    VALUES (?, ?, ?)
                    """,
                    (user_id, action_type, action_data)
                )
                if action_type == 'download':
                    await db.execute(
                        """
                        UPDATE users 
                        SET total_downloads = total_downloads + 1,
                            last_activity = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                        """,
                        (user_id,)
                    )
                await db.commit()
                db_logger.debug(f"Action logged successfully")
                return True
        except Exception as e:
            db_logger.error(f"Error logging action for user {user_id}: {str(e)}", exc_info=True)
            return False

    async def get_user_stats(self) -> dict:
        """Get enhanced user statistics"""
        try:
            db_logger.info("Fetching user statistics")
            async with aiosqlite.connect(self.db_file) as db:
                stats = {}
                
                # Basic user stats
                async with db.execute(
                    """
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) as active,
                        SUM(CASE WHEN is_active = FALSE THEN 1 ELSE 0 END) as inactive,
                        SUM(total_downloads) as total_downloads
                    FROM users
                    """
                ) as cursor:
                    basic_stats = await cursor.fetchone()
                    stats.update({
                        "total_users": basic_stats[0],
                        "active_users": basic_stats[1],
                        "inactive_users": basic_stats[2],
                        "total_downloads": basic_stats[3]
                    })
                
                # Active users in last 24 hours
                async with db.execute(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM analytics
                    WHERE timestamp > datetime('now', '-1 day')
                    """
                ) as cursor:
                    active_24h = await cursor.fetchone()
                    stats["active_24h"] = active_24h[0]
                
                db_logger.debug(f"Statistics fetched successfully: {stats}")
                return stats
        except Exception as e:
            db_logger.error(f"Error fetching user statistics: {str(e)}", exc_info=True)
            return {
                "total_users": 0,
                "active_users": 0,
                "inactive_users": 0,
                "total_downloads": 0,
                "active_24h": 0
            }

    async def get_user_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's download history"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                """
                SELECT 
                    url,
                    media_type,
                    file_size,
                    download_date,
                    status,
                    error_message
                FROM downloads
                WHERE user_id = ?
                ORDER BY download_date DESC
                LIMIT ?
                """,
                (user_id, limit)
            ) as cursor:
                history = await cursor.fetchall()
                return [
                    {
                        "url": row[0],
                        "media_type": row[1],
                        "file_size": row[2],
                        "download_date": row[3],
                        "status": row[4],
                        "error_message": row[5]
                    }
                    for row in history
                ] 