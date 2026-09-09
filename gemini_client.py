import logging
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from config import GEMINI_API_KEY, GEMINI_MODEL, VIVI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

# Fallback models in case the main one is overloaded (503)
MODELS_TO_TRY = [
    GEMINI_MODEL,
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
]

_history = {}
MAX_TURNS = 10


def get_history(chat_id: int):
    if chat_id not in _history:
        _history[chat_id] = []
    return _history[chat_id]


def ask_vivi(chat_id: int, user_text: str) -> str:
    history = get_history(chat_id)
    history.append({"role": "user", "text": user_text})

    contents = []
    for msg in history[-MAX_TURNS:]:
        contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["text"])],
            )
        )

    last_error = None

    # Loop through models if one is experiencing 503 high demand
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=VIVI_SYSTEM_PROMPT,
                    temperature=0.7,
                ),
            )

            reply = response.text or "I'm not sure how to respond to that."
            history.append({"role": "model", "text": reply})
            return reply

        except ServerError as e:
            # 503 high demand — log warning and try fallback model
            logger.warning(f"Model {model_name} overloaded (503). Trying fallback... Error: {e}")
            last_error = e
            time.sleep(0.5)
            continue
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}", exc_info=True)
            return "Sorry, I hit a snag processing that. Can you try again?"

    logger.error(f"All models exhausted: {last_error}")
    return "Google's AI servers are heavily overloaded right now. Please give it one moment and try again!"