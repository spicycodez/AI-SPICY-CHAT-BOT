import asyncio
import importlib
from pyrogram import idle
from SPICYBOT import LOGGER, bot, config
from SPICYBOT.modules import ALL_MODULES


async def boot():
    try:
        config.validate()
        LOGGER.info("✅ Configuration validated")
        
        await bot.start()
        
        # Load all modules
        for module in ALL_MODULES:
            try:
                importlib.import_module(f"SPICYBOT.modules.{module}")
                LOGGER.info(f"✅ Module loaded: {module}")
            except Exception as e:
                LOGGER.error(f"❌ Failed to load {module}: {e}")
        
        LOGGER.info("\n🎉 Bot is running! Waiting for messages...\n")
        await idle()
        
        await bot.stop()
    
    except Exception as e:
        LOGGER.error(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(boot())
