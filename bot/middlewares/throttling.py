import time
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from collections import defaultdict

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5):
        self.limit = limit
        self.cache = defaultdict(float)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        user_id = event.from_user.id
        current_time = time.time()
        last_time = self.cache[user_id]
        
        # Agar vaqt chegarasi buzilsa
        if current_time - last_time < self.limit:
            # Spam oldini olish uchun shunchaki ignor qilamiz
            # Yoki ogohlantirish berish mumkin (lekin bu ham spam bo'lishi mumkin)
            return
            
        self.cache[user_id] = current_time
        return await handler(event, data)
