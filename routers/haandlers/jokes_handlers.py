from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from services.api_client import APIClient
from services.cache_service import cache
from storage.database import db
from keyboards.inline import get_add_to_favorites, get_content_with_back
from utils.logger import logger

router = Router()

async def handle_joke(message_or_callback):
    """Обработка запроса шутки"""
    user_id = message_or_callback.from_user.id
    
    # Проверяем и создаем пользователя если нужно
    user = db.get_user(user_id)
    if not user:
        db.create_user(
            user_id=user_id,
            username=message_or_callback.from_user.username,
            first_name=message_or_callback.from_user.first_name
        )
    
    # Проверяем кэш
    cached_joke = cache.get("joke_recent")
    if cached_joke:
        joke = cached_joke
        logger.info("Joke served from cache")
    else:
        async with APIClient() as client:
            joke = await client.get_joke()
        
        if joke:
            cache.set("joke_recent", joke)
        else:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("❌ Не удалось получить шутку. Попробуйте позже.")
            else:
                await message_or_callback.message.edit_text("❌ Не удалось получить шутку. Попробуйте позже.")
            return
    
    # Сохраняем контент для возможности добавления в избранное
    from routers.handlers.favorites_handlers import save_last_content
    save_last_content(user_id, joke)
    
    # Сохраняем в историю
    db.add_to_history(user_id, "joke", joke)
    
    response_text = f"😄 **Шутка для вас:**\n\n{joke}"
    keyboard = get_content_with_back("joke")
    
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(response_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await message_or_callback.message.edit_text(response_text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "joke")
async def joke_callback(callback: CallbackQuery):
    """Callback для шутки"""
    await handle_joke(callback)
    await callback.answer()