import time
from typing import Optional, Any, Dict
from config.settings import settings
from utils.logger import logger

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _is_expired(self, timestamp: float) -> bool:
        """Проверить, истек ли срок кэша"""
        return time.time() - timestamp > settings.CACHE_TTL
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        if key in self._cache:
            cache_entry = self._cache[key]
            if not self._is_expired(cache_entry["timestamp"]):
                logger.info(f"Cache hit for key: {key}")
                return cache_entry["data"]
            else:
                # Удаляем устаревший кэш
                del self._cache[key]
                logger.info(f"Cache expired for key: {key}")
        
        logger.info(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Сохранить значение в кэш"""
        self._cache[key] = {
            "data": value,
            "timestamp": time.time()
        }
        logger.info(f"Cache set for key: {key}")
    
    def clear(self) -> None:
        """Очистить весь кэш"""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def stats(self) -> Dict[str, int]:
        """Получить статистику кэша"""
        total_entries = len(self._cache)
        expired_entries = sum(1 for entry in self._cache.values() 
                            if self._is_expired(entry["timestamp"]))
        
        return {
            "total_entries": total_entries,
            "active_entries": total_entries - expired_entries,
            "expired_entries": expired_entries
        }

# Глобальный экземпляр кэша
cache = CacheService()