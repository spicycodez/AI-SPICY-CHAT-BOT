"""
memory.py — Har group/DM ka short conversation history in-memory rakhta hai,
taaki AI ko pichle messages ka context mile aur reply natural lage.

Note: Ye memory RAM mein hai — bot restart hone par clear ho jaayegi.
Agar permanent memory chahiye (file/database mein), ye jagah hai usse plug karne ki.
"""
from collections import defaultdict, deque
from config import MEMORY_LIMIT

_chat_memory = defaultdict(lambda: deque(maxlen=MEMORY_LIMIT))


def get_history(chat_id: int) -> list:
    return list(_chat_memory[chat_id])


def add_message(chat_id: int, role: str, content: str) -> None:
    _chat_memory[chat_id].append({"role": role, "content": content})


def clear_history(chat_id: int) -> None:
    _chat_memory[chat_id].clear()
