"""
Path: speech.py
"""

from src.infrastructure.google_cloud_speech.speech_service import SpeechService
from src.use_cases.transcribe_audio_use_case import TranscribeAudioUseCase
from src.interface_adapter.controller.transcribe_audio_controller import TranscribeAudioController

try:
    # Instancia el servicio y el caso de uso
    speech_service = SpeechService()
    use_case = TranscribeAudioUseCase(speech_service)
    controller = TranscribeAudioController(use_case)

    # Ruta de ejemplo al archivo de audio
    TEST_AUDIO_FILE_PATH = input("Ingrese la ruta del archivo de audio para transcribir: ")

    # Ejecuta la transcripción usando el controlador
    resultado = controller.handle(TEST_AUDIO_FILE_PATH)
    print(resultado)
except FileNotFoundError as e:
    # Si falta el archivo de credenciales, muestra un mensaje estructurado
    print({
        "status": "error",
        "transcription": "",
        "language": "es-AR",
        "error_message": str(e)
    })
