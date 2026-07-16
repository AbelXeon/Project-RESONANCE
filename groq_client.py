from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, JARVIS_SYSTEM_PROMPT

client = Groq(api_key=GROQ_API_KEY)

# Very simple in-memory history per chat_id. Fine for a first bot;
# swap for a real DB later if you want it to survive restarts.
_history = {}

MAX_TURNS = 10  # how many past messages to keep per chat


def get_history(chat_id: int):
    if chat_id not in _history:
        _history[chat_id] = []
    return _history[chat_id]


def ask_jarvis(chat_id: int, user_text: str) -> str:
    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})

    messages = [{"role": "system", "content": JARVIS_SYSTEM_PROMPT}] + history[-MAX_TURNS:]

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply