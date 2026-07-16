import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_TOKEN
from groq_client import ask_vivi
from deepgram_client import transcribe_audio
from keepalive import start_keepalive_server

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey, it's Vivi! I'm here. What's going on?"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    reply = ask_vivi(chat_id, user_text)
    await update.message.reply_text(reply)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    local_path = f"/tmp/{voice.file_id}.ogg"
    await file.download_to_drive(local_path)

    try:
        transcript = transcribe_audio(local_path)
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

    if not transcript:
        await update.message.reply_text("Hmm, I couldn't catch that — mind sending it again?")
        return

    reply = ask_vivi(chat_id, transcript)
    await update.message.reply_text(f"You said: \"{transcript}\"\n\n{reply}")


def main():
    start_keepalive_server()

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("Vivi bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()