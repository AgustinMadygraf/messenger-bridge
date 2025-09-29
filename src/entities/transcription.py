"""
Path: src/domain/entities/transcription.py
"""

class Transcription:
    "Entidad que representa una transcripción de audio."
    def __init__(self, text: str, language: str = "es-AR", success: bool = True, error_message: str = None):
        self.text = text
        self.language = language
        self.success = success
        self.error_message = error_message

    def __repr__(self):
        return f"<Transcription success={self.success} language={self.language} text='{self.text}'>"
