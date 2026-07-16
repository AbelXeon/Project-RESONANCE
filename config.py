import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Which Groq model to use for chat replies
GROQ_MODEL = "llama-3.3-70b-versatile"

# Personality lives in persona.txt, which is gitignored — keeps personal
# details (names, custom behavior) out of the public repo. Falls back to
# persona.example.txt if persona.txt hasn't been created yet, so the bot
# still runs out of the box.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PERSONA_PATH = os.path.join(_BASE_DIR, "persona.txt")
_PERSONA_FALLBACK_PATH = os.path.join(_BASE_DIR, "persona.example.txt")

_persona_file = _PERSONA_PATH if os.path.exists(_PERSONA_PATH) else _PERSONA_FALLBACK_PATH
with open(_persona_file, "r", encoding="utf-8") as f:
    VIVI_SYSTEM_PROMPT = f.read()