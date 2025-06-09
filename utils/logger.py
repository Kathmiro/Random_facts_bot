import logging
import os
from config.settings import settings

def setup_logger():
    # Создаем директорию для логов если её нет
    os.makedirs("logs", exist_ok=True)
    
    # Настройка логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logger()