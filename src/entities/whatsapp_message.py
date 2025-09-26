"""
Path: src/entities/whatsapp_message.py"""

class WhatsappMessage:
    "Entidad que representa un mensaje de WhatsApp."
    def __init__(self, to: str, body: str):
        self.to = to
        self.body = body

    def __repr__(self):
        return f"WhatsappMessage(to={self.to!r}, body={self.body!r})"
