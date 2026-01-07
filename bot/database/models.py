from dataclasses import dataclass
from datetime import datetime

# Users jadvali modeli
@dataclass
class User:
    telegram_id: int
    first_name: str
    username: str
    language: str
    role: str
    created_at: str

# Anonymous Messages jadvali modeli
@dataclass
class AnonymousMessage:
    id: int
    sender_telegram_id: int
    sender_username: str
    message: str
    created_at: str

# Anonymous Replies jadvali modeli
@dataclass
class AnonymousReply:
    message_id: int
    receiver_telegram_id: int
    reply_text: str
    created_at: str
