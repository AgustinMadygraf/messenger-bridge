"""
Path: src/infrastructure/audio/pydub/pydub_converter.py
"""

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from src.shared.logger import get_logger

logger = get_logger("pydub-converter")

class PydubConverter:
    "Convertidor de formatos de audio usando pydub."
    @staticmethod
    def to_wav(input_path: str, output_path: str) -> bool:
        "Convierte un archivo de audio a formato WAV. Devuelve True si tuvo éxito."
        try:
            logger.debug("Convirtiendo %s a WAV: %s", input_path, output_path)
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="wav")
            logger.info("Conversión a WAV exitosa: %s", output_path)
            return True
        except (FileNotFoundError, CouldntDecodeError, OSError, ValueError, TypeError) as e:
            logger.error("Error en la conversión a WAV: %s", e)
            return False
