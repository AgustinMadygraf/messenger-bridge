"""
Path: src/interface_adapter/gateways/speech_to_text_gateway.py
"""

from src.use_cases.transcribe_audio_use_case import SpeechToTextPort
from src.entities.transcription import Transcription

class SpeechToTextGateway(SpeechToTextPort):
    "Implementación del puerto SpeechToTextPort como gateway."
    def transcribe(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        raise NotImplementedError
