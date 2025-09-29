"""
Path: src/use_cases/transcribe_audio_use_case.py
"""

from src.entities.transcription import Transcription

class SpeechToTextGateway:
    "Interfaz para servicios de transcripción de audio a texto."
    def transcribe(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        raise NotImplementedError

class TranscribeAudioUseCase:
    "Caso de uso para transcribir archivos de audio a texto."
    def __init__(self, speech_gateway: SpeechToTextGateway):
        self.speech_gateway = speech_gateway

    def execute(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        return self.speech_gateway.transcribe(audio_file_path)
