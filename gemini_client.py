import logging
import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, VIVI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

# 3.5-flash-lite is ultra-fast with virtually no 503 spikes; 3.6-flash as backup
MODELS_TO_TRY = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
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

    for model_name in MODELS_TO_TRY:
        # Retry up to 2 times if there's a temporary 503 spike
        for attempt in range(2):
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

            except Exception as e:
                last_error = e
                err_text = str(e)
                logger.warning(f"Attempt {attempt + 1} for {model_name} failed: {err_text}")

                # If it's a temporary 503 high demand spike, pause 1s and retry
                if "503" in err_text or "UNAVAILABLE" in err_text:
                    time.sleep(1.0)
                    continue
                
                # For any other error, move immediately to the next model
                break

    logger.error(f"All model attempts failed: {last_error}")
    return "Sorry, I had a brief connection hiccup. Can you say that again?"