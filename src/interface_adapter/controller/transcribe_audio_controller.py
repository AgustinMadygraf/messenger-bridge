"""
Path: src/interface_adapter/controller/transcribe_audio_controller.py
"""

from src.use_cases.transcribe_audio_use_case import TranscribeAudioUseCase
from src.interface_adapter.presenters.transcription_presenter import TranscriptionPresenter

class TranscribeAudioController:
    "Controller para manejar solicitudes de transcripción de audio."
    def __init__(self, use_case: TranscribeAudioUseCase):
        self.use_case = use_case

    def handle(self, audio_file_path: str):
        "Maneja la solicitud de transcripción y devuelve el resultado formateado."
        transcription = self.use_case.execute(audio_file_path)
        return TranscriptionPresenter.present(transcription)
