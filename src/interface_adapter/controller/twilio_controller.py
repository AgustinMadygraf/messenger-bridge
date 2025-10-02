"""
Path: src/interface_adapter/controller/twilio_controller.py
"""

from src.entities.message import Message

class TwilioMessageController:
    "Controlador para manejar mensajes de Twilio usando un caso de uso y presentador."
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    def handle(self, from_number, user_message: Message):
        "Procesa el mensaje entrante y devuelve la respuesta formateada para Twilio."
        response_message = self.use_case.execute(from_number, user_message)
        bot_message = Message(to="Bot", body=response_message.body)
        twiml = self.presenter.present(bot_message)
        return twiml
