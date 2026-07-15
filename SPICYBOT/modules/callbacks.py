from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from SPICYBOT import bot


@bot.on_callback_query(filters.regex("help_btn"))
async def help_callback(client: Client, callback_query: CallbackQuery):
    """Handle help button callback"""
    help_text = """**Help - SpicyBot**

📋 **Commands:**
/start - Start menu
/help - This message
/reset - Clear memory

💬 **Usage:**
→ Tag me in groups
→ Reply to me
→ DM me anytime
"""
    await callback_query.answer()
    await callback_query.edit_message_text(help_text)


@bot.on_callback_query(filters.regex("reset_btn"))
async def reset_callback(client: Client, callback_query: CallbackQuery):
    """Handle reset button callback"""
    from SPICYBOT.utils.ai import clear_history
    clear_history(callback_query.message.chat.id)
    await callback_query.answer("✅ Chat memory cleared!")
    await callback_query.edit_message_text("✅ Chat cleared!")
