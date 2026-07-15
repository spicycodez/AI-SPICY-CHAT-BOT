from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from SPICYBOT import bot, config, LOGGER
from SPICYBOT.utils.ai import get_ai_response


@bot.on_message(
    filters.text &
    ~filters.private &
    ~filters.bot &
    (filters.reply_to(bot.id) | filters.mentioned)
)
async def group_chat_handler(client: Client, message: Message):
    """Handle messages in groups (when replied to or mentioned)"""
    try:
        async with client.action(message.chat.id, ChatAction.TYPING):
            response = await get_ai_response(message.text, message.chat.id)
            await message.reply_text(response)
    except Exception as e:
        LOGGER.error(f"Error in group chat: {e}")
        await message.reply_text("❌ Sorry, something went wrong!")


@bot.on_message(
    filters.text &
    filters.private &
    ~filters.bot
)
async def private_chat_handler(client: Client, message: Message):
    """Handle messages in private chat"""
    try:
        async with client.action(message.chat.id, ChatAction.TYPING):
            response = await get_ai_response(message.text, message.chat.id)
            await message.reply_text(response)
    except Exception as e:
        LOGGER.error(f"Error in private chat: {e}")
        await message.reply_text("❌ Sorry, something went wrong!")
