from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SPICYBOT import bot, config, LOGGER


@bot.on_message(filters.new_chat_members)
async def welcome_handler(client: Client, message):
    """Welcome new members when bot is added"""
    for member in message.new_chat_members:
        if member.id == client.me.id:
            buttons = [
                [
                    InlineKeyboardButton(
                        "❓ Help",
                        callback_data="help_btn"
                    )
                ]
            ]
            
            welcome_text = f"""Thanks for adding me! 🎉

I'm {config.BOT_NAME}, your AI chat bot!

**Just tag me or reply to my messages** to chat with AI.

Enjoy! ✨
"""
            
            if config.START_IMG:
                try:
                    await message.reply_photo(
                        config.START_IMG,
                        caption=welcome_text,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except Exception as e:
                    LOGGER.error(f"Error sending welcome photo: {e}")
                    await message.reply_text(
                        welcome_text,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
            else:
                await message.reply_text(
                    welcome_text,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            LOGGER.info(f"Bot added to {message.chat.title}")
