"""
engine.py — Groq API ko call karke AI response generate karta hai.
Kisi aur provider (OpenAI/Gemini) pe switch karna ho toh bas yahi file badalni hogi,
baaki poora bot untouched rahega.
"""
from groq import AsyncGroq
from config import GROQ_API_KEY, GROQ_MODEL
from bot.ai.persona import SYSTEM_PROMPT
from bot.utils.memory import get_history, add_message

client = AsyncGroq(api_key=GROQ_API_KEY)


async def get_ai_reply(chat_id: int, user_name: str, user_text: str) -> str:
    """Chat history + persona ke sath Groq ko bhejta hai, AI ka reply string return karta hai."""
    history = get_history(chat_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": f"{user_name}: {user_text}"})

    try:
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.9,
            max_completion_tokens=200,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[AI ERROR] {e}")
        reply = "Ek second... mera dimaag thoda hang ho gaya 🙈 phir se try karo?"

    add_message(chat_id, "user", f"{user_name}: {user_text}")
    add_message(chat_id, "assistant", reply)

    return reply
