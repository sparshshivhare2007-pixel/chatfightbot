import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Telegram Credentials
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")

# =========================
# Database
# =========================

MONGO_URI = os.getenv("MONGO_URI")

# =========================
# Optional Services
# =========================

REDIS_URL = os.getenv("REDIS_URL", None)

# =========================
# Validation (Safe Startup)
# =========================

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env")

if not API_ID:
    raise ValueError("API_ID is missing in .env")

if not API_HASH:
    raise ValueError("API_HASH is missing in .env")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing in .env")
