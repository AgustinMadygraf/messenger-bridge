"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.interface_adapter.gateways.telegram_gateway import TelegramGateway
from src.interface_adapter.controller.telegram_controller import TelegramMessageController
from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.entities.message import Message

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
        "Agrega un handler para mensajes entrantes de cualquier tipo."
        self.app.add_handler(MessageHandler(filters.ALL, handler))

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
            # Informa al usuario que los mensajes de voz no son compatibles
            await gateway.sender.send_message(chat_id, "Lo siento, actualmente no puedo procesar mensajes de voz.")
            return

        # Procesa otros tipos de mensajes si lo deseas
        await gateway.sender.send_message(chat_id, "Sólo se aceptan mensajes de texto o audio.")
    return handler

def run_telegram_mode():
    "Configura e inicia el bot de Telegram con Rasa."
    telegram_token = config.get("TELEGRAM_API_KEY")
    if not telegram_token:
        logger.error("No se encontró el token de Telegram en la configuración.")
        raise ValueError("Telegram bot token not set en environment variables.")

    sender = TelegramSender(telegram_token)
    gateway = TelegramGateway(sender)
    presenter = TelegramMessagePresenter()

    rasa_url = config.get("RASA_API_URL", "http://localhost:5005/webhooks/rest/webhook")
    rasa_service = AgentGateway(rasa_url)
    use_case = GenerateAgentResponseUseCase(rasa_service)

    controller = TelegramMessageController(use_case, presenter)

    sender.add_command_handler("start", start)
    gateway.add_message_handler(make_handler(controller, gateway))

    logger.info("Iniciando bot de Telegram...")
    sender.run()

class TelegramApp:
    "Aplicación principal para manejar interacciones de Telegram con Rasa."
    def __init__(self, token: str, rasa_url: str):
        self.token = token
        self.rasa_service = AgentGateway(rasa_url)
        self.generate_response_use_case = GenerateAgentResponseUseCase(
            self.rasa_service
        )

    def handle_message(self, chat_id: str, text: str):
        "Maneja un mensaje entrante de Telegram."
        user_message = Message(to=chat_id, body=text)
        # Usa el caso de uso de Rasa para obtener la respuesta
        response_message = self.generate_response_use_case.execute(chat_id, user_message)
        # Envía la respuesta al usuario por Telegram
        self.send_message(chat_id, response_message.body)
