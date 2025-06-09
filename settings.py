import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # API URLs
    CAT_FACTS_API = "https://catfact.ninja/fact"
    JOKE_API = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    RANDOM_FACTS_API = "https://uselessfacts.jsph.pl/random.json?language=en"
    AGIFY_API = "https://api.agify.io"
    GENDERIZE_API = "https://api.genderize.io"
    
    # Cache settings
    CACHE_TTL = 300  # 5 minutes
    
    # Rate limiting
    RATE_LIMIT = 1  # requests per second
    
    # File paths
    USERS_FILE = "storage/users.json"
    LOG_FILE = "logs/bot.log"

settings = Settings()