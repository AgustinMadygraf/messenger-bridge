"""
Path: run_transcriber.py
"""

import os
from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber

class TranscriberApp:
    "Clase principal para ejecutar el proceso de transcripción de archivos OGG."

    def run(self):
        ogg_file_path = input("Please enter the path of the OGG file: ")

        if not os.path.isfile(ogg_file_path):
            print("The specified file does not exist. Please check the path and try again.")
            return

        transcriber = LocalAudioTranscriber()
        transcription = transcriber.transcribe_and_present(ogg_file_path)
        print("Transcription Result:")
        print(transcription)

if __name__ == "__main__":
    app = TranscriberApp()
    app.run()
