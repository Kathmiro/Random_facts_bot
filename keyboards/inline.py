from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню с основными функциями"""
    keyboard = [
        [
            InlineKeyboardButton(text="🐱 Факт о котах", callback_data="catfact"),
            InlineKeyboardButton(text="😄 Шутка", callback_data="joke")
        ],
        [
            InlineKeyboardButton(text="🎲 Случайный факт", callback_data="randomfact"),
            InlineKeyboardButton(text="🔮 Предсказание", callback_data="prediction")
        ],
        [
            InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites"),
            InlineKeyboardButton(text="📋 История", callback_data="history")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_favorites_menu() -> InlineKeyboardMarkup:
    """Меню управления избранным"""
    keyboard = [
        [
            InlineKeyboardButton(text="📋 Показать избранное", callback_data="show_favorites")
        ],
        [
            InlineKeyboardButton(text="❌ Удалить из избранного", callback_data="remove_favorite")
        ],
        [
            InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_add_to_favorites(content_type: str) -> InlineKeyboardMarkup:
    """Кнопка добавления в избранное с кнопкой назад"""
    keyboard = [
        [
            InlineKeyboardButton(text="⭐ Добавить в избранное", callback_data=f"add_favorite:{content_type}")
        ],
        [
            InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_button() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    keyboard = [
        [
            InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_prediction_menu() -> InlineKeyboardMarkup:
    """Меню предсказаний с кнопкой назад"""
    keyboard = [
        [
            InlineKeyboardButton(text="🎂 Угадать возраст", callback_data="predict_age"),
            InlineKeyboardButton(text="👫 Угадать пол", callback_data="predict_gender")
        ],
        [
            InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_content_with_back(content_type: str) -> InlineKeyboardMarkup:
    """Клавиатура с кнопками действий и возврата"""
    keyboard = [
        [
            InlineKeyboardButton(text="⭐ В избранное", callback_data=f"add_favorite:{content_type}"),
            InlineKeyboardButton(text="🔄 Еще раз", callback_data=content_type)
        ],
        [
            InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)