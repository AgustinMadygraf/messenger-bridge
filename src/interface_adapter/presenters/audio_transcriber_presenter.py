"""
Path: src/interface_adapter/presenters/audio_transcriber_presenter.py
"""

from src.entities.audio_transcriber import AudioTranscription


class AudioTranscriberPresenter:
    """
    Presenter para dar formato a la salida de la transcripción de audio.
    """

    def present(self, transcription: AudioTranscription) -> str:
        """
        Da formato a la transcripción para su presentación.
        """
        if transcription.is_empty():
            return f"No se pudo obtener una transcripción para el archivo: {transcription.source_path}"
        return f"Transcripción del archivo '{transcription.source_path}':\n{transcription.text}"
