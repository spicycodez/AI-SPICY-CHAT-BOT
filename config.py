import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Groq API key (free) — https://console.groq.com
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

# Bot persona configuration
BOT_NAME = os.getenv("BOT_NAME", "Pari")
MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "10"))

# MongoDB connection URL (optional but required for broadcast/storage)
MONGO_URL = os.getenv("MONGO_URL", "")

# Optional — Assistant/Userbot session string
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Start panel image
START_IMG = os.getenv("START_IMG", "")

# SUDO users
SUDO_USERS = set()
_sudo_raw = os.getenv("SUDO_USERS", "")
if _sudo_raw:
    try:
        SUDO_USERS = set(int(x.strip()) for x in _sudo_raw.split(",") if x.strip())
    except ValueError:
        print("WARNING: SUDO_USERS contains non-integer values; ignoring them.")


def validate():
    """Validate required environment variables"""
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if missing:
        print("❌ Missing required environment variables:", ", ".join(missing))
        print("   Copy .env.example to .env and fill in the values.")
        raise SystemExit(1)
