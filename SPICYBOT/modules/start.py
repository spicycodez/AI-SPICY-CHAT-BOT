from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from SPICYBOT import bot, config, LOGGER


@bot.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    """Handle /start in private chat"""
    buttons = [
        [
            InlineKeyboardButton(
                "💬 Add to Group",
                url=f"https://t.me/{bot.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help_btn"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Reset Chat",
                callback_data="reset_btn"
            )
        ]
    ]
    
    text = f"""Hey! 👋 I'm {config.BOT_NAME}

I'm an AI-powered chat bot running on **Groq API** (completely free!).

**What I can do:**
✨ Reply to your messages with AI
🧠 Remember conversation context
🎨 Work in groups and DMs
⚡ Lightning-fast responses

Tag me in a group or message me here!
"""
    
    if config.START_IMG:
        try:
            await message.reply_photo(
                config.START_IMG,
                caption=text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            LOGGER.error(f"Error sending photo: {e}")
            await message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    else:
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@bot.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    """Handle /start in group chat"""
    buttons = [
        [
            InlineKeyboardButton(
                "💬 DM",
                url=f"https://t.me/{bot.username}?start=dm"
            ),
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help_btn"
            )
        ]
    ]
    
    text = f"""Thanks for adding me! 👋

I'm {config.BOT_NAME}, your AI chat companion!

**How to use me:**
→ Reply to my messages
→ Tag me: @{bot.username}
→ Just chat naturally!
"""
    
    if config.START_IMG:
        try:
            await message.reply_photo(
                config.START_IMG,
                caption=text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            LOGGER.error(f"Error sending photo: {e}")
            await message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    else:
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@bot.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    """Handle /help command"""
    help_text = f"""**Help - {config.BOT_NAME}**

📋 **Available Commands:**
/start - Show start menu
/help - Show this message
/reset - Clear conversation memory

💬 **How to chat:**
→ In groups: Tag me or reply to my messages
→ In DM: Just type normally
→ I'll use AI (Groq) to generate responses

🤖 **Powered by:** Groq API (Free)
"""
    await message.reply_text(help_text)


@bot.on_message(filters.command("reset"))
async def reset_cmd(client: Client, message: Message):
    """Handle /reset command"""
    from SPICYBOT.utils.ai import clear_history
    clear_history(message.chat.id)
    await message.reply_text("✅ Chat memory cleared!")
