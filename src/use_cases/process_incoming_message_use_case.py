"""
Path: src/use_cases/process_incoming_message_use_case.py
"""

from src.entities.message import Message

class ProcessIncomingMessageUseCase:
    "Caso de uso para procesar mensajes entrantes y generar respuestas."
    def __init__(self, conversation):
        self.conversation = conversation

    def execute(self, from_number: str, user_message: str) -> str:
        "Procesa el mensaje entrante y devuelve una respuesta."
        # Usar Message en vez de string
        self.conversation.add_message(Message(to=str(from_number), body=user_message))
        response_text = f"Recibido tu mensaje '{user_message}'. Esta es una respuesta simulada."
        self.conversation.add_message(Message(to="Bot", body=response_text))
        return response_text
