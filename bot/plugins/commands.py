"""
commands.py — /start, /help, /reset commands + unke inline button callbacks.
/start ka panel private aur group mein alag hota hai (dono photo + caption +
buttons ke sath, agar START_IMG configured hai).

Ye sirf `bot` (BotFather) client pe kaam karte hain — assistant sirf chat karta hai,
commands ka kaam bot ka hai.
"""
import sys
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType

from bot.utils.memory import clear_history
from bot.ui.texts import start_private_text, start_group_text, help_text
from bot.ui.keyboards import start_private_keyboard, start_group_keyboard
from config import START_IMG


async def _send_start_panel(client, message: Message):
    print(f"[START] _send_start_panel called from {message.from_user.first_name}", flush=True)
    print(f"[START] Chat type: {message.chat.type}", flush=True)
    
    if message.chat.type == ChatType.PRIVATE:
        name = message.from_user.first_name if message.from_user else "there"
        text = start_private_text(name)
        keyboard = start_private_keyboard()
        print(f"[START] Private chat - generating start panel for {name}", flush=True)
    else:
        text = start_group_text()
        keyboard = start_group_keyboard()
        print(f"[START] Group chat - generating start panel", flush=True)

    if START_IMG:
        print(f"[START] Trying to send photo with START_IMG: {START_IMG}", flush=True)
        try:
            await client.send_photo(message.chat.id, START_IMG, caption=text, reply_markup=keyboard)
            print(f"[START] ✅ Photo sent successfully", flush=True)
            return
        except Exception as e:
            print(f"[START] Photo send failed: {type(e).__name__}: {str(e)}", flush=True)
            import traceback
            traceback.print_exc(file=sys.stdout)

    print(f"[START] Sending text message", flush=True)
    await client.send_message(message.chat.id, text, reply_markup=keyboard)
    print(f"[START] ✅ Message sent successfully", flush=True)


async def start_cmd(client, message: Message):
    print(f"[COMMAND] /start command received from {message.from_user.first_name if message.from_user else 'UNKNOWN'}", flush=True)
    try:
        await _send_start_panel(client, message)
    except Exception as e:
        error_msg = f"[START ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
        try:
            await message.reply_text(f"❌ Error: {str(e)}")
        except:
            pass


async def help_cmd(client, message: Message):
    print(f"[COMMAND] /help command received", flush=True)
    try:
        help_text_msg = help_text()
        await message.reply_text(help_text_msg)
        print(f"[COMMAND] ✅ Help message sent", flush=True)
    except Exception as e:
        error_msg = f"[HELP ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)


async def reset_cmd(client, message: Message):
    print(f"[COMMAND] /reset command received", flush=True)
    try:
        clear_history(message.chat.id)
        await message.reply_text("Theek hai, sab bhool gayi 🙈 Fresh start karte hain!")
        print(f"[COMMAND] ✅ Reset done", flush=True)
    except Exception as e:
        error_msg = f"[RESET ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)


async def help_callback(client, callback_query: CallbackQuery):
    print(f"[CALLBACK] help button clicked", flush=True)
    try:
        await callback_query.answer()
        help_text_msg = help_text()
        await callback_query.message.reply_text(help_text_msg)
        print(f"[CALLBACK] ✅ Help callback done", flush=True)
    except Exception as e:
        error_msg = f"[CALLBACK ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)


async def reset_callback(client, callback_query: CallbackQuery):
    print(f"[CALLBACK] reset button clicked", flush=True)
    try:
        clear_history(callback_query.message.chat.id)
        await callback_query.answer("Memory clear ho gayi! 🙈", show_alert=True)
        print(f"[CALLBACK] ✅ Reset callback done", flush=True)
    except Exception as e:
        error_msg = f"[CALLBACK ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
