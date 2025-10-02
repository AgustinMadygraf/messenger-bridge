"""
Path: run_transcriber.py
"""

import os
from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber
from src.interface_adapter.gateways.audio_transcriber_gateway import AudioTranscriberGateway
from src.interface_adapter.presenters.audio_transcriber_presenter import AudioTranscriberPresenter
from src.interface_adapter.controller.audio_transcriber_controller import AudioTranscriberController

class LocalFileAudioGateway(AudioTranscriberGateway):
    """
    Gateway concreto para obtener archivos locales.
    """
    def get_audio_file(self, audio_file_path: str) -> str:
        return audio_file_path

class TranscriberApp:
    "Clase principal para ejecutar el proceso de transcripción de archivos OGG."

    def run(self):
        "Inicia el proceso de transcripción."
        ogg_file_path = input("Please enter the path of the OGG file: ")

        if not os.path.isfile(ogg_file_path):
            print("The specified file does not exist. Please check the path and try again.")
            return

        gateway = LocalFileAudioGateway()
        presenter = AudioTranscriberPresenter()
        use_case = LocalAudioTranscriber(gateway, presenter)
        controller = AudioTranscriberController(use_case)

        transcription = controller.transcribe(ogg_file_path)
        print("Transcription Result:")
        print(presenter.present(transcription))

if __name__ == "__main__":
    app = TranscriberApp()
    app.run()
