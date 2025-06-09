from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def build_favorites_list(favorites: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Построить клавиатуру со списком избранного"""
    keyboard = []
    
    for i, favorite in enumerate(favorites[:10]):  # Показываем максимум 10
        content = favorite["content"]
        if len(content) > 30:
            content = content[:30] + "..."
        
        type_emoji = {
            "catfact": "🐱",
            "joke": "😄", 
            "randomfact": "🎲"
        }.get(favorite["type"], "📝")
        
        button_text = f"{type_emoji} {content}"
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"view_favorite:{i}"
            )
        ])
    
    # Добавляем кнопку возврата
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="favorites")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def build_remove_favorites_list(favorites: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Построить клавиатуру для удаления из избранного"""
    keyboard = []
    
    for i, favorite in enumerate(favorites[:10]):
        content = favorite["content"]
        if len(content) > 25:
            content = content[:25] + "..."
        
        type_emoji = {
            "catfact": "🐱",
            "joke": "😄", 
            "randomfact": "🎲"
        }.get(favorite["type"], "📝")
        
        button_text = f"❌ {type_emoji} {content}"
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"delete_favorite:{i}"
            )
        ])
    
    # Добавляем кнопку возврата
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="favorites")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
