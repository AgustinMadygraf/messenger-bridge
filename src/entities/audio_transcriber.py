"""
Path: src/entities/audio_transcriber.py
"""

class AudioTranscription:
    "Entidad que representa el resultado de una transcripción de audio."
    def __init__(self, text: str, source_path: str):
        self.text = text
        self.source_path = source_path

    def is_empty(self) -> bool:
        "Indica si la transcripción está vacía."
        return not bool(self.text)
