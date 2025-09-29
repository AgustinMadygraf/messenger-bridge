"""
Path: src/interface_adapter/gateways/speech_to_text_gateway.py
"""

from src.entities.transcription import Transcription

class SpeechToTextGateway:
    "Interfaz para servicios de transcripción de audio a texto."
    def transcribe(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        raise NotImplementedError
