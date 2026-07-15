import logging
import time
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import config

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)
BOOT_TIME = time.time()

# MongoDB connection
if config.MONGO_URL:
    mongo = MongoCli(config.MONGO_URL)
    db = mongo.SpicyBot
else:
    mongo = None
    db = None


class BotClient(Client):
    def __init__(self):
        super().__init__(
            name="SPICYBOT",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + (" " + self.me.last_name if self.me.last_name else "")
        self.username = self.me.username
        self.mention = self.me.mention
        LOGGER.info(f"✅ Bot started as @{self.username}")

    async def stop(self):
        await super().stop()
        LOGGER.info("❌ Bot stopped")


bot = BotClient()
