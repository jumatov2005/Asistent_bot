from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from database.db import db
from texts import TEXTS

class MaintenanceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        # Check maintenance efficiently (Async)
        if await db.is_maintenance_mode():
            user_id = event.from_user.id
            user = await db.get_user(user_id)
            
            # Agar user bo'lmasa yoki super admin bo'lmasa -> bloklanadi
            if not user or user["role"] != "super_admin":
                # Tilni aniqlash
                lang = user["language"] if user else "uz"
                try:
                    await event.answer(TEXTS["maintenance_active_msg"][lang], parse_mode="HTML")
                except:
                    pass
                return
                
        return await handler(event, data)
