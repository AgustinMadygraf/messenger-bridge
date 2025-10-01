"""
Path: src/infrastructure/audio/local_audio_transcriber.py
"""

import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from src.entities.audio_transcriber import AudioTranscription
from src.interface_adapter.gateways.audio_transcriber_gateway import AudioTranscriberGateway
from src.interface_adapter.presenters.audio_transcriber_presenter import AudioTranscriberPresenter
from src.interface_adapter.controller.audio_transcriber_controller import AudioTranscriberController
from src.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase

class LocalAudioTranscriberGateway(AudioTranscriberGateway):
    def get_audio_file(self, audio_file_path: str) -> str:
        if not os.path.isfile(audio_file_path):
            raise FileNotFoundError(f"The file {audio_file_path} does not exist.")
        return audio_file_path

class LocalAudioTranscriberUseCase(AudioTranscriberUseCase):
    def __init__(self, gateway: AudioTranscriberGateway):
        self.gateway = gateway

    def transcribe(self, audio_file_path: str) -> AudioTranscription:
        audio_file_path = self.gateway.get_audio_file(audio_file_path)
        wav_path = audio_file_path + ".wav"
        try:
            audio = AudioSegment.from_ogg(audio_file_path)
            audio.export(wav_path, format="wav")
        except (FileNotFoundError, CouldntDecodeError, OSError, ValueError, TypeError) as e:
            return AudioTranscription(text=f"Error en la conversión: {e}", source_path=audio_file_path)

        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="es-ES")
        except sr.UnknownValueError:
            text = "Audio unintelligible"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"
        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

        return AudioTranscription(text=text, source_path=audio_file_path)

class LocalAudioTranscriber:
    """
    Clase que orquesta la transcripción de audio local, usando controller y presenter.
    """

    def __init__(self):
        gateway = LocalAudioTranscriberGateway()
        use_case = LocalAudioTranscriberUseCase(gateway)
        self.controller = AudioTranscriberController(use_case)
        self.presenter = AudioTranscriberPresenter()

    def transcribe_and_present(self, audio_file_path: str) -> str:
        """
        Transcribe el archivo OGG y devuelve el resultado formateado.
        """
        transcription = self.controller.transcribe(audio_file_path)
        return self.presenter.present(transcription)