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
from groq_client import ask_jarvis
from deepgram_client import transcribe_audio

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "At your service, sir. J.A.R.V.I.S. online and ready."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    reply = ask_jarvis(chat_id, user_text)
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
        await update.message.reply_text("I couldn't quite make that out, sir.")
        return

    reply = ask_jarvis(chat_id, transcript)
    await update.message.reply_text(f"You said: \"{transcript}\"\n\n{reply}")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("Jarvis bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()