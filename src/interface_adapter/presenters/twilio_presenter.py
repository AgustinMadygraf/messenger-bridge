"""
Path: src/interface_adapter/presenters/twilio_presenter.py
"""

class TwilioPresenter:
    "Formatea la respuesta para Twilio (Twiml XML)."
    def present(self, response_text: str) -> str:
        " Devuelve la respuesta formateada en TwiML."
        return f"<Response><Message>{response_text}</Message></Response>"
