"""
Path: src/infrastructure/telegram_bot/telegram.py
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.agent_gateway import AgentGateway
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

def run_telegram_mode():
    "Configura el webhook de Telegram (no levanta servidor, solo setea el webhook si es necesario)."
    telegram_token = config.get("TELEGRAM_API_KEY")
    logger.debug("Obteniendo TELEGRAM_API_KEY: %s", telegram_token)
    if not telegram_token:
        logger.error("No se encontró el token de Telegram en la configuración.")
        raise ValueError("Telegram bot token not set en environment variables.")

    public_url = config.get("NGROK_DOMAIN")
    if not public_url:
        logger.error("No se pudo iniciar ngrok para Telegram webhook.")
        return
    webhook_url = f"{public_url}/telegram/webhook"
    logger.info("Configurando webhook de Telegram en: %s", webhook_url)

    # Configura el webhook usando la API de Telegram
    import requests
    set_webhook_url = f"https://api.telegram.org/bot{telegram_token}/setWebhook"
    resp = requests.post(set_webhook_url, json={"url": webhook_url}, timeout=10)
    if resp.ok:
        logger.info("Webhook de Telegram configurado correctamente.")
    else:
        logger.error("Error configurando webhook de Telegram: %s", resp.text)

def make_handler(controller, gateway):
    "Crea un handler para responder a mensajes de texto y audios usando memoria y Gemini."
    async def handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
        logger.debug("Mensaje recibido: %s", update)
        if not hasattr(update, "message") or update.message is None:
            logger.debug("Update recibido sin mensaje. Update: %s", update)
            return
        chat_id = update.message.chat_id
        logger.debug("chat_id: %s", chat_id)

        # Procesa mensajes de texto
        if update.message.text:
            user_message = update.message.text
            logger.debug("Mensaje de texto recibido: %s", user_message)
            try:
                chat_id, response_text = await controller.handle(chat_id, user_message)
                logger.debug("Respuesta generada: %s", response_text)
                await gateway.sender.send_message(chat_id, response_text)
            except (ValueError, TypeError) as e:
                logger.error("Error procesando mensaje de texto: %s", e, exc_info=True)
            return

        # Procesa mensajes de audio (voice)
        if update.message.voice:
            logger.debug("Mensaje de voz recibido.")
            await gateway.sender.send_message(chat_id, "Lo siento, actualmente no puedo procesar mensajes de voz.")
            return

        logger.debug("Mensaje de tipo no soportado recibido.")
        await gateway.sender.send_message(chat_id, "Sólo se aceptan mensajes de texto o audio.")
    return handler

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
