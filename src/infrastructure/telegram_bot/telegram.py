"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters




def main():
    " Configura y ejecuta el bot de Telegram "
    app = ApplicationBuilder().token("TU_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND))
    app.run_polling()
