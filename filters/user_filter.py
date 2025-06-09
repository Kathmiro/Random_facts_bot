from aiogram.filters import BaseFilter
from aiogram.types import Message
from storage.database import db

class RegisteredUserFilter(BaseFilter):
    def __init__(self):
        pass
    
    async def __call__(self, message: Message) -> bool:
        user = db.get_user(message.from_user.id)
        return user is not None

class NewUserFilter(BaseFilter):
    def __init__(self):
        pass
    
    async def __call__(self, message: Message) -> bool:
        user = db.get_user(message.from_user.id)
        return user is None