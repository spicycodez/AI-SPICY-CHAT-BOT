"""
bot/db/mongo.py
Async Mongo helper for chat registry and broadcast logs.
Requires MONGO_URL in env (config.MONGO_URL).
"""
import datetime
from typing import Optional

import motor.motor_asyncio
import config

_client = None
_db = None


def _get_client():
    global _client, _db
    if _client is None:
        if not config.MONGO_URL:
            raise RuntimeError("MONGO_URL not configured")
        _client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URL)
        try:
            _db_name = _client.get_default_database().name
        except Exception:
            _db_name = "flirtybot"
        _db = _client[_db_name]
    return _db


async def register_chat(chat_id: int, chat_type: str, title: Optional[str], username: Optional[str]):
    db = _get_client()
    now = datetime.datetime.utcnow()
    await db.chats.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "chat_type": chat_type,
            "title": title,
            "username": username,
            "last_seen": now
        }, "$setOnInsert": {"first_seen": now}},
        upsert=True
    )


async def list_chats(chat_type: Optional[str] = None):
    db = _get_client()
    q = {}
    if chat_type:
        q["chat_type"] = chat_type
    cursor = db.chats.find(q)
    return [doc async for doc in cursor]


async def add_broadcast_log(sender_id: int, text: str, to_count: int, flags: dict):
    db = _get_client()
    doc = {
        "sender_id": sender_id,
        "text": text,
        "to_count": to_count,
        "flags": flags,
        "created_at": datetime.datetime.utcnow()
    }
    res = await db.broadcasts.insert_one(doc)
    return res.inserted_id
