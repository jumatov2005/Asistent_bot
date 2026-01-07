import asyncpg
import logging
import os
from datetime import datetime
from typing import List, Optional, Union, Dict, Any
from config import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT

class Database:
    def __init__(self):
        self.pool = None

    async def create(self):
        """
        Create connection pool.
        """
        try:
            self.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                host=DB_HOST,
                port=DB_PORT
            )
            await self.create_tables()
            logging.info("Connected to PostgreSQL successfully")
        except Exception as e:
            logging.critical(f"Failed to connect to DB: {e}")
            raise

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            # Users
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id BIGINT PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    language TEXT,
                    role TEXT,
                    created_at TIMESTAMP
                );
            """)

            # Anonymous Messages
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS anonymous_messages (
                    id SERIAL PRIMARY KEY,
                    sender_telegram_id BIGINT,
                    sender_username TEXT,
                    message TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    is_replied BOOLEAN DEFAULT FALSE,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP
                );
            """)

            # Anonymous Replies
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS anonymous_replies (
                    id SERIAL PRIMARY KEY,
                    receiver_telegram_id BIGINT,
                    reply_text TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    created_at TIMESTAMP
                );
            """)

            # Comments
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id SERIAL PRIMARY KEY,
                    sender_telegram_id BIGINT,
                    sender_role TEXT,
                    sender_username TEXT,
                    comment TEXT,
                    message_type TEXT DEFAULT 'text',
                    file_id TEXT,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP
                );
            """)

            # Broadcast Logs
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS broadcast_logs (
                    id SERIAL PRIMARY KEY,
                    sender_id BIGINT,
                    target_group TEXT,
                    message_type TEXT,
                    file_id TEXT,
                    caption TEXT,
                    recipients_count INTEGER,
                    created_at TIMESTAMP
                );
            """)

            # Bot Settings
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS bot_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
            """)

    # --- USER METHODS ---
    async def add_user(self, telegram_id: int, first_name: str, username: str, language: str, role: str = "user"):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO users (telegram_id, first_name, username, language, role, created_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (telegram_id) DO NOTHING
                """, telegram_id, first_name, username, language, role, datetime.now())
        except Exception as e:
            logging.error(f"Error adding user: {e}")

    async def get_user(self, telegram_id: int) -> Optional[Dict]:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)

    async def update_user_language(self, telegram_id: int, language: str):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET language = $1 WHERE telegram_id = $2", language, telegram_id)

    async def update_user_role(self, telegram_id: int, role: str):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET role = $1 WHERE telegram_id = $2", role, telegram_id)

    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        clean_username = username.strip().replace("@", "")
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE username = $1", clean_username)

    # --- ADMIN METHODS ---
    async def get_admins(self) -> List[Dict]:
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM users WHERE role IN ('admin', 'super_admin')")

    async def get_all_user_ids(self) -> List[int]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch("SELECT telegram_id FROM users")
            return [r["telegram_id"] for r in records]

    async def get_admin_ids(self) -> List[int]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch("SELECT telegram_id FROM users WHERE role IN ('admin', 'super_admin')")
            return [r["telegram_id"] for r in records]

    async def downgrade_admin(self, username: str) -> bool:
        user = await self.get_user_by_username(username)
        if user and user["role"] == 'admin':
            await self.update_user_role(user["telegram_id"], 'user')
            return True
        return False

    async def get_stats(self) -> dict:
        async with self.pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM users")
            users = await conn.fetchval("SELECT COUNT(*) FROM users WHERE role = 'user'")
            admins = await conn.fetchval("SELECT COUNT(*) FROM users WHERE role IN ('admin', 'super_admin')")
            return {"total": total, "users": users, "admins": admins}

    # --- MESSAGES & COMMENTS ---
    async def add_anonymous_message(self, telegram_id: int, username: str, message: str, msg_type: str = "text", file_id: str = None) -> int:
        async with self.pool.acquire() as conn:
            # fetchval returns the SERIAL id
            return await conn.fetchval("""
                INSERT INTO anonymous_messages (sender_telegram_id, sender_username, message, message_type, file_id, is_replied, is_read, created_at)
                VALUES ($1, $2, $3, $4, $5, FALSE, FALSE, $6)
                RETURNING id
            """, telegram_id, username, message, msg_type, file_id, datetime.now())

    async def get_unreplied_anonymous_messages(self, limit: int = 10) -> List[Dict]:
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM anonymous_messages WHERE is_replied = FALSE ORDER BY id DESC LIMIT $1", limit)

    async def get_filtered_anonymous_messages(self, filter_type: str) -> List[Dict]:
        async with self.pool.acquire() as conn:
            # PostgreSQL interval syntax
            if filter_type == "1_day_new":
                return await conn.fetch("SELECT * FROM anonymous_messages WHERE created_at >= NOW() - INTERVAL '1 day' AND is_read = FALSE ORDER BY id DESC")
            elif filter_type == "1_week":
                return await conn.fetch("SELECT * FROM anonymous_messages WHERE created_at >= NOW() - INTERVAL '7 days' ORDER BY id DESC")
            elif filter_type == "1_month":
                return await conn.fetch("SELECT * FROM anonymous_messages WHERE created_at >= NOW() - INTERVAL '30 days' ORDER BY id DESC")
            else:
                return await conn.fetch("SELECT * FROM anonymous_messages ORDER BY id DESC LIMIT 20")

    async def mark_anonymous_messages_read(self, ids: List[int]):
        if not ids: return
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE anonymous_messages SET is_read = TRUE WHERE id = ANY($1::int[])", ids)

    async def delete_read_anonymous_messages(self):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM anonymous_messages WHERE is_read = TRUE")

    async def add_comment(self, telegram_id: int, role: str, username: str, comment: str, msg_type: str = "text", file_id: str = None):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO comments (sender_telegram_id, sender_role, sender_username, comment, message_type, file_id, is_read, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, FALSE, $7)
            """, telegram_id, role, username, comment, msg_type, file_id, datetime.now())

    async def get_filtered_comments(self, filter_type: str) -> List[Dict]:
        async with self.pool.acquire() as conn:
            if filter_type == "1_day_new":
                return await conn.fetch("SELECT * FROM comments WHERE created_at >= NOW() - INTERVAL '1 day' AND is_read = FALSE ORDER BY id DESC")
            elif filter_type == "1_week":
                return await conn.fetch("SELECT * FROM comments WHERE created_at >= NOW() - INTERVAL '7 days' ORDER BY id DESC")
            elif filter_type == "1_month":
                return await conn.fetch("SELECT * FROM comments WHERE created_at >= NOW() - INTERVAL '30 days' ORDER BY id DESC")
            else:
                return await conn.fetch("SELECT * FROM comments ORDER BY id DESC LIMIT 20")

    async def mark_comments_read(self, ids: List[int]):
        if not ids: return
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE comments SET is_read = TRUE WHERE id = ANY($1::int[])", ids)

    async def delete_read_comments(self):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM comments WHERE is_read = TRUE")

    async def add_reply_log(self, receiver_id: int, text: str, msg_type: str = "text", file_id: str = None):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO anonymous_replies (receiver_telegram_id, reply_text, message_type, file_id, created_at)
                VALUES ($1, $2, $3, $4, $5)
            """, receiver_id, text, msg_type, file_id, datetime.now())

    async def add_broadcast_log(self, sender_id: int, target: str, msg_type: str, file_id: str, caption: str, count: int):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO broadcast_logs (sender_id, target_group, message_type, file_id, caption, recipients_count, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, sender_id, target, msg_type, file_id, caption, count, datetime.now())

    # --- SETTINGS / MAINTENANCE ---
    async def set_maintenance_mode(self, active: bool):
        async with self.pool.acquire() as conn:
            val = "1" if active else "0"
            await conn.execute("""
                INSERT INTO bot_settings (key, value) VALUES ('maintenance', $1)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
            """, val)

    async def is_maintenance_mode(self) -> bool:
        async with self.pool.acquire() as conn:
            val = await conn.fetchval("SELECT value FROM bot_settings WHERE key = 'maintenance'")
            return val == "1"

db = Database()
