"""
chat.py — Yahi asli "flirty AI chat" wala logic hai.

Rules:
- Private (DM) mein: har text message ka AI reply milega
- Group mein: sirf tab reply milega jab bot/assistant ko @mention kiya ho
  ya uske kisi message pe reply kiya ho

Ye function `bot` aur `assistant` (agar configured hai) — dono client pe
lagta hai, isliye ek hi jagah logic likha hai aur dono ise reuse karte hain.
"""
import sys
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

from bot.core.clients import bot, assistant, self_ids
from bot.ai.engine import get_ai_reply

# optional DB registration helper
try:
    from bot.db.mongo import register_chat
except Exception:
    register_chat = None


async def _process(client, message: Message):
    print(f"[CHAT] Message received: {message.text[:50] if message.text else 'NO TEXT'}", flush=True)
    
    if not message.text or message.text.startswith("/"):
        print(f"[CHAT] Skipping: no text or is command", flush=True)
        return

    my_id = self_ids.get(client)
    print(f"[CHAT] my_id: {my_id}, chat_type: {message.chat.type}", flush=True)
    
    if not my_id:
        print(f"[CHAT] Skipping: client not fully started", flush=True)
        return  # client abhi fully start nahi hua

    if message.chat.type == ChatType.PRIVATE:
        should_reply = True
        print(f"[CHAT] Private chat - should_reply=True", flush=True)
    else:
        replied_to_me = bool(
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == my_id
        )
        should_reply = bool(message.mentioned or replied_to_me)
        print(f"[CHAT] Group chat - mentioned={message.mentioned}, replied_to_me={replied_to_me}, should_reply={should_reply}", flush=True)

    if not should_reply:
        print(f"[CHAT] Skipping: should_reply is False", flush=True)
        return

    user_name = message.from_user.first_name if message.from_user else "Someone"
    print(f"[CHAT] Processing message from {user_name}: {message.text}", flush=True)

    try:
        await client.send_chat_action(message.chat.id, "typing")
        print(f"[CHAT] Typing indicator sent", flush=True)
    except Exception as e:
        print(f"[CHAT] Typing indicator failed: {e}", flush=True)
        pass

    # register chat in MongoDB (best-effort)
    if register_chat:
        try:
            chat_type = message.chat.type.value if hasattr(message.chat.type, "value") else str(message.chat.type)
            title = getattr(message.chat, "title", None)
            username = getattr(message.from_user, "username", None)
            await register_chat(message.chat.id, chat_type, title, username)
            print(f"[CHAT] Chat registered in MongoDB", flush=True)
        except Exception as e:
            print(f"[CHAT] MongoDB registration failed: {e}", flush=True)
            pass

    try:
        print(f"[CHAT] Calling get_ai_reply...", flush=True)
        reply_text = await get_ai_reply(message.chat.id, user_name, message.text)
        print(f"[CHAT] Got reply: {reply_text[:50]}", flush=True)
        await message.reply_text(reply_text)
        print(f"[CHAT] ✅ Reply sent successfully", flush=True)
    except Exception as e:
        error_msg = f"[CHAT ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
        raise


@bot.on_message(filters.text)
async def bot_chat_handler(client, message: Message):
    print(f"[HANDLER] bot_chat_handler triggered", flush=True)
    await _process(client, message)


if assistant:
    @assistant.on_message(filters.text)
    async def assistant_chat_handler(client, message: Message):
        print(f"[HANDLER] assistant_chat_handler triggered", flush=True)
        await _process(client, message)
