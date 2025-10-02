"""
Path: run_transcriber.py
"""

from src.infrastructure.audio.local_audio_transcriber import TranscriberApp

if __name__ == "__main__":
    app = TranscriberApp()
    app.run()
