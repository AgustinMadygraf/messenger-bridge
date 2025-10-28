"""
Path: src/use_cases/generate_agent_response_use_case.py

Caso de uso para generar respuesta con Rasa.
"""

from src.shared.logger import get_logger

from src.entities.message import Message

logger = get_logger("generate-agent-response-use-case")

class GenerateAgentResponseUseCase:
    "Orquesta la generación de respuestas usando el servicio Rasa."
    def __init__(self, agent_bot_service, audio_transcriber_use_case=None):
        self.agent_bot_service = agent_bot_service
        self.audio_transcriber_use_case = audio_transcriber_use_case


    def execute(self, _conversation_id: str, user_message: Message, prompt: str = None) -> Message:
        "Genera una respuesta para el mensaje del usuario. El prompt puede ser texto transcripto si el mensaje es de audio."
        if prompt is not None:
            agent_bot_response = self.agent_bot_service.get_response(prompt)
        else:
            agent_bot_response = self.agent_bot_service.get_response(user_message.body)
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
