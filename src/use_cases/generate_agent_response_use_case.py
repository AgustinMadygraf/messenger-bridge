"""
Path: src/use_cases/generate_agent_response_use_case.py

Caso de uso para generar respuesta con Rasa.
"""

from src.entities.message import Message

class GenerateAgentResponseUseCase:
    "Orquesta la generación de respuestas usando el servicio Rasa."
    def __init__(self, agent_bot_service):
        self.agent_bot_service = agent_bot_service

    def execute(self, _conversation_id: str, user_message: Message) -> Message:
        " Genera una respuesta de Rasa para el mensaje del usuario."
        print(f"[USECASE] Mensaje recibido: {user_message.body}")
        prompt = user_message.body
        agent_bot_response = self.agent_bot_service.get_response(prompt)
        print(f"[USECASE] Respuesta de Rasa: {agent_bot_response}")

        # Detecta error de conexión y responde amigablemente
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
