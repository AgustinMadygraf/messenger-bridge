"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.telegram_gateway import TelegramGateway
from src.interface_adapter.controller.telegram_message_controller import TelegramMessageController
from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter

# NUEVO: imports para memoria y Gemini
from src.entities.conversation_manager import ConversationManager
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
from src.infrastructure.google_generativeai.gemini_service import GeminiService
from src.use_cases.generate_response_with_memory_use_case import GenerateResponseWithMemoryUseCase

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

def make_handler(controller, gateway):
    "Crea un handler para responder a mensajes de texto usando memoria y Gemini."
    async def handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        user_message = update.message.text
        chat_id, response_text = await controller.handle(chat_id, user_message)
        await gateway.sender.send_message(chat_id, response_text)
    return handler

def main():
    "Configura e inicia el bot de Telegram con memoria y Gemini."
    telegram_token = config.get("TELEGRAM_API_KEY")
    if not telegram_token:
        logger.error("No se encontró el token de Telegram en la configuración.")
        raise ValueError("Telegram bot token not set en environment variables.")

    sender = TelegramSender(telegram_token)
    gateway = TelegramGateway(sender)
    presenter = TelegramMessagePresenter()

    # NUEVO: inicialización de memoria y Gemini
    conversation_manager = ConversationManager()
    gemini_service = GeminiService()
    gemini_use_case = GenerateGeminiResponseUseCase(gemini_service)
    # Puedes cargar instrucciones de sistema si lo deseas
    system_instructions = None
    use_case = GenerateResponseWithMemoryUseCase(conversation_manager, gemini_use_case, system_instructions)

    controller = TelegramMessageController(use_case, presenter)

    sender.add_command_handler("start", start)
    gateway.add_message_handler(make_handler(controller, gateway))

    logger.info("Iniciando bot de Telegram...")
    sender.run()
