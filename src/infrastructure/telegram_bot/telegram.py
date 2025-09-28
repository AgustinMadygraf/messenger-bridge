"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.telegram_gateway import TelegramGateway
from src.entities.message import Message
from src.use_cases.send_message_use_case import SendMessageUseCase

logger = get_logger(__name__)
config = get_config()

class TelegramSender:
    "Implementación concreta para enviar y manejar mensajes con Telegram."
    def __init__(self, token):
        self.app = ApplicationBuilder().token(token).build()

    async def send_message(self, chat_id, text):
        "Envía un mensaje de texto a un chat específico."
        await self.app.bot.send_message(chat_id=chat_id, text=text)

    def add_message_handler(self, handler):
        "Agrega un handler para mensajes entrantes."
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    def add_command_handler(self, command, handler):
        "Agrega un handler para comandos específicos."
        self.app.add_handler(CommandHandler(command, handler))

    def run(self):
        "Inicia el bot de Telegram."
        self.app.run_polling()

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    "Maneja el comando /start."
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

def make_echo_handler(send_message_use_case, gateway):
    " Crea un handler que usa el caso de uso para responder mensajes."
    async def echo(update: Update, _context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        chat_id = update.message.chat_id

        incoming_message = Message(to=chat_id, body=user_message)
        response_text = send_message_use_case.execute(
            incoming_message,
            content_sid="",
            content_variables={}
        )

        # Aquí envías el texto, no la coroutine
        await gateway.sender.send_message(chat_id, response_text)
    return echo

def main():
    "Configura e inicia el bot de Telegram."
    telegram_token = config.get("TELEGRAM_API_KEY")
    if not telegram_token:
        logger.error("No se encontró el token de Telegram en la configuración.")
        raise ValueError("Telegram bot token not set en environment variables.")

    sender = TelegramSender(telegram_token)
    gateway = TelegramGateway(sender)
    send_message_use_case = SendMessageUseCase(gateway)

    sender.add_command_handler("start", start)
    # Usar el handler con dependencias inyectadas
    gateway.add_message_handler(make_echo_handler(send_message_use_case, gateway))

    logger.info("Iniciando bot de Telegram...")
    sender.run()
