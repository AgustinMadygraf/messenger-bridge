"""
Path: src/infrastructure/fastapi/fastapi_webhook.py
"""


import os
import asyncio
import tempfile
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber
from src.interface_adapter.controller.telegram_controller import TelegramMessageController
from src.interface_adapter.controller.twilio_controller import TwilioMessageController
from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.interface_adapter.presenters.twilio_presenter import TwilioPresenter
from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase
from src.entities.message import Message

logger = get_logger("fastapi-webhook")


config = get_config()
TELEGRAM_TOKEN = config.get("TELEGRAM_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
RASA_URL = config.get("RASA_API_URL", "http://localhost:5005/webhooks/rest/webhook")

# Implementación concreta de HttpClient usando requests
class RequestsHttpClient:
    "Implementación de HttpClient usando la librería requests."
    def post(self, url: str, json: dict, timeout: int = 60):
        "Envía una solicitud POST usando requests."
        return requests.post(url, json=json, timeout=timeout)

http_client = RequestsHttpClient()
agent_bot_service = AgentGateway(RASA_URL, http_client=http_client)
twilio_presenter = TwilioPresenter()
telegram_presenter = TelegramMessagePresenter()

# Instanciar el transcriptor de audio y su caso de uso
local_audio_transcriber = LocalAudioTranscriber()
audio_transcriber_use_case = AudioTranscriberUseCase(local_audio_transcriber)

# Inyectar el caso de uso de transcripción en GenerateAgentResponseUseCase
generate_agent_bot_use_case = GenerateAgentResponseUseCase(
    agent_bot_service,
    audio_transcriber_use_case=audio_transcriber_use_case
)

telegram_controller = TelegramMessageController(generate_agent_bot_use_case, telegram_presenter)
twilio_controller = TwilioMessageController(generate_agent_bot_use_case, twilio_presenter)

app = FastAPI()

# Agrega el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a tus dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/twilio/webhook")
async def webhook(request: Request):
    "Webhook para manejar mensajes entrantes de Twilio (WhatsApp) "
    logger.info("Webhook POST recibido")
    form = await request.form()
    user_message = form.get('Body', '')
    from_number = form.get('From', '')
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
    message = update.get("message")
    if not message:
        logger.info("[Telegram] No es un mensaje válido. Ignorando.")
        return PlainTextResponse("OK", status_code=200)

    chat_id = message["chat"]["id"]

    # --- Manejo de mensajes de texto ---
    if "text" in message:
        text = message["text"]
        entities = message.get("entities", None)
        chat_id, response_text = await telegram_controller.handle(chat_id, text, entities)
        logger.info("[Telegram] Respuesta generada: %s", response_text)
        response_message = Message(to=chat_id, body=response_text)
        formatted_responses = telegram_presenter.present(response_message)
        if not isinstance(formatted_responses, list):
            formatted_responses = [formatted_responses]
        payloads = [
            {
                "chat_id": chat_id,
                **resp
            }
            for resp in formatted_responses
        ]
        async with httpx.AsyncClient() as client:
            for payload in payloads:
                resp = await client.post(TELEGRAM_API_URL, json=payload)
                await asyncio.sleep(3)  # <-- Delay de 3 segundos entre mensajes
        return PlainTextResponse("OK", status_code=200)

    # --- Manejo de mensajes de voz (audio) ---
    if "voice" in message:
        voice = message["voice"]
        file_id = voice["file_id"]
        mime_type = voice.get("mime_type", "audio/ogg")
        # Obtener la URL del archivo de audio desde Telegram API
        async with httpx.AsyncClient() as client:
            file_resp = await client.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
            )
            file_info = file_resp.json()
            file_path = file_info["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

            # Descargar el archivo de audio localmente
            audio_resp = await client.get(file_url)
            tmp_file_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_file:
                    tmp_file.write(audio_resp.content)
                    tmp_file_path = tmp_file.name

                # Transcribir el audio usando el caso de uso de transcripción
                transcription = audio_transcriber_use_case.transcribe(tmp_file_path)
                os.remove(tmp_file_path)
            except (httpx.HTTPError, OSError, asyncio.TimeoutError) as e:
                transcription = None
                logger.error("[Telegram] Error al descargar/transcribir audio: %s", e)

        if transcription and not transcription.is_empty():
            transcribed_text = transcription.text
        else:
            transcribed_text = "[No se pudo transcribir el audio. Enviando audio original.]"

        # Construir el objeto Message con media_url y media_type
        audio_message = Message(
            to=chat_id,
            body="[audio]",  # O puedes dejarlo vacío
            media_url=file_url,
            media_type=mime_type
        )
        # Procesar el mensaje de audio usando el controlador, pasando el texto transcripto
        chat_id, response_text = await telegram_controller.handle(chat_id, audio_message, None, transcribed_text=transcribed_text)
        logger.info("[Telegram] Respuesta generada para audio: %s", response_text)
        response_message = Message(to=chat_id, body=response_text)
        formatted_response = telegram_presenter.present(response_message)
        payload = {
            "chat_id": chat_id,
            **formatted_response
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(TELEGRAM_API_URL, json=payload)
        return PlainTextResponse("OK", status_code=200)

    logger.info("[Telegram] No es un mensaje de texto ni de voz. Ignorando.")
    return PlainTextResponse("OK", status_code=200)

@app.get("/")
async def index():
    "Página de inicio simple para verificar que el servidor está funcionando."
    return {"message": "Bienvenido al webhook de FastAPI"}

@app.post("/webchat/webhook")
async def webchat_webhook(request: Request):
    """
    Endpoint para recibir mensajes del chat web y responder con el mensaje del agente.
    Espera un JSON: { "user_id": "...", "text": "mensaje del usuario" }
    Responde: { "role": "assistant", "text": "respuesta del agente" }
    """
    data = await request.json()
    user_id = data.get("user_id", None)
    user_text = data.get("text", "")
    if not user_id or not user_text:
        return {"role": "assistant", "text": "Faltan datos en la solicitud."}

    # Construir entidad Message
    webchat_message = Message(
        to=user_id,
        body=user_text
    )

    # Generar respuesta usando el caso de uso conversacional
    response_message = generate_agent_bot_use_case.execute(user_id, webchat_message)

    return {
        "role": "assistant",
        "text": response_message.body
    }

def run_fastapi_webhook(host="0.0.0.0", port=8443):
    "Función para ejecutar el servidor FastAPI"
    logger.info("[Twilio] Modo respuesta. Iniciando webhook FastAPI en http://%s:%s/webhook ...", host, port)
    uvicorn.run("src.infrastructure.fastapi.fastapi_webhook:app", host=host, port=port, reload=False)
