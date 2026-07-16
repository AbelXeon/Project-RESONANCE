<div align="center">

# 🤖 Telegram AI Assistant Bot

**A personal AI assistant on Telegram**  
*Chat, voice notes, live web search, and a fully customizable personality.*

![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq-orange?style=for-the-badge)
![Deepgram](https://img.shields.io/badge/Voice-Deepgram-purple?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

</div>

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 💬 **Text & voice input** | Handles typed messages and Telegram voice notes, transcribed via Deepgram |
| 🌐 **Live web search** | The model calls a search tool on its own for time-sensitive questions — news, prices, current events — instead of relying only on training data |
| 🧠 **Per-chat memory** | Keeps a rolling window of recent messages so replies stay contextual |
| 🎭 **Configurable personality** | The system prompt lives in a separate, gitignored file — customize freely without touching version control |

---

## 🗂️ Architecture

├── main.py              # Telegram bot entrypoint and message handlers
├── config.py             # Environment config and persona loading
├── groq_client.py        # Chat completions + tool-calling loop
├── search_tool.py        # Web search tool definition
├── deepgram_client.py    # Voice note transcription
├── keepalive.py          # Minimal HTTP server for host/uptime-monitor compatibility
├── persona.example.txt   # Template for the bot's personality
├── persona.txt           # Your actual personality (gitignored, create locally)
├── requirements.txt
└── .env.example          # Environment variable template

main.py is the only module that talks to Telegram directly. Text messages and transcribed voice notes are both routed through groq_client.ask_vivi(), which handles the Groq API call and, when needed, hands off to search_tool.py for live information before responding.

📋 Requirements
Python 3.10+
A Telegram bot token → @BotFather
A Groq API key → console.groq.com
A Deepgram API key → console.deepgram.com

🚀 Setup
Clone the repository
code
Bash
git clone <this-repo>
cd <this-repo>
Set up virtual environment

Bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
Install dependencies


Bash
pip install -r requirements.txt
Initialize configuration


Bash
cp .env.example .env                 # then fill in your API keys
cp persona.example.txt persona.txt   # then customize the personality
Run the bot


Bash
python main.py


⚙️ Configuration
Environment variables (.env)
Variable	Description
TELEGRAM_TOKEN	Bot token from BotFather
GROQ_API_KEY	API key for chat completions
DEEPGRAM_API_KEY	API key for voice transcription
Personality (persona.txt)
Plain text, loaded as the system prompt at startup. Not tracked by git — customize freely without exposing personal details in a public repo. If persona.txt doesn't exist, the bot falls back to the generic template in persona.example.txt.

☁️ Deployment
The bot runs via long polling, so it doesn't need a public URL for Telegram's sake — it just needs a host that keeps the process running continuously.
A small Flask server (keepalive.py) runs alongside the bot purely to satisfy platforms that require something bound to an HTTP port. It serves a single 200 OK response and has no connection to the bot's logic.
Option A — Render (free tier) + uptime ping
Render's free tier only supports Web Services (apps that require HTTP requests), not background workers. The workaround:
Push this repo to Render as a Web Service.
Build command: pip install -r requirements.txt
Start command: python main.py
Environment Variables: Add TELEGRAM_TOKEN, GROQ_API_KEY, DEEPGRAM_API_KEY.
Render assigns a public URL and a PORT env var, which keepalive.py binds to automatically.
Add a free monitor on UptimeRobot (or cron-job.org) pointed at that URL, checked every 5–10 minutes.
As long as the monitor keeps pinging, Render never sees 15 minutes of inactivity — the bot stays up continuously, at no cost.
Option B — VPS / free-tier cloud VM
For a setup with no keep-alive dependency, run it on any VM with a systemd service:

Ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
WorkingDirectory=/path/to/repo
ExecStart=/path/to/repo/venv/bin/python main.py
Restart=always
User=youruser

[Install]
WantedBy=multi-user.target


📝 Notes
Memory: Conversation history is stored in memory and resets on restart. For persistence, swap the in-memory store in groq_client.py for SQLite or another database.
TTS: Text-to-speech (spoken replies) isn't implemented, but could be added via Deepgram's or another provider's TTS API.
