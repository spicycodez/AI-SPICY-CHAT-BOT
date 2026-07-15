from groq import Groq
import config
from SPICYBOT import LOGGER

client = Groq(api_key=config.GROQ_API_KEY)

# Store conversation history
conversation_history = {}


async def get_ai_response(user_message: str, chat_id: int = None) -> str:
    """
    Get AI response using Groq API
    """
    try:
        # Initialize chat history if needed
        if chat_id and chat_id not in conversation_history:
            conversation_history[chat_id] = []
        
        # Add user message to history
        if chat_id:
            conversation_history[chat_id].append({
                "role": "user",
                "content": user_message
            })
            
            # Keep only last N messages
            if len(conversation_history[chat_id]) > config.MEMORY_LIMIT * 2:
                conversation_history[chat_id] = conversation_history[chat_id][-config.MEMORY_LIMIT * 2:]
            
            messages = conversation_history[chat_id]
        else:
            messages = [{"role": "user", "content": user_message}]
        
        # Create system prompt
        system_prompt = f"""You are {config.BOT_NAME}, a helpful, friendly, and witty AI chat bot.

Be concise, engaging, and natural in your responses.
Your personality is warm, helpful, and a bit playful.
Always be respectful and appropriate.
Keep responses under 500 characters when possible.
"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        
        ai_response = response.choices[0].message.content
        
        # Add assistant response to history
        if chat_id:
            conversation_history[chat_id].append({
                "role": "assistant",
                "content": ai_response
            })
        
        return ai_response
        
    except Exception as e:
        LOGGER.error(f"Error getting AI response: {e}")
        return f"❌ Error: {str(e)[:100]}"


def clear_history(chat_id: int):
    """Clear conversation history for a chat"""
    if chat_id in conversation_history:
        del conversation_history[chat_id]
        return True
    return False
