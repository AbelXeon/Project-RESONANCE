import logging
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, VIVI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# In-memory history per chat_id
_history = {}
MAX_TURNS = 10


def get_history(chat_id: int):
    if chat_id not in _history:
        _history[chat_id] = []
    return _history[chat_id]


def ask_vivi(chat_id: int, user_text: str) -> str:
    history = get_history(chat_id)
    history.append({"role": "user", "text": user_text})

    # Prepare chat history turns for Gemini
    contents = []
    for msg in history[-MAX_TURNS:]:
        contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["text"])],
            )
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=VIVI_SYSTEM_PROMPT,
                temperature=0.7,
            ),
        )

        reply = response.text or "I'm not sure how to respond to that."
        history.append({"role": "model", "text": reply})
        return reply

    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}", exc_info=True)
        return "Sorry, I hit a snag processing that. Can you try again?"