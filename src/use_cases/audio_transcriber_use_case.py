"""
Path: src/use_cases/audio_transcriber_use_case.py
"""

from src.entities.audio_transcriber import AudioTranscription
from src.interface_adapter.gateways.audio_transcriber_gateway import AudioTranscriberGateway

class AudioTranscriberUseCase:
    "Caso de uso para la transcripción de audio."
    def __init__(self, gateway: AudioTranscriberGateway):
        self.gateway = gateway

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        "Transcribe usando el gateway."
        return self.gateway.transcribe(audio_file_path)
