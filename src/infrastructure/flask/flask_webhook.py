"""
Path: src/infrastructure/flask/flask_webhook.py
"""

from flask import Flask, request, Response

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
        # Aquí podrías agregar lógica avanzada de respuesta
        response_text = f"Recibido tu mensaje '{user_message}'. Esta es una respuesta simulada."
        # Respuesta TwiML
        twiml = f"<Response><Message>{response_text}</Message></Response>"
        return Response(twiml, mimetype='application/xml')

    print(f"[Twilio] Modo respuesta. Iniciando webhook Flask en http://{host}:{port}/webhook ...")
    app.run(host=host, port=port)
