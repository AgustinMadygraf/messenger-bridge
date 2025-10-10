"""
Path: run_transcriber.py
"""

import argparse

from src.shared.logger import get_logger

from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber

logger = get_logger("run-transcriber")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe un archivo de audio.")
    parser.add_argument("--audio", "-a", help="Ruta del archivo de audio a transcribir")
    args = parser.parse_args()
    audio_file_path = args.audio
    LocalAudioTranscriber.run_from_cli(audio_file_path)
