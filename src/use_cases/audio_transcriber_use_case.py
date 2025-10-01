"""
Path: src/use_cases/audio_transcriber_use_case.py
"""

from src.entities.audio_transcriber import AudioTranscription

class AudioTranscriberUseCase:
    "Caso de uso para la transcripción de audio."

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        """
        Método abstracto para transcribir un archivo de audio.
        Debe ser implementado por la infraestructura.
        """
        raise NotImplementedError("Este método debe ser implementado por la infraestructura.")
