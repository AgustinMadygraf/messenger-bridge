"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.infrastructure.google_generativeai.gemini_service import GeminiService
from src.interface_adapter.gateways.telegram_gateway import TelegramGateway
from src.interface_adapter.controller.telegram_message_controller import TelegramMessageController
from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
from src.use_cases.generate_response_with_memory_use_case import GenerateResponseWithMemoryUseCase
from src.entities.conversation_manager import ConversationManager

logger = get_logger(__name__)
config = get_config()

SYSTEM_INSTRUCTIONS_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "google_generativeai",
    "system_instructions.json"
)

class TelegramSender:
    "Implementación concreta para enviar y manejar mensajes con Telegram."
    def __init__(self, token):
        self.app = ApplicationBuilder().token(token).build()

    async def send_message(self, chat_id, text):
        "Envía un mensaje de texto a un chat específico."
        await self.app.bot.send_message(chat_id=chat_id, text=text)

    def add_message_handler(self, handler):
        "Agrega un handler para mensajes entrantes de cualquier tipo."
        self.app.add_handler(MessageHandler(filters.ALL, handler))  # <-- Cambia filters.TEXT por filters.ALL

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
    "Crea un handler para responder a mensajes de texto y audios usando memoria y Gemini."
    async def handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        # Procesa mensajes de texto
        if update.message.text:
            user_message = update.message.text
            chat_id, response_text = await controller.handle(chat_id, user_message)
            await gateway.sender.send_message(chat_id, response_text)
            return

        # Procesa mensajes de audio (voice)
        if update.message.voice:
            # Descarga el archivo de audio
            file = await update.message.voice.get_file()
            audio_file_path = f"temp_audio_{chat_id}.ogg"
            await file.download_to_drive(audio_file_path)

            # Aquí deberías integrar una API de transcripción (por ejemplo, Google Speech-to-Text)
            # Por ahora, simula la transcripción
            transcribed_text = "[Audio recibido: transcripción no implementada]"

            chat_id, response_text = await controller.handle(chat_id, transcribed_text)
            await gateway.sender.send_message(chat_id, response_text)
            # Opcional: elimina el archivo temporal
            try:
                os.remove(audio_file_path)
            except OSError as e:
                logger.debug("No se pudo eliminar el archivo temporal: %s", e)
            return

        # Procesa otros tipos de mensajes si lo deseas
        await gateway.sender.send_message(chat_id, "Sólo se aceptan mensajes de texto o audio.")
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

    conversation_manager = ConversationManager()
    gemini_service = GeminiService(instructions_json_path=SYSTEM_INSTRUCTIONS_PATH)
    gemini_use_case = GenerateGeminiResponseUseCase(gemini_service)
    # Las instrucciones ya están cargadas en gemini_service.system_instructions
    use_case = GenerateResponseWithMemoryUseCase(conversation_manager, gemini_use_case, gemini_service.system_instructions)

    controller = TelegramMessageController(use_case, presenter)

    sender.add_command_handler("start", start)
    gateway.add_message_handler(make_handler(controller, gateway))

    logger.info("Iniciando bot de Telegram...")
    sender.run()
