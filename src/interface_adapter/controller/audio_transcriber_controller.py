"""
Path: src/interface_adapter/controller/audio_transcriber_controller.py
"""

from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase
from src.entities.audio_transcriber import AudioTranscription

class AudioTranscriberController:
    """
    Controller para orquestar la transcripción de audio.
    Recibe el caso de uso como dependencia.
    """

    def __init__(self, transcriber_use_case: AudioTranscriberUseCase):
        self.transcriber_use_case = transcriber_use_case

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        """
        Orquesta la transcripción de un archivo de audio.
        """
        return self.transcriber_use_case.transcribe(audio_file_path)

