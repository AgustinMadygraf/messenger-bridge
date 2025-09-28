"""
Path: src/infrastructure/google_cloud_speech/speech_service.py
Servicio para transcribir audio a texto usando Google Speech-to-Text.
"""

import os
from google.cloud import speech
from google.api_core.exceptions import GoogleAPICallError

from src.shared.logger import get_logger
from src.shared.config import get_config

logger = get_logger("speech-service")

class SpeechService:
    "Servicio para transcribir archivos de audio a texto usando Google Speech-to-Text."
    def __init__(self, credentials_path=None):
        # Configura las credenciales si se proporciona la ruta o desde config
        config = get_config()
        cred_path = credentials_path or config.get("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
            logger.debug("Usando credenciales de Google Cloud: %s", cred_path)
        try:
            self.client = speech.SpeechClient()
            logger.info("SpeechService inicializado correctamente.")
        except Exception as e:
            logger.error("Error al inicializar SpeechClient: %s", e)
            raise

    def transcribe(self, audio_file_path: str) -> str:
        "Transcribe el archivo de audio especificado y devuelve el texto."
        try:
            with open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                sample_rate_hertz=16000,
                language_code="es-AR",  # Ajusta el idioma según tu necesidad
            )

            response = self.client.recognize(config=config, audio=audio)

            transcript = " ".join([result.alternatives[0].transcript for result in response.results])
            logger.debug("Transcripción obtenida: %s", transcript)
            return transcript if transcript else "[No se pudo transcribir el audio]"
        except FileNotFoundError as e:
            logger.error("Archivo de audio no encontrado: %s", e)
        except GoogleAPICallError as e:
            logger.error("Error en la llamada a la API de Google Speech: %s", e)
            return "[Error en la llamada a la API de Google Speech]"
