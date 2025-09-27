"""
Path: src/infrastructure/flask/flask_webhook.py
"""

from flask import Flask, request, Response

from src.interface_adapter.controller.incoming_message_controller import IncomingMessageController
from src.interface_adapter.presenters.twilio_presenter import TwilioPresenter
from src.interface_adapter.presenters.gemini_presenter import GeminiPresenter
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
from src.entities.conversation import Conversation
from src.infrastructure.google_generativeai.gemini_service import GeminiService
from src.interface_adapter.gateways.gemini_gateway import GeminiGateway

conversation = Conversation()
gemini_service = GeminiService()
gemini_gateway = GeminiGateway(gemini_service)
generate_gemini_use_case = GenerateGeminiResponseUseCase(gemini_gateway)
incoming_message_controller = IncomingMessageController(generate_gemini_use_case, conversation)
gemini_presenter = GeminiPresenter()
twilio_presenter = TwilioPresenter()

def run_flask_webhook(host="0.0.0.0", port=5000):
    "Inicia un servidor Flask para manejar webhooks de Twilio."
    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        "Webhook para recibir mensajes de Twilio y responder."
        data = request.form
        user_message = data.get('Body', '')
        from_number = data.get('From', '')
        print(f"[Twilio] Mensaje recibido de {from_number}: {user_message}")

        response_text = incoming_message_controller.handle(from_number, user_message)
        formatted_response = gemini_presenter.present(response_text)
        twiml = twilio_presenter.present(formatted_response)
        return Response(twiml, mimetype='application/xml')

    print(f"[Twilio] Modo respuesta. Iniciando webhook Flask en http://{host}:{port}/webhook ...")
    app.run(host=host, port=port)
