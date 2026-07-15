"""
keyboards.py — Saare inline buttons yahan define hote hain. Button add/hatana
ho, bas yahi file edit karo.
"""
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.core.clients import bot_info


def _add_to_group_url() -> str:
    username = bot_info.get("username")
    return f"https://t.me/{username}?startgroup=true" if username else "https://t.me"


def _dm_url() -> str:
    username = bot_info.get("username")
    return f"https://t.me/{username}?start=fromgroup" if username else "https://t.me"


def start_private_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Your Group", url=_add_to_group_url())],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("🔄 Reset", callback_data="reset"),
        ],
    ])


def start_group_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Message Me Privately", url=_dm_url())],
    ])


def thanks_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("➕ Add To Another Group", url=_add_to_group_url()),
        ],
    ])
