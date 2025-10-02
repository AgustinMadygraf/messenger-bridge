"""
Path: run_transcriber.py
"""

from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber

if __name__ == "__main__":
    app = LocalAudioTranscriber()
    audio_file_path = input("Ingrese la ruta del archivo de audio: ")
    app.transcribe(audio_file_path)
