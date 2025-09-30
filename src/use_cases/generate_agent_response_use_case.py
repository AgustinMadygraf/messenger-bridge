"""
Path: src/use_cases/generate_agent_response_use_case.py

Caso de uso para generar respuesta con Rasa.
"""

from src.entities.conversation_manager import ConversationManager
from src.entities.message import Message

class GenerateAgentResponseUseCase:
    "Orquesta la generación de respuestas usando el servicio Rasa."
    def __init__(self, rasa_service, conversation_manager: ConversationManager):
        self.rasa_service = rasa_service
        self.conversation_manager = conversation_manager

    def execute(self, conversation_id: str, user_message: Message) -> Message:
        " Genera una respuesta de Rasa para el mensaje del usuario."
        print(f"[USECASE] Mensaje recibido: {user_message.body}")  # Depuración
        self.conversation_manager.add_message(conversation_id, user_message)
        prompt = user_message.body
        rasa_response = self.rasa_service.get_response(prompt)
        print(f"[USECASE] Respuesta de Rasa: {rasa_response}")  # Depuración

        # Detecta error de conexión y responde amigablemente
        if isinstance(rasa_response, str) and "Error al comunicarse con Rasa" in rasa_response:
            friendly_message = (
                "Lo sentimos, el servidor no está disponible en este momento. "
                "Por favor, comuníquese con el área de mantenimiento."
            )
            response_body = friendly_message
        else:
            response_body = rasa_response

        response_message = Message(
            to=user_message.to,
            body=response_body
        )
        self.conversation_manager.add_message(conversation_id, response_message)
        return response_message
