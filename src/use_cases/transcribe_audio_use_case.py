"""
Path: src/use_cases/transcribe_audio_use_case.py
"""

from abc import ABC, abstractmethod
from src.entities.transcription import Transcription

class SpeechToTextPort(ABC):
    "Puerto para servicios de transcripción de audio a texto."
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        pass #pylint disable=unnecessary-pass

class TranscribeAudioUseCase:
    "Caso de uso para transcribir archivos de audio a texto."
    def __init__(self, speech_service: SpeechToTextPort):
        self.speech_service = speech_service

    def execute(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio y devuelve una entidad Transcription."
        return self.speech_service.transcribe(audio_file_path)
