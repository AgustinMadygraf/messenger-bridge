"""
Path: src/interface_adapter/presenters/transcription_presenter.py
Presentador para formatear la respuesta de transcripción.
"""

from src.domain.entities.transcription import Transcription

class TranscriptionPresenter:
    "Presentador para la salida de transcripción."
    @staticmethod
    def present(transcription: Transcription) -> dict:
        "Formatea la transcripción en una estructura de respuesta."
        return {
            "status": "success" if transcription.success else "error",
            "transcription": transcription.text,
            "language": transcription.language,
            "error_message": transcription.error_message
        }
