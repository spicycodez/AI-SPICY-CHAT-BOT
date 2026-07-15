"""
welcome.py — Jab bot ko kisi naye group mein add kiya jaata hai, thank-you
panel (photo + caption + buttons) bhejta hai.

Note: Agar koi is bot ko `?startgroup=true` deep-link se add karta hai, Telegram
khud bhi ek /start bhej sakta hai us group mein — us case mein ye thank-you
message aur group ka /start panel dono aa sakte hain, thoda overlap ho sakta
hai. Abhi ke liye ye theek hai, chaho toh baad mein dedupe kar sakte ho.
"""
from pyrogram import filters
from pyrogram.types import Message

from bot.core.clients import bot, self_ids
from bot.ui.texts import thanks_for_adding_text
from bot.ui.keyboards import thanks_keyboard
from config import START_IMG


@bot.on_message(filters.new_chat_members)
async def welcomed_to_group(client, message: Message):
    my_id = self_ids.get(client)
    if not my_id or not message.new_chat_members:
        return

    added_me = any(user.id == my_id for user in message.new_chat_members)
    if not added_me:
        return  # koi normal member join hua hai, bot nahi — ignore

    text = thanks_for_adding_text(message.chat.title or "this group")
    keyboard = thanks_keyboard()

    if START_IMG:
        try:
            await client.send_photo(message.chat.id, START_IMG, caption=text, reply_markup=keyboard)
            return
        except Exception as e:
            print(f"[START_IMG ERROR] {e} — text-only pe fallback ho raha hai")

    await client.send_message(message.chat.id, text, reply_markup=keyboard)
