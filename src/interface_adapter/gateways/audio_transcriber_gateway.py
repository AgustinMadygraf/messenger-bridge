"""
Path: src/interface_adapter/gateways/audio_transcriber_gateway.py
"""

from abc import ABC, abstractmethod

class AudioTranscriberGateway(ABC):
    """
    Interfaz para el acceso a archivos de audio.
    """

    @abstractmethod
    def get_audio_file(self, audio_file_path: str) -> str:
        """
        Devuelve la ruta del archivo de audio a transcribir.
        Puede implementar lógica adicional (descarga, validación, etc).
        """
        pass #pylint :disable=unnecessary-pass
