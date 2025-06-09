from typing import List, Dict, Any
from datetime import datetime

def format_favorites(favorites: List[Dict[str, Any]]) -> str:
    """Форматировать список избранного"""
    if not favorites:
        return "❌ У вас пока нет избранных элементов"
    
    formatted = "⭐ **Ваше избранное:**\n\n"
    
    for i, favorite in enumerate(favorites, 1):
        type_emoji = {
            "catfact": "🐱",
            "joke": "😄", 
            "randomfact": "🎲"
        }.get(favorite["type"], "📝")
        
        content = favorite["content"]
        if len(content) > 100:
            content = content[:100] + "..."
        
        added_date = datetime.fromisoformat(favorite["added_at"]).strftime("%d.%m.%Y")
        
        formatted += f"{i}. {type_emoji} {content}\n"
        formatted += f"   📅 Добавлено: {added_date}\n\n"
    
    return formatted

def format_history(history: List[Dict[str, Any]]) -> str:
    """Форматировать историю запросов"""
    if not history:
        return "❌ История пуста"
    
    formatted = "📋 **Ваша история:**\n\n"
    
    # Показываем последние 10 записей
    recent_history = history[-10:] if len(history) > 10 else history
    
    for item in reversed(recent_history):
        command_emoji = {
            "catfact": "🐱",
            "joke": "😄", 
            "randomfact": "🎲",
            "prediction": "🔮"
        }.get(item["command"], "📝")
        
        content = item["content"]
        if len(content) > 80:
            content = content[:80] + "..."
        
        timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%d.%m %H:%M")
        
        formatted += f"{command_emoji} {content}\n"
        formatted += f"   🕐 {timestamp}\n\n"
    
    if len(history) > 10:
        formatted += f"... и еще {len(history) - 10} записей"
    
    return formatted

def format_stats(stats: Dict[str, Any]) -> str:
    """Форматировать статистику бота"""
    formatted = "📊 **Статистика бота:**\n\n"
    
    formatted += f"👥 Всего пользователей: {stats.get('total_users', 0)}\n"
    formatted += f"✅ Активных пользователей: {stats.get('active_users', 0)}\n"
    formatted += f"📝 Всего запросов: {stats.get('total_requests', 0)}\n"
    formatted += f"⭐ Всего в избранном: {stats.get('total_favorites', 0)}\n\n"
    
    if stats.get('created_at'):
        created_date = datetime.fromisoformat(stats['created_at']).strftime("%d.%m.%Y")
        formatted += f"🚀 Запущен: {created_date}"
    
    return formatted

def format_prediction_result(prediction_data: Dict[str, Any], prediction_type: str) -> str:
    """Форматировать результат предсказания"""
    name = prediction_data.get("name", "").title()
    
    if prediction_type == "age":
        age = prediction_data.get("age")
        count = prediction_data.get("count", 0)
        return f"🎂 **Предсказание возраста для {name}:**\n\n" \
               f"Предполагаемый возраст: **{age} лет**\n" \
               f"Уверенность: {count} записей в базе"
    
    elif prediction_type == "gender":
        gender = prediction_data.get("gender")
        gender_ru = "Мужской" if gender == "male" else "Женский"
        probability = prediction_data.get("probability", 0)
        count = prediction_data.get("count", 0)
        
        return f"👫 **Предсказание пола для {name}:**\n\n" \
               f"Предполагаемый пол: **{gender_ru}**\n" \
               f"Вероятность: {probability:.1%}\n" \
               f"Уверенность: {count} записей в базе"
    
    return "❌ Не удалось получить предсказание"
