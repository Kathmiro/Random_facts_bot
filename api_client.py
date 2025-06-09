import aiohttp
import asyncio
from typing import Optional, Dict, Any
from utils.logger import logger
from config.settings import settings

class APIClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=10)
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Базовый метод для выполнения HTTP запросов с обработкой ошибок"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(timeout=self.timeout)
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successful API call to {url}")
                    return data
                else:
                    logger.error(f"API request failed with status {response.status} for URL: {url}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout error for URL: {url}")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"Client error for URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for URL {url}: {e}")
            return None
    
    async def get_cat_fact(self) -> Optional[str]:
        """Получить случайный факт о котах"""
        data = await self._make_request(settings.CAT_FACTS_API)
        return data.get("fact") if data else None
    
    async def get_joke(self) -> Optional[str]:
        """Получить случайную шутку"""
        data = await self._make_request(settings.JOKE_API)
        if data and not data.get("error"):
            if data.get("type") == "single":
                return data.get("joke")
            else:
                setup = data.get("setup", "")
                delivery = data.get("delivery", "")
                return f"{setup}\n\n{delivery}"
        return None
    
    async def get_random_fact(self) -> Optional[str]:
        """Получить случайный факт"""
        data = await self._make_request(settings.RANDOM_FACTS_API)
        return data.get("text") if data else None
    
    async def get_age_prediction(self, name: str) -> Optional[Dict]:
        """Предсказать возраст по имени"""
        params = {"name": name}
        data = await self._make_request(settings.AGIFY_API, params)
        return data if data and data.get("age") else None
    
    async def get_gender_prediction(self, name: str) -> Optional[Dict]:
        """Предсказать пол по имени"""
        params = {"name": name}
        data = await self._make_request(settings.GENDERIZE_API, params)
        return data if data and data.get("gender") else None