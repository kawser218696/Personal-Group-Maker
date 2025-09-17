import os
from dotenv import load_dotenv

load_dotenv()

# Bot API
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Redis (for storing multiple accounts)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# API credentials (for your primary account)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")