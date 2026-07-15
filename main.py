"""
main.py — Bot yahan se start hota hai.

Chalane ka tareeka:
    python main.py
"""
import asyncio
import sys
from pyrogram import idle

import config
from bot.core import clients as clients  # import module namespace to avoid name collision

print("[MAIN] Starting bot imports...", flush=True)

# Ye imports zaroori hain — inke andar @bot.on_message / @assistant.on_message
# decorators hain jo handlers register karte hain. Import na kiya toh commands,
# chat, aur welcome — teeno kaam nahi karenge.
try:
    import bot.plugins.commands  # noqa: F401
    print("[MAIN] ✅ commands plugin loaded", flush=True)
except Exception as e:
    print(f"[MAIN] ❌ commands plugin FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc(file=sys.stdout)

try:
    import bot.plugins.chat  # noqa: F401
    print("[MAIN] ✅ chat plugin loaded", flush=True)
except Exception as e:
    print(f"[MAIN] ❌ chat plugin FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc(file=sys.stdout)

try:
    import bot.plugins.welcome  # noqa: F401
    print("[MAIN] ✅ welcome plugin loaded", flush=True)
except Exception as e:
    print(f"[MAIN] ❌ welcome plugin FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc(file=sys.stdout)

try:
    import bot.plugins.broadcast  # noqa: F401
    print("[MAIN] ✅ broadcast plugin loaded", flush=True)
except Exception as e:
    print(f"[MAIN] ❌ broadcast plugin FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc(file=sys.stdout)


async def main():
    try:
        config.validate()
        print("[MAIN] ✅ Config validation passed", flush=True)

        await clients.bot.start()
        me = await clients.bot.get_me()
        clients.self_ids[clients.bot] = me.id
        clients.bot_info["username"] = me.username
        print(f"[MAIN] ✅ [BOT] Logged in as @{me.username}", flush=True)

        if clients.assistant:
            await clients.assistant.start()
            a_me = await clients.assistant.get_me()
            clients.self_ids[clients.assistant] = a_me.id
            print(f"[MAIN] ✅ [ASSISTANT] Logged in as {a_me.first_name} (id: {a_me.id})", flush=True)
        else:
            print("[MAIN] ℹ️  [ASSISTANT] SESSION_STRING set nahi hai — sirf normal bot chalega.", flush=True)

        print("\n[MAIN] 🎉 Sab ready hai! Waiting for messages...\n", flush=True)
        await idle()

        await clients.bot.stop()
        if clients.assistant:
            await clients.assistant.stop()
    
    except Exception as e:
        print(f"[MAIN] ❌ ERROR: {type(e).__name__}: {str(e)}", flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
        raise


if __name__ == "__main__":
    asyncio.run(main())
