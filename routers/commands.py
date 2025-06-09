from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from storage.database import db
from filters.admin_filter import AdminFilter
from filters.user_filter import NewUserFilter, RegisteredUserFilter
from keyboards.inline import get_main_menu
from utils.formatters import format_stats
from utils.logger import logger

router = Router()

@router.message(Command("start"), NewUserFilter())
async def start_new_user(message: Message):
    """Приветствие нового пользователя"""
    user = message.from_user
    
    # Создаем пользователя в базе
    db.create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    
    welcome_text = f"👋 Привет, {user.first_name}!\n\n" \
                   f"Добро пожаловать в **RandomFactsBot**! 🎲\n\n" \
                   f"Я могу предложить тебе:\n" \
                   f"🐱 Интересные факты о котах\n" \
                   f"😄 Забавные шутки\n" \
                   f"🎲 Случайные факты\n" \
                   f"🔮 Предсказания по имени\n" \
                   f"⭐ Сохранение в избранное\n\n" \
                   f"Выбери что тебя интересует!"
    
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    logger.info(f"New user registered: {user.id}")

@router.message(Command("start"), RegisteredUserFilter())
async def start_existing_user(message: Message):
    """Приветствие существующего пользователя"""
    user = message.from_user
    
    welcome_text = f"С возвращением, {user.first_name}! 👋\n\n" \
                   f"Что будем изучать сегодня?"
    
    await message.answer(welcome_text, reply_markup=get_main_menu())

@router.message(Command("help"))
async def help_command(message: Message):
    """Команда помощи"""
    help_text = "🤖 **Справка по RandomFactsBot**\n\n" \
                "**Доступные команды:**\n" \
                "/start - Начать работу с ботом\n" \
                "/help - Показать эту справку\n" \
                "/catfact - Случайный факт о котах\n" \
                "/joke - Случайная шутка\n" \
                "/randomfact - Случайный факт\n" \
                "/favorites - Управление избранным\n" \
                "/history - История ваших запросов\n\n" \
                "**Дополнительные возможности:**\n" \
                "⭐ Добавление контента в избранное\n" \
                "📋 Просмотр истории запросов\n" \
                "🔮 Предсказания по имени\n\n" \
                "Используйте кнопки для удобной навигации!"
    
    await message.answer(help_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@router.message(Command("stats"))
async def stats_command(message: Message):
    """Статистика бота (доступна всем пользователям)"""
    stats = db.get_stats()
    stats_text = format_stats(stats)
    
    await message.answer(stats_text, parse_mode="Markdown")
    logger.info(f"User {message.from_user.id} requested stats")

@router.message(Command("catfact"))
async def catfact_command(message: Message):
    """Команда получения факта о котах"""
    from routers.handlers.facts_handlers import handle_cat_fact
    await handle_cat_fact(message)

@router.message(Command("joke"))
async def joke_command(message: Message):
    """Команда получения шутки"""
    from routers.handlers.jokes_handlers import handle_joke
    await handle_joke(message)

@router.message(Command("randomfact"))
async def randomfact_command(message: Message):
    """Команда получения случайного факта"""
    from routers.handlers.facts_handlers import handle_random_fact
    await handle_random_fact(message)

@router.message(Command("favorites"))
async def favorites_command(message: Message):
    """Команда управления избранным"""
    from keyboards.inline import get_favorites_menu
    await message.answer("⭐ Управление избранным:", reply_markup=get_favorites_menu())

@router.message(Command("history"))
async def back_command(message: Message):
    """Команда возврата в главное меню"""
    await message.answer(
        "🎲 **FactFusion Bot**\n\nВыберите что вас интересует:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )
async def history_command(message: Message):
    """Команда просмотра истории"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        # Создаем пользователя если его нет
        db.create_user(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )
        user = db.get_user(user_id)
    
    from utils.formatters import format_history
    history_text = format_history(user.get("history", []))
    
    from keyboards.inline import get_back_button
    await message.answer(history_text, reply_markup=get_back_button(), parse_mode="Markdown")
