"""
Path: src/infrastructure/flask/flask_webhook.py
"""

from flask import Flask, request, Response

from src.interface_adapter.controller.incoming_message_controller import IncomingMessageController
from src.interface_adapter.presenters.twilio_presenter import TwilioPresenter
from src.use_cases.process_incoming_message_use_case import ProcessIncomingMessageUseCase
from src.entities.conversation import Conversation

conversation = Conversation()
process_message_use_case = ProcessIncomingMessageUseCase(conversation)
incoming_message_controller = IncomingMessageController(process_message_use_case)
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
        twiml = twilio_presenter.present(response_text)
        return Response(twiml, mimetype='application/xml')

    print(f"[Twilio] Modo respuesta. Iniciando webhook Flask en http://{host}:{port}/webhook ...")
    app.run(host=host, port=port)
