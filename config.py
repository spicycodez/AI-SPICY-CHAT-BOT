"""
config.py — Saari settings aur .env variables yahan se load hote hain.
Kuch bhi change karna ho (bot ka naam, memory limit, AI model) toh .env file edit karo,
is file ko touch karne ki zarurat nahi.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials — https://my.telegram.org se milte hain
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

# @BotFather se bana bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Optional: Assistant/Userbot session string (generate_session.py se banao)
# Khali chhod do agar sirf normal bot chahiye, assistant nahi
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Groq API key (free) — https://console.groq.com se lo
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# openai/gpt-oss-20b = fast + free-tier friendly (default)
# openai/gpt-oss-120b = zyada smart replies, thoda slower
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Persona ka naam — isse .env mein change kar sakte ho
BOT_NAME = os.getenv("BOT_NAME", "Pari")

# Optional — /start aur "thanks for adding me" panels ki banner image
# (public image URL ya container ke andar ka local file path). Khali chhod do
# agar image nahi chahiye — sirf text panel chalega.
START_IMG = os.getenv("START_IMG", "")

# Har chat mein kitne purane messages yaad rakhe (conversation context ke liye)
MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "10"))

# MongoDB connection URL (optional but required for broadcast persistence)
MONGO_URL = os.getenv("MONGO_URL", "")

# SUDO users (comma separated list of Telegram user IDs). Example: "12345,67890"
SUDO_USERS = set()
_sudo_raw = os.getenv("SUDO_USERS", "")
if _sudo_raw:
    try:
        SUDO_USERS = set(int(x.strip()) for x in _sudo_raw.split(",") if x.strip())
    except ValueError:
        print("WARNING: SUDO_USERS contains non-integer values; ignoring them.")


def validate():
    """Zaroori env vars check karta hai, missing hone par clear error deta hai."""
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
        print("❌ .env file mein ye missing hai:", ", ".join(missing))
        print("   .env.example ko copy karke .env banao aur values bharo.")
        raise SystemExit(1)
