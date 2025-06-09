from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from utils.logger import logger

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user_info = f"User {event.from_user.id} (@{event.from_user.username})"
            message_info = f"Message: {event.text[:50]}..." if event.text and len(event.text) > 50 else f"Message: {event.text}"
            logger.info(f"{user_info} - {message_info}")
        
        elif isinstance(event, CallbackQuery):
            user_info = f"User {event.from_user.id} (@{event.from_user.username})"
            callback_info = f"Callback: {event.data}"
            logger.info(f"{user_info} - {callback_info}")
        
        result = await handler(event, data)
        return result