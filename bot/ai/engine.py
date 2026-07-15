"""
engine.py — Groq API ko call karke AI response generate karta hai.
Kisi aur provider (OpenAI/Gemini) pe switch karna ho toh bas yahi file badalni hogi,
baaki poora bot untouched rahega.
"""
import sys
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
        print(f"[AI] Calling Groq API with model: {GROQ_MODEL}", flush=True)
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.9,
            max_completion_tokens=200,
        )
        reply = completion.choices[0].message.content.strip()
        print(f"[AI] ✅ Reply generated successfully", flush=True)
    except Exception as e:
        error_msg = f"[AI ERROR] {type(e).__name__}: {str(e)}"
        print(error_msg, flush=True)
        import traceback
        traceback.print_exc(file=sys.stdout)
        reply = "Ek second... mera dimaag thoda hang ho gaya 🙈 phir se try karo?"

    add_message(chat_id, "user", f"{user_name}: {user_text}")
    add_message(chat_id, "assistant", reply)

    return reply
