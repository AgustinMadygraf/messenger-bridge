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

from src.entities.audio_transcriber import AudioTranscription
from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase
from src.interface_adapter.gateways.audio_transcriber_gateway import AudioTranscriberGateway
from src.interface_adapter.presenters.audio_transcriber_presenter import AudioTranscriberPresenter

class LocalAudioTranscriber(AudioTranscriberUseCase):
    """
    Implementación concreta del caso de uso para transcribir audio localmente usando Vosk (offline) y Google (fallback).
    Depende del gateway para obtener el archivo y del presenter para formatear la salida.
    """

    def __init__(self, gateway: AudioTranscriberGateway, presenter: AudioTranscriberPresenter, vosk_model_path: str = "model"):
        self.gateway = gateway
        self.presenter = presenter
        self.vosk_enabled = (
            Model is not None and KaldiRecognizer is not None and os.path.isdir(vosk_model_path)
        )
        if self.vosk_enabled:
            self.vosk_model = Model(vosk_model_path)
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        "Transcribe un archivo de audio OGG y devuelve un objeto AudioTranscription."
        # Usa el gateway para obtener la ruta real del archivo
        audio_file_path = self.gateway.get_audio_file(audio_file_path)

        if not os.path.isfile(audio_file_path):
            transcription = AudioTranscription(text=f"El archivo {audio_file_path} no existe.", source_path=audio_file_path)
            return transcription

        wav_path = audio_file_path + ".wav"
        try:
            audio = AudioSegment.from_ogg(audio_file_path)
            audio.export(wav_path, format="wav")
        except (FileNotFoundError, CouldntDecodeError, OSError, ValueError, TypeError) as e:
            transcription = AudioTranscription(text=f"Error en la conversión: {e}", source_path=audio_file_path)
            return transcription

        text = None

        # Intentar con Vosk (offline)
        if self.vosk_enabled:
            try:
                wf = wave.open(wav_path, "rb")
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                    # Vosk requiere WAV PCM 16bit mono
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
                    text = "Vosk no pudo transcribir el audio."
            except (wave.Error, OSError, ValueError, json.JSONDecodeError) as e:
                text = f"Error usando Vosk: {e}"

        # Si Vosk falla o no está disponible, usar Google (requiere Internet)
        if not text or text.startswith("Error usando Vosk"):
            try:
                with sr.AudioFile(wav_path) as source:
                    audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="es-ES")
            except sr.UnknownValueError:
                text = "Audio unintelligible"
            except sr.RequestError as e:
                text = f"Could not request results from Google Speech Recognition service; {e}"

        if os.path.exists(wav_path):
            os.remove(wav_path)

        transcription = AudioTranscription(text=text, source_path=audio_file_path)
        return transcription
