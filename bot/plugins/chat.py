"""
chat.py — Yahi asli "flirty AI chat" wala logic hai.

Rules:
- Private (DM) mein: har text message ka AI reply milega
- Group mein: sirf tab reply milega jab bot/assistant ko @mention kiya ho
  ya uske kisi message pe reply kiya ho

Ye function `bot` aur `assistant` (agar configured hai) — dono client pe
lagta hai, isliye ek hi jagah logic likha hai aur dono ise reuse karte hain.
"""
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
    if not message.text or message.text.startswith("/"):
        return

    my_id = self_ids.get(client)
    if not my_id:
        return  # client abhi fully start nahi hua

    if message.chat.type == ChatType.PRIVATE:
        should_reply = True
    else:
        replied_to_me = bool(
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == my_id
        )
        should_reply = bool(message.mentioned or replied_to_me)

    if not should_reply:
        return

    user_name = message.from_user.first_name if message.from_user else "Someone"

    try:
        await client.send_chat_action(message.chat.id, "typing")
    except Exception:
        pass

    # register chat in MongoDB (best-effort)
    if register_chat:
        try:
            chat_type = message.chat.type.value if hasattr(message.chat.type, "value") else str(message.chat.type)
            title = getattr(message.chat, "title", None)
            username = getattr(message.from_user, "username", None)
            await register_chat(message.chat.id, chat_type, title, username)
        except Exception:
            pass

    reply_text = await get_ai_reply(message.chat.id, user_name, message.text)
    await message.reply_text(reply_text)


@bot.on_message(filters.text)
async def bot_chat_handler(client, message: Message):
    await _process(client, message)


if assistant:
    @assistant.on_message(filters.text)
    async def assistant_chat_handler(client, message: Message):
        await _process(client, message)
