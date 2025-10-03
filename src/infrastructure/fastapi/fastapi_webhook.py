"""
Path: src/infrastructure/fastapi/fastapi_webhook.py

Servidor FastAPI para manejar webhooks de Twilio y Telegram usando Rasa.
"""

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
import uvicorn

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.controller.telegram_controller import TelegramMessageController
from src.interface_adapter.controller.twilio_controller import TwilioMessageController
from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.interface_adapter.presenters.twilio_presenter import TwilioPresenter
from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.entities.message import Message

logger = get_logger("fastapi-webhook")

config = get_config()
TELEGRAM_TOKEN = config.get("TELEGRAM_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
RASA_URL = config.get("RASA_API_URL", "http://localhost:5005/webhooks/rest/webhook")
agent_bot_service = AgentGateway(RASA_URL)
twilio_presenter = TwilioPresenter()
telegram_presenter = TelegramMessagePresenter()
generate_agent_bot_use_case = GenerateAgentResponseUseCase(agent_bot_service)
telegram_controller = TelegramMessageController(generate_agent_bot_use_case, telegram_presenter)
twilio_controller = TwilioMessageController(generate_agent_bot_use_case, twilio_presenter)

app = FastAPI()

@app.post("/twilio/webhook")
async def webhook(request: Request):
    "Webhook para manejar mensajes entrantes de Twilio (WhatsApp) "
    logger.info("Webhook POST recibido")
    form = await request.form()
    user_message = form.get('Body', '')
    from_number = form.get('From', '')
    logger.debug("Datos recibidos: %s", dict(form))
    logger.info("[Twilio] Mensaje recibido de %s: %s", from_number, user_message)

    # --- Manejo de archivos multimedia ---
    num_media = int(form.get('NumMedia', '0'))
    media_url = None
    media_type = None
    if num_media > 0:
        media_url = form.get('MediaUrl0')
        media_type = form.get('MediaContentType0')
        logger.info("[Twilio] Archivo multimedia recibido: %s (%s)", media_url, media_type)

    # --- Construye entidad Message para texto y multimedia ---
    whatsapp_message = Message(
        to=from_number,
        body=user_message,
        media_url=media_url,
        media_type=media_type
    )

    # Usa el controlador para obtener la respuesta TwiML
    twiml = twilio_controller.handle(from_number, whatsapp_message)
    logger.info("Respuesta TwiML generada: %s", twiml)
    return Response(content=twiml, media_type="application/xml")

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    "Webhook para manejar mensajes entrantes de Telegram "
    logger.info("[Telegram] Webhook POST recibido")
    update = await request.json()
    logger.debug("[Telegram] Payload recibido: %s", update)

    # Extraer chat_id, texto y entidades del mensaje
    message = update.get("message")
    if not message or "text" not in message:
        logger.info("[Telegram] No es un mensaje de texto. Ignorando.")
        return PlainTextResponse("OK", status_code=200)

    chat_id = message["chat"]["id"]
    text = message["text"]
    entities = message.get("entities", None)  # Extraer entidades si existen

    # Usar el controlador actualizado que procesa entidades
    chat_id, response_text = await telegram_controller.handle(chat_id, text, entities)
    logger.info("[Telegram] Respuesta generada: %s", response_text)

    # Log de diagnóstico: longitud y preview del mensaje
    logger.debug("[Telegram] Longitud de la respuesta: %d", len(response_text))
    logger.debug("[Telegram] Primeros 500 caracteres: %s", response_text[:500])

    response_message = Message(to=chat_id, body=response_text)
    formatted_response = telegram_presenter.present(response_message)

    # Log de diagnóstico: mensaje formateado y longitud final
    logger.debug("[Telegram] Longitud del mensaje formateado: %d", len(formatted_response['text']))
    logger.debug("[Telegram] Preview mensaje formateado: %s", formatted_response['text'][:500])
    logger.debug("[Telegram] Payload a enviar: %s", formatted_response)

    payload = {
        "chat_id": chat_id,
        **formatted_response
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(TELEGRAM_API_URL, json=payload)
        logger.debug("[Telegram] Respuesta enviada. Status: %s, Body: %s", resp.status_code, resp.text)

    return PlainTextResponse("OK", status_code=200)

@app.get("/", response_class=HTMLResponse)
async def index():
    "Página de inicio simple con instrucciones"
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Twilio Bot QR</title>
    </head>
    <body>
        <h2>Escanea este QR para conectar tu WhatsApp</h2>
        <img src="/static/qr.svg" alt="QR WhatsApp" style="width:300px;height:300px;">
    </body>
    </html>
    """
    return html

def run_fastapi_webhook(host="0.0.0.0", port=8443):
    "Función para ejecutar el servidor FastAPI"
    logger.info("[Twilio] Modo respuesta. Iniciando webhook FastAPI en http://%s:%s/webhook ...", host, port)
    uvicorn.run("src.infrastructure.fastapi.fastapi_webhook:app", host=host, port=port, reload=False)
