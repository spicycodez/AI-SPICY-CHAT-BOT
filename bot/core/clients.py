"""
clients.py — Dono Pyrogram clients yahan define hote hain:

1. `bot`       -> Normal bot (BotFather token). Commands (/start, /help, /reset)
                  aur tag/reply pe chat, dono isi se hote hain.
2. `assistant` -> Optional userbot (SESSION_STRING se). Agar .env mein
                  SESSION_STRING set hai, ye bhi tag/reply pe chat karega —
                  bas iske paas "BOT" tag nahi dikhega, real account jaisa lagega
                  (bilkul AnonXMusic ke "assistant" jaisa concept, par yahan
                  music ki jagah chatting ke liye use ho raha hai).
"""
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# in_memory=True: koi .session file disk pe nahi banti, sirf RAM mein rehti hai.
# Ye zaroori hai kyunki Heroku ka filesystem ephemeral hai (har restart/redeploy pe
# wipe ho jaata hai) — BOT_TOKEN aur SESSION_STRING already har start pe poora
# re-authenticate kar dete hain, isliye local session file ki zarurat hi nahi.
bot = Client(
    "flirty_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

assistant = None
if SESSION_STRING:
    assistant = Client(
        "flirty_assistant",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        in_memory=True,
    )

# client object -> apni khud ki Telegram user id (main.py start hone ke baad bharta hai)
self_ids = {}

# Bot ka username — deep-link buttons (Add to Group, DM me) banane ke liye
# main.py start hone ke baad bharta hai
bot_info = {"username": None}
