"""
Path: src/interface_adapter/controllers/audio_transcriber_controller.py
Controlador para la transcripción de audio.
"""

from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase
from src.entities.audio_transcriber import AudioTranscription

class AudioTranscriberController:
    "Controlador para la transcripción de audio."
    def __init__(self, transcriber_use_case: AudioTranscriberUseCase):
        self.transcriber_use_case = transcriber_use_case

    def transcribe_audio(self, audio_file_path: str) -> AudioTranscription:
        "Controla la transcripción de un archivo de audio."
        return self.transcriber_use_case.transcribe(audio_file_path)
