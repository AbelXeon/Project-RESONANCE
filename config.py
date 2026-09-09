import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Gemini model to use
GEMINI_MODEL = "gemini-2.5-flash"

# Load persona prompt
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PERSONA_PATH = os.path.join(_BASE_DIR, "persona.txt")
_PERSONA_FALLBACK_PATH = os.path.join(_BASE_DIR, "persona.example.txt")

_persona_file = _PERSONA_PATH if os.path.exists(_PERSONA_PATH) else _PERSONA_FALLBACK_PATH
with open(_persona_file, "r", encoding="utf-8") as f:
    VIVI_SYSTEM_PROMPT = f.read()