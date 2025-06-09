from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from storage.database import db
from keyboards.inline import get_favorites_menu, get_main_menu, get_back_button
from keyboards.builders import build_favorites_list, build_remove_favorites_list
from utils.formatters import format_favorites
from states.user_states import UserStates
from utils.logger import logger

router = Router()

# Глобальная переменная для хранения последнего контента для добавления в избранное
last_content = {}

@router.callback_query(F.data == "favorites")
async def favorites_menu(callback: CallbackQuery):
    """Меню управления избранным"""
    await callback.message.edit_text(
        "⭐ **Управление избранным:**\n\nВыберите действие:",
        reply_markup=get_favorites_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "show_favorites")
async def show_favorites(callback: CallbackQuery):
    """Показать список избранного"""
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    favorites = user.get("favorites", [])
    
    if not favorites:
        await callback.message.edit_text(
            "❌ У вас пока нет избранных элементов\n\n"
            "Используйте кнопку ⭐ после получения фактов, шуток или предсказаний!",
            reply_markup=get_back_button()
        )
    else:
        keyboard = build_favorites_list(favorites)
        await callback.message.edit_text(
            "⭐ **Ваше избранное:**\n\nНажмите на элемент для просмотра:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("view_favorite:"))
async def view_favorite(callback: CallbackQuery):
    """Просмотр конкретного избранного элемента"""
    try:
        favorite_index = int(callback.data.split(":")[1])
        user = db.get_user(callback.from_user.id)
        
        if not user or favorite_index >= len(user.get("favorites", [])):
            await callback.answer("❌ Элемент не найден")
            return
        
        favorite = user["favorites"][favorite_index]
        content = favorite["content"]
        type_emoji = {
            "catfact": "🐱",
            "joke": "😄", 
            "randomfact": "🎲",
            "prediction": "🔮"
        }.get(favorite["type"], "📝")
        
        response_text = f"{type_emoji} **Из избранного:**\n\n{content}"
        
        await callback.message.edit_text(
            response_text,
            reply_markup=get_back_button(),
            parse_mode="Markdown"
        )
        
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка при просмотре элемента")
    
    await callback.answer()

@router.callback_query(F.data == "remove_favorite")
async def remove_favorite_menu(callback: CallbackQuery):
    """Меню удаления из избранного"""
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    favorites = user.get("favorites", [])
    
    if not favorites:
        await callback.message.edit_text(
            "❌ У вас пока нет избранных элементов для удаления\n\n"
            "Сначала добавьте что-нибудь в избранное!",
            reply_markup=get_back_button()
        )
    else:
        keyboard = build_remove_favorites_list(favorites)
        await callback.message.edit_text(
            "❌ **Удаление из избранного:**\n\nВыберите элемент для удаления:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("delete_favorite:"))
async def delete_favorite(callback: CallbackQuery):
    """Удаление элемента из избранного"""
    try:
        favorite_index = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        
        removed_item = db.remove_from_favorites(user_id, favorite_index)
        
        if removed_item:
            await callback.message.edit_text(
                "✅ Элемент удален из избранного",
                reply_markup=get_favorites_menu()
            )
            logger.info(f"User {user_id} removed item from favorites")
        else:
            await callback.message.edit_text(
                "❌ Не удалось удалить элемент",
                reply_markup=get_favorites_menu()
            )
            
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка при удалении элемента")
    
    await callback.answer()

@router.callback_query(F.data.startswith("add_favorite:"))
async def add_to_favorites(callback: CallbackQuery):
    """Добавление в избранное"""
    content_type = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    # Получаем последний контент для этого пользователя
    if user_id not in last_content:
        await callback.answer("❌ Контент для добавления не найден")
        return
    
    content = last_content[user_id]
    
    # Проверяем, существует ли пользователь в базе
    user = db.get_user(user_id)
    if not user:
        # Создаем пользователя если его нет
        db.create_user(
            user_id=user_id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name
        )
    
    success = db.add_to_favorites(user_id, content, content_type)
    
    if success:
        await callback.answer("✅ Добавлено в избранное!", show_alert=True)
        logger.info(f"User {user_id} added {content_type} to favorites")
    else:
        await callback.answer("❌ Не удалось добавить в избранное")

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        "🎲 **RandomFactsBot**\n\nВыберите что вас интересует:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

# Функция для сохранения последнего контента (вызывается из других хендлеров)
def save_last_content(user_id: int, content: str):
    """Сохранить последний контент для возможности добавления в избранное"""
    last_content[user_id] = content