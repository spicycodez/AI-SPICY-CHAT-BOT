"""
broadcast.py — /broadcast command for admins (SUDO_USERS).
Usage examples:
 - Reply to a message and run: /broadcast -assistant -pin -forward
 - /broadcast -user Hello everyone!
Flags:
 - -user     : send only to private users (those who started the bot)
 - -assistant: send from assistant account (so messages look like normal user messages)
 - -pin     : pin the sent message in the destination chat (if bot has permission)
 - -pinloud : pin + notify (if permitted)
 - -forward : if command was a reply to a message, forward that message instead of sending text
 - -nofwd   : explicit no forward, send text always
"""
import asyncio
from pyrogram import filters
from pyrogram.types import Message

from bot.core.clients import bot, assistant
import config

try:
    from bot.db.mongo import list_chats, add_broadcast_log
except Exception:
    list_chats = None
    add_broadcast_log = None

BATCH_SLEEP = 0.05  # seconds between sends to avoid flood limits


def _is_sudo(user_id: int):
    return user_id in config.SUDO_USERS


@bot.on_message(filters.command("broadcast"))
async def broadcast_cmd(client, message: Message):
    if not message.from_user or not _is_sudo(message.from_user.id):
        await message.reply_text("❌ Aapko ye karne ki permission nahi hai.")
        return

    # parse tokens and flags
    tokens = message.text.split()
    flags = set(t.lower() for t in tokens[1:] if t.startswith("-"))
    # message payload: prefer replied message text (if not forwarding) or text after flags
    text_payload = None
    # compute text after flags (non-flag tokens)
    nonflag_tokens = [t for t in tokens[1:] if not t.startswith("-")]
    if nonflag_tokens:
        text_payload = " ".join(nonflag_tokens)

    # If the command was a reply and no nonflag text, prefer replied message's text/media
    is_reply = bool(message.reply_to_message)
    use_forward = ("-forward" in flags) or (is_reply and "-nofwd" not in flags and not text_payload)

    # choose destinations
    target_type = None
    if "-user" in flags:
        target_type = "private"

    # choose sending client
    send_client = bot
    if "-assistant" in flags:
        if not assistant:
            await message.reply_text("❌ Assistant session configured nahi hai.")
            return
        send_client = assistant

    # collect target chats
    if list_chats is None:
        await message.reply_text("❌ MongoDB not configured or DB helper missing; cannot get chat list.")
        return

    chats = await list_chats(chat_type=target_type)
    if not chats:
        await message.reply_text("ℹ️ Koi chats nahi mile DB mein.")
        return

    total = 0
    # perform broadcast (best-effort)
    for doc in chats:
        chat_id = doc.get("chat_id")
        try:
            if use_forward and is_reply:
                # forward replied message
                await send_client.forward_messages(chat_id, message.chat.id, message.reply_to_message.message_id)
                sent = None
            else:
                # text payload fallback: if replied message and text_payload empty, try reply's text
                payload_text = text_payload
                if not payload_text and is_reply and message.reply_to_message.text:
                    payload_text = message.reply_to_message.text
                if not payload_text:
                    # nothing to send
                    continue
                sent = await send_client.send_message(chat_id, payload_text)
            # pin logic
            if "-pin" in flags and sent:
                try:
                    await send_client.pin_chat_message(chat_id, sent.message_id, disable_notification=("-pinloud" not in flags))
                except Exception:
                    pass
            total += 1
            await asyncio.sleep(BATCH_SLEEP)
        except Exception:
            # ignore per-chat errors to continue broadcast
            continue

    # log broadcast
    try:
        if add_broadcast_log:
            flags_dict = {f: True for f in flags}
            await add_broadcast_log(message.from_user.id, text_payload or "(forwarded message)", total, flags_dict)
    except Exception:
        pass

    await message.reply_text(f"✅ Broadcast complete. Sent to {total} chats.")
