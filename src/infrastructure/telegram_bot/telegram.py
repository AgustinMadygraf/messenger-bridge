"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

logger = get_logger(__name__)
config = get_config()

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    "Responde al comando /start"
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

async def echo(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    "Reenvía los mensajes de texto que recibe"
    await update.message.reply_text(update.message.text)

def main():
    "Configura y ejecuta el bot de Telegram"
    telegram_token = config.get("TELEGRAM_API_KEY")
    if not telegram_token:
        logger.error("No se encontró el token de Telegram en la configuración.")
        raise ValueError("Telegram bot token not set in environment variables.")
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logger.info("Iniciando bot de Telegram...")
    app.run_polling()
