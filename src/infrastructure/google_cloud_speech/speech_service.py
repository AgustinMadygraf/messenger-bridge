"""
Path: src/infrastructure/google_cloud_speech/speech_service.py
Servicio para transcribir audio a texto usando Google Speech-to-Text.
"""

import os
from google.cloud import speech
from google.api_core.exceptions import GoogleAPICallError

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.use_cases.transcribe_audio_use_case import SpeechToTextGateway
from src.entities.transcription import Transcription

logger = get_logger("speech-service")

class SpeechService(SpeechToTextGateway):
    "Servicio para transcribir archivos de audio a texto usando Google Speech-to-Text."
    def __init__(self, credentials_path=None):
        config = get_config()
        cred_path = credentials_path or config.get("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path:
            if not os.path.isfile(cred_path):
                logger.error("El archivo de credenciales no existe: %s", cred_path)
                raise FileNotFoundError(f"El archivo de credenciales no existe: {cred_path}")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
            logger.debug("Usando credenciales de Google Cloud: %s", cred_path)
        try:
            self.client = speech.SpeechClient()
            logger.info("SpeechService inicializado correctamente.")
        except Exception as e:
            logger.error("Error al inicializar SpeechClient: %s", e)
            raise

    def transcribe(self, audio_file_path: str) -> Transcription:
        "Transcribe el archivo de audio especificado y devuelve el texto."
        try:
            logger.debug("Intentando abrir el archivo de audio: %s", audio_file_path)
            with open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            logger.debug("Tamaño del archivo de audio leído: %d bytes", len(content))
            logger.debug("Primeros 32 bytes del audio: %s", content[:32])

            # Depuración: verifica si el archivo parece OGG/Opus
            if not content.startswith(b'OggS'):
                logger.warning("El archivo no parece ser OGG/Opus. Encabezado: %s", content[:8])

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                sample_rate_hertz=16000,
                language_code="es-AR",
            )
            logger.debug("Configuración de reconocimiento: encoding=%s, sample_rate_hertz=%d, language_code=%s",
                         "OGG_OPUS", 16000, "es-AR")

            response = self.client.recognize(config=config, audio=audio)
            logger.debug("Respuesta completa de la API: %s", response)
            logger.debug("Cantidad de resultados: %d", len(response.results))

            for idx, result in enumerate(response.results):
                logger.debug("Resultado %d: %s", idx, result)
                for alt_idx, alt in enumerate(result.alternatives):
                    logger.debug("Alternativa %d: transcript='%s', confidence=%s", alt_idx, alt.transcript, alt.confidence)

            if not response.results:
                logger.warning("La API no devolvió resultados. Revisa el formato, idioma y calidad del audio.")

            transcript = " ".join([result.alternatives[0].transcript for result in response.results if result.alternatives])
            logger.debug("Transcripción obtenida: '%s'", transcript)

            success = bool(transcript)
            return Transcription(
                text=transcript if transcript else "",
                language="es-AR",
                success=success,
                error_message=None if success else "No se pudo transcribir el audio"
            )
        except FileNotFoundError as e:
            logger.error("Archivo de audio no encontrado: %s", e)
            return Transcription(
                text="",
                language="es-AR",
                success=False,
                error_message=str(e)
            )
        except GoogleAPICallError as e:
            logger.error("Error en la llamada a la API de Google Speech: %s", e)
            return Transcription(
                text="",
                language="es-AR",
                success=False,
                error_message="Error en la llamada a la API de Google Speech"
            )
        except (IOError, ValueError) as e:
            logger.error("Error inesperado en transcribe: %s", e, exc_info=True)
            return Transcription(
                text="",
                language="es-AR",
                success=False,
                error_message=f"Error inesperado: {str(e)}"
            )
