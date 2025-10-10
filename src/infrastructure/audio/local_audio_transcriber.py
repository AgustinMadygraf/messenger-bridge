"""
Path: src/infrastructure/audio/local_audio_transcriber.py
"""

import os

from src.shared.logger import get_logger

from src.infrastructure.audio.vosk.vosk_transcriber import VoskTranscriber
from src.infrastructure.audio.pydub.pydub_converter import PydubConverter
from src.infrastructure.audio.speech_recognition.speech_recognition_transcriber import SpeechRecognitionTranscriber
from src.interface_adapter.controller.audio_transcriber_controller import AudioTranscriberController
from src.interface_adapter.gateways.audio_transcriber_gateway import AudioTranscriberGateway
from src.entities.audio_transcriber import AudioTranscription

logger = get_logger("local-audio-transcriber")

class LocalAudioTranscriber(AudioTranscriberGateway):
    "Transcriptor de audio local que usa Vosk (offline) y SpeechRecognition (Google, online) como fallback."
    def __init__(self, vosk_model_path: str = "model"):
        self.vosk_transcriber = VoskTranscriber(vosk_model_path)
        self.speech_recognition_transcriber = SpeechRecognitionTranscriber()

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        "Transcribe el archivo de audio especificado"
        logger.info("Iniciando transcripción para: %s", audio_file_path)
        if not os.path.isfile(audio_file_path):
            logger.error("El archivo %s no existe.", audio_file_path)
            return AudioTranscription(
                text=f"El archivo {audio_file_path} no existe.",
                source_path=audio_file_path
            )

        wav_path = audio_file_path + ".wav"
        try:
            logger.debug("Convirtiendo %s a WAV temporal: %s", audio_file_path, wav_path)
            if not PydubConverter.to_wav(audio_file_path, wav_path):
                return AudioTranscription(
                    text=f"Error en la conversión: No se pudo convertir {audio_file_path} a WAV.",
                    source_path=audio_file_path
                )
        except (FileNotFoundError, OSError, ValueError, TypeError) as e:
            logger.error("Error en la conversión a WAV: %s", e)
            return AudioTranscription(
                text=f"Error en la conversión: {e}",
                source_path=audio_file_path
            )

        # Intentar con Vosk (offline)
        text = None
        if self.vosk_transcriber.vosk_enabled:
            text = self.vosk_transcriber.transcribe(wav_path)

        # Si Vosk falla o no está disponible, usar SpeechRecognitionTranscriber (Google)
        if not text or (isinstance(text, str) and text.startswith("Error usando Vosk")):
            text = self.speech_recognition_transcriber.transcribe(wav_path, language="es-ES")

        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
                logger.debug("Archivo temporal eliminado: %s", wav_path)
            except OSError as e:
                logger.warning("No se pudo eliminar el archivo temporal %s: %s", wav_path, e)

        transcription = AudioTranscription(text=text, source_path=audio_file_path)
        logger.info("Transcripción finalizada para %s: %s", audio_file_path, text)
        return transcription

    @classmethod
    def run_from_cli(cls, audio_file_path: str = None):
        "Método de clase para ejecutar la transcripción desde la línea de comandos."
        if not audio_file_path:
            audio_file_path = input("Ingrese la ruta del archivo de audio: ")

        try:
            use_case = cls()
            controller = AudioTranscriberController(use_case)
            transcription = controller.transcribe_audio(audio_file_path)
            logger.info("Transcripción: %s", transcription.text)
        except FileNotFoundError as e:
            logger.error("No se encontró el archivo: %s", e)
        except PermissionError as e:
            logger.error("No se tienen permisos para acceder al archivo: %s", e)
        except OSError as e:
            logger.error("Ocurrió un error de sistema durante la transcripción: %s", e)
