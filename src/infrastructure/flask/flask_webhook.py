"""
Path: src/infrastructure/flask/flask_webhook.py
"""

import os
from flask import Flask, request, Response, render_template_string

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.interface_adapter.presenters.twilio_presenter import TwilioPresenter
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.entities.message import Message

logger = get_logger("flask-webhook")

config = get_config()
RASA_URL = config.get("RASA_API_URL", "http://localhost:5005/webhooks/rest/webhook")
rasa_service = AgentGateway(RASA_URL)
generate_rasa_use_case = GenerateAgentResponseUseCase(rasa_service)
twilio_presenter = TwilioPresenter()

def run_flask_webhook(host="0.0.0.0", port=5000):
    "Inicia un servidor Flask para manejar webhooks de Twilio usando Rasa."
    app = Flask(__name__, static_folder=os.path.abspath("static"))

    @app.route('/webhook', methods=['POST'])
    def webhook():
        logger.info("Webhook POST recibido")
        data = request.form
        user_message = data.get('Body', '')
        from_number = data.get('From', '')
        logger.debug("Datos recibidos: %s", data)
        logger.info("[Twilio] Mensaje recibido de %s: %s", from_number, user_message)

        # --- Manejo de archivos multimedia ---
        num_media = int(data.get('NumMedia', '0'))
        media_url = None
        media_type = None
        if num_media > 0:
            media_url = data.get('MediaUrl0')
            media_type = data.get('MediaContentType0')
            logger.info("[Twilio] Archivo multimedia recibido: %s (%s)", media_url, media_type)

        # --- Construye entidad Message para texto y multimedia ---
        whatsapp_message = Message(
            to=from_number,
            body=user_message,
            media_url=media_url,
            media_type=media_type
        )

        # Usa el caso de uso de Rasa para obtener la respuesta
        response_message = generate_rasa_use_case.execute(from_number, whatsapp_message)
        bot_message = Message(to="Bot", body=response_message.body)
        twiml = twilio_presenter.present(bot_message)
        logger.info("Respuesta TwiML generada: %s", twiml)
        return Response(twiml, mimetype='application/xml')

    @app.route('/', methods=['GET'])
    def index():
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
        return render_template_string(html), 200

    logger.info("[Twilio] Modo respuesta. Iniciando webhook Flask en http://%s:%s/webhook ...", host, port)
    app.run(host=host, port=port, debug=False, use_reloader=False)
