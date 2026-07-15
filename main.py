"""
main.py — Bot yahan se start hota hai.

Chalane ka tareeka:
    python main.py
"""
import asyncio
from pyrogram import idle

import config
from bot.core.clients import bot, assistant, self_ids, bot_info

# Ye imports zaroori hain — inke andar @bot.on_message / @assistant.on_message
# decorators hain jo handlers register karte hain. Import na kiya toh commands,
# chat, aur welcome — teeno kaam nahi karenge.
import bot.plugins.commands  # noqa: F401
import bot.plugins.chat  # noqa: F401
import bot.plugins.welcome  # noqa: F401


async def main():
    config.validate()

    await bot.start()
    me = await bot.get_me()
    self_ids[bot] = me.id
    bot_info["username"] = me.username
    print(f"✅ [BOT] Logged in as @{me.username}")

    if assistant:
        await assistant.start()
        a_me = await assistant.get_me()
        self_ids[assistant] = a_me.id
        print(f"✅ [ASSISTANT] Logged in as {a_me.first_name} (id: {a_me.id})")
    else:
        print("ℹ️  [ASSISTANT] SESSION_STRING set nahi hai — sirf normal bot chalega.")

    print("\n🎉 Sab ready hai! Ctrl+C dabakar band kar sakte ho.\n")
    await idle()

    await bot.stop()
    if assistant:
        await assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
