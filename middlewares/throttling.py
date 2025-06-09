import time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from config.settings import settings

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = settings.RATE_LIMIT):
        self.rate_limit = rate_limit
        self.last_request: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user_id = event.from_user.id
            current_time = time.time()
            
            if user_id in self.last_request:
                time_passed = current_time - self.last_request[user_id]
                if time_passed < self.rate_limit:
                    await event.answer("⏳ Слишком много запросов! Подождите немного.")
                    return
            
            self.last_request[user_id] = current_time
        
        return await handler(event, data)