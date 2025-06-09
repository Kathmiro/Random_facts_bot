import json
import os
import shutil
from typing import Dict, List, Any, Optional
from datetime import datetime
from config.settings import settings
from utils.logger import logger

class Database:
    def __init__(self):
        self.file_path = settings.USERS_FILE
        self._ensure_storage_dir()
        self._init_database()
    
    def _ensure_storage_dir(self):
        """Создать директорию storage если её нет"""
        os.makedirs("storage", exist_ok=True)
    
    def _init_database(self):
        """Инициализировать базу данных"""
        initial_data = {
            "users": {},
            "stats": {
                "total_users": 0,
                "total_requests": 0,
                "created_at": datetime.now().isoformat()
            }
        }
        try:
            self._save_data(initial_data)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Загрузить данные из файла"""
        try:
            if not os.path.exists(self.file_path):
                # Если файла нет, создаем его с начальными данными
                self._init_database()
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    # Если файл пустой, инициализируем заново
                    logger.warning("Database file is empty, reinitializing...")
                    self._init_database()
                    return {"users": {}, "stats": {"total_users": 0, "total_requests": 0}}
                
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading database: {e}")
            # При ошибке создаем новую базу
            self._init_database()
            return {"users": {}, "stats": {"total_users": 0, "total_requests": 0}}
        except Exception as e:
            logger.error(f"Unexpected error loading database: {e}")
            return {"users": {}, "stats": {"total_users": 0, "total_requests": 0}}
    
    def _save_data(self, data: Dict[str, Any]):
        """Сохранить данные в файл"""
        try:
            # Создаем временный файл для безопасного сохранения
            temp_file = self.file_path + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Заменяем основной файл только если запись прошла успешно
            import shutil
            shutil.move(temp_file, self.file_path)
            logger.info("Database saved successfully")
        except Exception as e:
            logger.error(f"Error saving database: {e}")
            # Удаляем временный файл если что-то пошло не так
            if os.path.exists(self.file_path + '.tmp'):
                os.remove(self.file_path + '.tmp')
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить данные пользователя"""
        data = self._load_data()
        return data["users"].get(str(user_id))
    
    def create_user(self, user_id: int, username: str = None, first_name: str = None):
        """Создать нового пользователя"""
        data = self._load_data()
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "favorites": [],
            "history": [],
            "created_at": datetime.now().isoformat(),
            "request_count": 0
        }
        
        data["users"][str(user_id)] = user_data
        data["stats"]["total_users"] += 1
        self._save_data(data)
        logger.info(f"User {user_id} created")
        return user_data
    
    def update_user(self, user_id: int, updates: Dict[str, Any]):
        """Обновить данные пользователя"""
        data = self._load_data()
        if str(user_id) in data["users"]:
            data["users"][str(user_id)].update(updates)
            self._save_data(data)
            logger.info(f"User {user_id} updated")
            return True
        return False
    
    def add_to_favorites(self, user_id: int, item: str, item_type: str):
        """Добавить элемент в избранное"""
        user = self.get_user(user_id)
        if user:
            favorite_item = {
                "content": item,
                "type": item_type,
                "added_at": datetime.now().isoformat()
            }
            user["favorites"].append(favorite_item)
            self.update_user(user_id, {"favorites": user["favorites"]})
            return True
        return False
    
    def remove_from_favorites(self, user_id: int, index: int):
        """Удалить элемент из избранного"""
        user = self.get_user(user_id)
        if user and 0 <= index < len(user["favorites"]):
            removed_item = user["favorites"].pop(index)
            self.update_user(user_id, {"favorites": user["favorites"]})
            return removed_item
        return None
    
    def add_to_history(self, user_id: int, command: str, content: str):
        """Добавить запись в историю"""
        user = self.get_user(user_id)
        if user:
            history_item = {
                "command": command,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
            user["history"].append(history_item)
            
            # Ограничиваем историю последними 50 записями
            if len(user["history"]) > 50:
                user["history"] = user["history"][-50:]
            
            user["request_count"] += 1
            self.update_user(user_id, {
                "history": user["history"],
                "request_count": user["request_count"]
            })
            
            # Обновляем общую статистику
            data = self._load_data()
            data["stats"]["total_requests"] += 1
            self._save_data(data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику"""
        data = self._load_data()
        stats = data.get("stats", {})
        
        # Добавляем дополнительную статистику
        users = data.get("users", {})
        active_users = len([u for u in users.values() if u.get("request_count", 0) > 0])
        total_favorites = sum(len(u.get("favorites", [])) for u in users.values())
        
        stats.update({
            "active_users": active_users,
            "total_favorites": total_favorites
        })
        
        return stats
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Получить всех пользователей"""
        data = self._load_data()
        return list(data["users"].values())

# Глобальный экземпляр базы данных
db = Database()
