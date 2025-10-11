"""
Path: run_transcriber.py
"""

import argparse
from colorama import init, Fore, Style

from src.shared.logger import get_logger
from src.infrastructure.audio.local_audio_transcriber import LocalAudioTranscriber

logger = get_logger("run-transcriber")
init(autoreset=True)

def main():
    "Entry point for the audio transcription script."
    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}Transcribe un archivo de audio usando Messenger Bridge{Style.RESET_ALL}"
    )
    parser.add_argument(
        "--audio", "-a",
        help=f"{Fore.YELLOW}Ruta del archivo de audio a transcribir{Style.RESET_ALL}",
        required=True
    )
    args = parser.parse_args()
    audio_file_path = args.audio

    print(f"{Fore.GREEN}🔊 Iniciando transcripción para: {audio_file_path}{Style.RESET_ALL}")
    try:
        LocalAudioTranscriber.run_from_cli(audio_file_path)
        print(f"{Fore.GREEN}✅ Transcripción finalizada.{Style.RESET_ALL}")
    except FileNotFoundError as e:
        print(f"{Fore.RED}❌ Archivo no encontrado: {e}{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}❌ Valor inválido: {e}{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}❌ Error de sistema operativo: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
