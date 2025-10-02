"""
Path: src/infrastructure/audio/local_audio_transcriber.py
"""

import os
import wave
import json
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from src.shared.logger import get_logger

from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase
from src.entities.audio_transcriber import AudioTranscription

logger = get_logger("local-audio-transcriber")

class LocalAudioTranscriber(AudioTranscriberUseCase):
    """
    Implementación concreta del caso de uso para transcribir audio localmente usando 
    Vosk (offline) y Google (fallback).
    """

    def __init__(self, vosk_model_path: str = "model"):
        self.vosk_enabled = (
            Model is not None and KaldiRecognizer is not None and os.path.isdir(vosk_model_path)
        )
        if self.vosk_enabled:
            logger.info("Modelo Vosk encontrado en %s.", vosk_model_path)
            self.vosk_model = Model(vosk_model_path)
        else:
            logger.warning("Vosk no está disponible o el modelo no se encontró.")
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
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
            audio = AudioSegment.from_file(audio_file_path)
            audio.export(wav_path, format="wav")
        except (FileNotFoundError, CouldntDecodeError, OSError, ValueError, TypeError) as e:
            logger.error("Error en la conversión a WAV: %s", e)
            return AudioTranscription(
                text=f"Error en la conversión: {e}",
                source_path=audio_file_path
            )

        text = None

        # Intentar con Vosk (offline)
        if self.vosk_enabled:
            try:
                logger.info("Intentando transcripción offline con Vosk...")
                wf = wave.open(wav_path, "rb")
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                    logger.debug("Ajustando WAV a formato PCM 16bit mono para Vosk.")
                    audio = AudioSegment.from_wav(wav_path).set_channels(1).set_sample_width(2)
                    audio.export(wav_path, format="wav")
                    wf = wave.open(wav_path, "rb")
                rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
                vosk_result = ""
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        vosk_result += rec.Result()
                vosk_result += rec.FinalResult()
                result_json = json.loads(vosk_result.split('\n')[-2] if '\n' in vosk_result else vosk_result)
                text = result_json.get("text", "").strip()
                if not text:
                    logger.warning("Vosk no pudo transcribir el audio.")
                    text = "Vosk no pudo transcribir el audio."
                else:
                    logger.info("Transcripción exitosa con Vosk.")
            except (wave.Error, OSError, ValueError, json.JSONDecodeError) as e:
                logger.error("Error usando Vosk: %s", e)
                text = f"Error usando Vosk: {e}"

        # Si Vosk falla o no está disponible, usar Google (requiere Internet)
        if not text or text.startswith("Error usando Vosk"):
            try:
                logger.info("Intentando transcripción online con Google Speech Recognition...")
                with sr.AudioFile(wav_path) as source:
                    audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="es-ES")
                logger.info("Transcripción exitosa con Google Speech Recognition.")
            except sr.UnknownValueError:
                logger.warning("Google Speech Recognition no pudo entender el audio.")
                text = "Audio unintelligible"
            except sr.RequestError as e:
                logger.critical("No se pudo conectar con Google Speech Recognition: %s", e)
                text = f"Could not request results from Google Speech Recognition service; {e}"

        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
                logger.debug("Archivo temporal eliminado: %s", wav_path)
            except OSError as e:
                logger.warning("No se pudo eliminar el archivo temporal %s: %s", wav_path, e)

        transcription = AudioTranscription(text=text, source_path=audio_file_path)
        logger.info("Transcripción finalizada para %s: %s", audio_file_path, text)
        return transcription
