"""
Path: src/infrastructure/audio/speech_recognition/speech_recognition_transcriber.py
"""

import speech_recognition as sr

from src.shared.logger import get_logger

logger = get_logger("speech-recognition-transcriber")

class SpeechRecognitionTranscriber:
    "Transcriptor de audio usando Google Speech Recognition (requiere Internet)."
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, wav_path: str, language: str = "es-ES") -> str:
        "Transcribe un archivo WAV usando Google Speech Recognition."
        try:
            logger.info("Intentando transcripción online con Google Speech Recognition...")
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio_data, language=language)
            logger.info("Transcripción exitosa con Google Speech Recognition.")
            return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition no pudo entender el audio.")
            return "Audio unintelligible"
        except sr.RequestError as e:
            logger.critical("No se pudo conectar con Google Speech Recognition: %s", e)
            return f"Could not request results from Google Speech Recognition service; {e}"
        except (OSError, ValueError) as e:
            logger.error("Error usando Google Speech Recognition: %s", e)
            return f"Error usando Google Speech Recognition: {e}"
