"""
commands.py — /start, /help, /reset commands + unke inline button callbacks.
/start ka panel private aur group mein alag hota hai (dono photo + caption +
buttons ke sath, agar START_IMG configured hai).

Ye sirf `bot` (BotFather) client pe kaam karte hain — assistant sirf chat karta hai,
commands ka kaam bot ka hai.
"""
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType

from bot.core.clients import bot
from bot.utils.memory import clear_history
from bot.ui.texts import start_private_text, start_group_text, help_text
from bot.ui.keyboards import start_private_keyboard, start_group_keyboard
from config import START_IMG


async def _send_start_panel(client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        name = message.from_user.first_name if message.from_user else "there"
        text = start_private_text(name)
        keyboard = start_private_keyboard()
    else:
        text = start_group_text()
        keyboard = start_group_keyboard()

    if START_IMG:
        try:
            await client.send_photo(message.chat.id, START_IMG, caption=text, reply_markup=keyboard)
            return
        except Exception as e:
            print(f"[START_IMG ERROR] {e} — text-only pe fallback ho raha hai")

    await client.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await _send_start_panel(client, message)


@bot.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text(help_text())


@bot.on_message(filters.command("reset"))
async def reset_cmd(client, message: Message):
    clear_history(message.chat.id)
    await message.reply_text("Theek hai, sab bhool gayi 🙈 Fresh start karte hain!")


@bot.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply_text(help_text())


@bot.on_callback_query(filters.regex("^reset$"))
async def reset_callback(client, callback_query: CallbackQuery):
    clear_history(callback_query.message.chat.id)
    await callback_query.answer("Memory clear ho gayi! 🙈", show_alert=True)
