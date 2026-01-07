import sqlite3
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional, Union, Dict, Any

class Database:
    def __init__(self, path_to_db=None):
        """
        Database sinfi.
        """
        if path_to_db is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.path_to_db = os.path.join(base_dir, "main.db")
        else:
            self.path_to_db = path_to_db

    def get_connection(self) -> sqlite3.Connection:
        """
        Xavfsiz ulanish va Row factory.
        """
        try:
            conn = sqlite3.connect(self.path_to_db)
            conn.row_factory = sqlite3.Row # Dict-like access
            return conn
        except sqlite3.Error as e:
            logging.error(f"DB Connection Error: {e}")
            raise

    def create_tables(self):
        """Jadvallarni yaratish va yangilash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    language TEXT,
                    role TEXT,
                    created_at TIMESTAMP
                )
            """)

            # Anonymous Messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anonymous_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_telegram_id INTEGER,
                    sender_username TEXT,
                    message TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    is_replied BOOLEAN DEFAULT 0,
                    is_read BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP
                )
            """)
            # Migrations check
            self._check_migrations(cursor, "anonymous_messages", "message_type", "TEXT DEFAULT 'text'")
            self._check_migrations(cursor, "anonymous_messages", "file_id", "TEXT")
            self._check_migrations(cursor, "anonymous_messages", "is_replied", "BOOLEAN DEFAULT 0")
            self._check_migrations(cursor, "anonymous_messages", "is_read", "BOOLEAN DEFAULT 0")

            # Anonymous Replies
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anonymous_replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    receiver_telegram_id INTEGER,
                    reply_text TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    created_at TIMESTAMP
                )
            """)
            self._check_migrations(cursor, "anonymous_replies", "message_type", "TEXT DEFAULT 'text'")
            self._check_migrations(cursor, "anonymous_replies", "file_id", "TEXT")

            # Comments
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_telegram_id INTEGER,
                    sender_role TEXT,
                    sender_username TEXT,
                    comment TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    is_read BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP
                )
            """)
            self._check_migrations(cursor, "comments", "message_type", "TEXT DEFAULT 'text'")
            self._check_migrations(cursor, "comments", "file_id", "TEXT")
            self._check_migrations(cursor, "comments", "is_read", "BOOLEAN DEFAULT 0")

            # Broadcast Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS broadcast_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    target_group TEXT,
                    message_type TEXT,
                    file_id TEXT,
                    caption TEXT,
                    recipients_count INTEGER,
                    created_at TIMESTAMP
                )
            """)

            # Bot Settings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

    def _check_migrations(self, cursor, table, column, definition):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        except sqlite3.OperationalError:
            pass

    # --- USER METHODS ---
    def add_user(self, telegram_id: int, first_name: str, username: str, language: str, role: str = "user"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO users (telegram_id, first_name, username, language, role, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (telegram_id, first_name, username, language, role, datetime.now()))
                conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error adding user: {e}")

    def get_user(self, telegram_id: int) -> Optional[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            return cursor.fetchone()

    def update_user_language(self, telegram_id: int, language: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET language = ? WHERE telegram_id = ?", (language, telegram_id))
            conn.commit()

    def update_user_role(self, telegram_id: int, role: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = ? WHERE telegram_id = ?", (role, telegram_id))
            conn.commit()

    def get_user_by_username(self, username: str) -> Optional[sqlite3.Row]:
        clean_username = username.strip().replace("@", "")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (clean_username,))
            return cursor.fetchone()

    # --- ADMIN METHODS ---
    def get_admins(self) -> List[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE role IN ('admin', 'super_admin')")
            return cursor.fetchall()

    def get_all_user_ids(self) -> List[int]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT telegram_id FROM users")
            return [row["telegram_id"] for row in cursor.fetchall()]

    def get_admin_ids(self) -> List[int]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT telegram_id FROM users WHERE role IN ('admin', 'super_admin')")
            return [row["telegram_id"] for row in cursor.fetchall()]

    def downgrade_admin(self, username: str) -> bool:
        user = self.get_user_by_username(username)
        # user["role"] access allowed due to Row factory
        if user and user["role"] == 'admin':
            self.update_user_role(user["telegram_id"], 'user')
            return True
        return False

    def get_stats(self) -> dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
            users = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE role IN ('admin', 'super_admin')")
            admins = cursor.fetchone()[0]
            return {"total": total, "users": users, "admins": admins}

    # --- MESSAGES & COMMENTS ---
    def add_anonymous_message(self, telegram_id: int, username: str, message: str, msg_type: str = "text", file_id: str = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO anonymous_messages (sender_telegram_id, sender_username, message, message_type, file_id, is_replied, is_read, created_at)
                VALUES (?, ?, ?, ?, ?, 0, 0, ?)
            """, (telegram_id, username, message, msg_type, file_id, datetime.now()))
            conn.commit()
            return cursor.lastrowid



    def get_unreplied_anonymous_messages(self, limit: int = 10) -> List[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM anonymous_messages WHERE is_replied = 0 ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()

    def get_filtered_anonymous_messages(self, filter_type: str) -> List[sqlite3.Row]:
        """
        filter_type: 1_day_new, 1_week, 1_month
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            
            if filter_type == "1_day_new":
                date_limit = now - timedelta(days=1)
                # Faqat o'qilmaganlar
                cursor.execute("SELECT * FROM anonymous_messages WHERE created_at >= ? AND is_read = 0 ORDER BY id DESC", (date_limit,))
            elif filter_type == "1_week":
                date_limit = now - timedelta(weeks=1)
                cursor.execute("SELECT * FROM anonymous_messages WHERE created_at >= ? ORDER BY id DESC", (date_limit,))
            elif filter_type == "1_month":
                date_limit = now - timedelta(days=30)
                cursor.execute("SELECT * FROM anonymous_messages WHERE created_at >= ? ORDER BY id DESC", (date_limit,))
            else:
                cursor.execute("SELECT * FROM anonymous_messages ORDER BY id DESC LIMIT 20")
            
            return cursor.fetchall()

    def mark_anonymous_messages_read(self, ids: List[int]):
        if not ids: return
        with self.get_connection() as conn:
            cursor = conn.cursor()
            id_str = ",".join(map(str, ids))
            cursor.execute(f"UPDATE anonymous_messages SET is_read = 1 WHERE id IN ({id_str})")
            conn.commit()

    def delete_read_anonymous_messages(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM anonymous_messages WHERE is_read = 1")
            conn.commit()

    # Note: DB optimization - single commit for adding comment
    def add_comment(self, telegram_id: int, role: str, username: str, comment: str, msg_type: str = "text", file_id: str = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO comments (sender_telegram_id, sender_role, sender_username, comment, message_type, file_id, is_read, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?)
            """, (telegram_id, role, username, comment, msg_type, file_id, datetime.now()))
            conn.commit()

    def get_filtered_comments(self, filter_type: str) -> List[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            
            if filter_type == "1_day_new":
                date_limit = now - timedelta(days=1)
                cursor.execute("SELECT * FROM comments WHERE created_at >= ? AND is_read = 0 ORDER BY id DESC", (date_limit,))
            elif filter_type == "1_week":
                date_limit = now - timedelta(weeks=1)
                cursor.execute("SELECT * FROM comments WHERE created_at >= ? ORDER BY id DESC", (date_limit,))
            elif filter_type == "1_month":
                date_limit = now - timedelta(days=30)
                cursor.execute("SELECT * FROM comments WHERE created_at >= ? ORDER BY id DESC", (date_limit,))
            else:
                cursor.execute("SELECT * FROM comments ORDER BY id DESC LIMIT 20")
            
            return cursor.fetchall()

    def mark_comments_read(self, ids: List[int]):
        if not ids: return
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Xavfsiz usulda formatlash (faqat integerlar)
            id_str = ",".join(map(str, ids))
            cursor.execute(f"UPDATE comments SET is_read = 1 WHERE id IN ({id_str})")
            conn.commit()

    def delete_read_comments(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM comments WHERE is_read = 1")
            conn.commit()

    def add_reply_log(self, receiver_id: int, text: str, msg_type: str = "text", file_id: str = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO anonymous_replies (receiver_telegram_id, reply_text, message_type, file_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (receiver_id, text, msg_type, file_id, datetime.now()))
            # Update original message status logic would go here if we tracked message IDs specifically
            # For now just logging the reply
            conn.commit()

    def add_broadcast_log(self, sender_id: int, target: str, msg_type: str, file_id: str, caption: str, count: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO broadcast_logs (sender_id, target_group, message_type, file_id, caption, recipients_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sender_id, target, msg_type, file_id, caption, count, datetime.now()))
            conn.commit()

    # --- SETTINGS / MAINTENANCE ---
    def set_maintenance_mode(self, active: bool):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            val = "1" if active else "0"
            cursor.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES ('maintenance', ?)", (val,))
            conn.commit()

    def is_maintenance_mode(self) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM bot_settings WHERE key = 'maintenance'")
            row = cursor.fetchone()
            if row:
                return row["value"] == "1" # Name access
            return False

db = Database()
