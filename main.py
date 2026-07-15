"""
main.py — Bot yahan se start hota hai.

Chalane ka tareeka:
    python main.py
"""
import asyncio
from pyrogram import idle

import config
from bot.core import clients as clients  # import module namespace to avoid name collision

# Ye imports zaroori hain — inke andar @bot.on_message / @assistant.on_message
# decorators hain jo handlers register karte hain. Import na kiya toh commands,
# chat, aur welcome — teeno kaam nahi karenge.
import bot.plugins.commands  # noqa: F401
import bot.plugins.chat  # noqa: F401
import bot.plugins.welcome  # noqa: F401
import bot.plugins.broadcast  # noqa: F401  # broadcast plugin


async def main():
    config.validate()

    await clients.bot.start()
    me = await clients.bot.get_me()
    clients.self_ids[clients.bot] = me.id
    clients.bot_info["username"] = me.username
    print(f"✅ [BOT] Logged in as @{me.username}")

    if clients.assistant:
        await clients.assistant.start()
        a_me = await clients.assistant.get_me()
        clients.self_ids[clients.assistant] = a_me.id
        print(f"✅ [ASSISTANT] Logged in as {a_me.first_name} (id: {a_me.id})")
    else:
        print("ℹ️  [ASSISTANT] SESSION_STRING set nahi hai — sirf normal bot chalega.")

    print("\n🎉 Sab ready hai! Ctrl+C dabakar band kar sakte ho.\n")
    await idle()

    await clients.bot.stop()
    if clients.assistant:
        await clients.assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
