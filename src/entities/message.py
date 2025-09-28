"""
Path: src/entities/message.py
"""

class Message:
    "Entidad que representa un mensaje de WhatsApp, soportando texto y archivos multimedia."
    def __init__(
        self,
        to: str,
        body: str = "",
        media_url: str = None,
        media_type: str = None
    ):
        self.to = to
        self.body = body
        self.media_url = media_url  # URL del archivo multimedia (imagen, audio, documento, etc.)
        self.media_type = media_type  # Tipo MIME del archivo (image/jpeg, audio/mpeg, etc.)

    def is_media(self) -> bool:
        "Indica si el mensaje contiene archivo multimedia."
        return self.media_url is not None

    def __repr__(self):
        return (
            f"Message(to={self.to!r}, body={self.body!r}, "
            f"media_url={self.media_url!r}, media_type={self.media_type!r})"
        )
