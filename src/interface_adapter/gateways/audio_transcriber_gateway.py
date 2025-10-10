"""
Path: src/interface_adapter/gateways/audio_transcriber_gateway.py
"""

from abc import ABC, abstractmethod
from src.entities.audio_transcriber import AudioTranscription

class AudioTranscriberGateway(ABC):
    "Puerto para la transcripción de audio."
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        pass
