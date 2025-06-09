from aiogram.filters import BaseFilter
from aiogram.types import Message

class AdminFilter(BaseFilter):
    def __init__(self, admin_ids: list = None):
        self.admin_ids = admin_ids or []
    
    async def __call__(self, message: Message) -> bool:
        # Возвращаем False, так как не используем админов
        return False