from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.api_client import APIClient
from services.cache_service import cache
from storage.database import db
from keyboards.inline import get_add_to_favorites, get_main_menu, get_prediction_menu, get_content_with_back
from utils.formatters import format_prediction_result
from utils.logger import logger
from states.user_states import UserStates

router = Router()

async def handle_cat_fact(message_or_callback):
    """Обработка запроса факта о котах"""
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
    cached_fact = cache.get("catfact_recent")
    if cached_fact:
        fact = cached_fact
        logger.info("Cat fact served from cache")
    else:
        async with APIClient() as client:
            fact = await client.get_cat_fact()
        
        if fact:
            cache.set("catfact_recent", fact)
        else:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("❌ Не удалось получить факт о котах. Попробуйте позже.")
            else:
                await message_or_callback.message.edit_text("❌ Не удалось получить факт о котах. Попробуйте позже.")
            return
    
    # Сохраняем контент для возможности добавления в избранное
    from routers.handlers.favorites_handlers import save_last_content
    save_last_content(user_id, fact)
    
    # Сохраняем в историю
    db.add_to_history(user_id, "catfact", fact)
    
    response_text = f"🐱 **Факт о котах:**\n\n{fact}"
    keyboard = get_content_with_back("catfact")
    
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(response_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await message_or_callback.message.edit_text(response_text, reply_markup=keyboard, parse_mode="Markdown")

async def handle_random_fact(message_or_callback):
    """Обработка запроса случайного факта"""
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
    cached_fact = cache.get("randomfact_recent")
    if cached_fact:
        fact = cached_fact
        logger.info("Random fact served from cache")
    else:
        async with APIClient() as client:
            fact = await client.get_random_fact()
        
        if fact:
            cache.set("randomfact_recent", fact)
        else:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("❌ Не удалось получить случайный факт. Попробуйте позже.")
            else:
                await message_or_callback.message.edit_text("❌ Не удалось получить случайный факт. Попробуйте позже.")
            return
    
    # Сохраняем контент для возможности добавления в избранное
    from routers.handlers.favorites_handlers import save_last_content
    save_last_content(user_id, fact)
    
    # Сохраняем в историю
    db.add_to_history(user_id, "randomfact", fact)
    
    response_text = f"🎲 **Случайный факт:**\n\n{fact}"
    keyboard = get_content_with_back("randomfact")
    
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(response_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await message_or_callback.message.edit_text(response_text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "catfact")
async def catfact_callback(callback: CallbackQuery):
    """Callback для факта о котах"""
    await handle_cat_fact(callback)
    await callback.answer()

@router.callback_query(F.data == "randomfact")
async def randomfact_callback(callback: CallbackQuery):
    """Callback для случайного факта"""
    await handle_random_fact(callback)
    await callback.answer()

@router.callback_query(F.data == "prediction")
async def prediction_callback(callback: CallbackQuery):
    """Callback для меню предсказаний"""
    await callback.message.edit_text(
        "🔮 **Предсказания по имени:**\n\nВыберите тип предсказания:",
        reply_markup=get_prediction_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("predict_"))
async def handle_prediction_request(callback: CallbackQuery, state: FSMContext):
    """Обработка запроса предсказания"""
    prediction_type = callback.data.split("_")[1]  # age или gender
    
    await state.set_state(UserStates.waiting_for_name_prediction)
    await state.update_data(prediction_type=prediction_type)
    
    prediction_text = "возраста" if prediction_type == "age" else "пола"
    
    await callback.message.edit_text(
        f"🔮 Введите имя для предсказания {prediction_text}:",
        reply_markup=get_main_menu()
    )
    
    await callback.answer(f"Введите имя для предсказания {prediction_text}")

async def handle_name_prediction(message: Message, prediction_type: str):
    """Обработка предсказания по имени"""
    name = message.text.strip()
    if not name or len(name) > 50:
        await message.answer("❌ Пожалуйста, введите корректное имя (до 50 символов)")
        return
    
    user_id = message.from_user.id
    
    # Проверяем кэш
    cache_key = f"{prediction_type}_{name.lower()}"
    cached_result = cache.get(cache_key)
    
    if cached_result:
        result = cached_result
        logger.info(f"Prediction {prediction_type} for {name} served from cache")
    else:
        async with APIClient() as client:
            if prediction_type == "age":
                result = await client.get_age_prediction(name)
            else:
                result = await client.get_gender_prediction(name)
        
        if result:
            cache.set(cache_key, result)
        else:
            await message.answer("❌ Не удалось получить предсказание. Попробуйте позже.")
            return
    
    # Форматируем результат
    response_text = format_prediction_result(result, prediction_type)
    
    # Сохраняем контент для возможности добавления в избранное
    from routers.handlers.favorites_handlers import save_last_content
    save_last_content(user_id, response_text)
    
    # Сохраняем в историю
    db.add_to_history(user_id, "prediction", response_text)
    
    keyboard = get_content_with_back("prediction")
    await message.answer(response_text, reply_markup=keyboard, parse_mode="Markdown")