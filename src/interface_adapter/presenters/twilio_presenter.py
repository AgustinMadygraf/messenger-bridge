"""
Path: src/interface_adapter/presenters/twilio_presenter.py
"""

from src.entities.message import Message

class TwilioPresenter:
    "Formatea la respuesta para Twilio (Twiml XML)."
    def present(self, message: Message) -> str:
        "Devuelve la respuesta formateada en TwiML."
        return f"<Response><Message>{message.body}</Message></Response>"
