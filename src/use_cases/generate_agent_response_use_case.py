"""
Path: src/use_cases/generate_agent_response_use_case.py

Caso de uso para generar respuesta con Rasa.
"""

import os
import tempfile
import requests
from requests.auth import HTTPBasicAuth

from src.shared.config import get_config

from src.entities.message import Message

class GenerateAgentResponseUseCase:
    "Orquesta la generación de respuestas usando el servicio Rasa."
    def __init__(self, agent_bot_service, audio_transcriber_use_case=None):
        self.agent_bot_service = agent_bot_service
        self.audio_transcriber_use_case = audio_transcriber_use_case

    def execute(self, _conversation_id: str, user_message: Message) -> Message:
        "Genera una respuesta para el mensaje del usuario."
        print(f"[USECASE] Mensaje recibido: {user_message.body}")

        config = get_config()
        # Si el mensaje tiene contenido multimedia de audio, transcribir antes de enviar
        if (
            user_message.is_media()
            and user_message.media_type
            and "audio" in user_message.media_type
            and self.audio_transcriber_use_case
        ):
            # Descargar el archivo de audio desde la URL (requiere helper externo)
            try:
                auth = HTTPBasicAuth(config['ACCOUNT_SID'], config['AUTH_TOKEN'])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_file:
                    audio_resp = requests.get(user_message.media_url, auth=auth, timeout=20)
                    audio_resp.raise_for_status()
                    tmp_file.write(audio_resp.content)
                    tmp_file_path = tmp_file.name

                transcription = self.audio_transcriber_use_case.transcribe(tmp_file_path)
                os.remove(tmp_file_path)
            except (requests.RequestException, OSError) as e:
                transcription = None
                print(f"[USECASE] Error al descargar/transcribir audio: {e}")

            if transcription and not transcription.is_empty():
                prompt = transcription.text
            else:
                prompt = "[No se pudo transcribir el audio. Enviando audio original.]"
            agent_bot_response = self.agent_bot_service.get_response(prompt)
        else:
            prompt = user_message.body
            agent_bot_response = self.agent_bot_service.get_response(prompt)

        print(f"[USECASE] Respuesta de Rasa: {agent_bot_response}")

        if isinstance(agent_bot_response, str) and "Error al comunicarse con Rasa" in agent_bot_response:
            friendly_message = (
                "Lo sentimos, el servidor no está disponible en este momento. "
                "Por favor, comuníquese con el área de mantenimiento."
            )
            response_body = friendly_message
        else:
            response_body = agent_bot_response

        response_message = Message(
            to=user_message.to,
            body=response_body
        )
        return response_message
