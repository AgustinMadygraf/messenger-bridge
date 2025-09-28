"""
Path: src/interface_adapter/controller/gemini_controller.py
"""

from src.entities.conversation import Conversation
from src.entities.message import Message

class GeminiController:
    "Controlador para orquestar la interacción entre la entrada del usuario y el caso de uso, gestionando el historial."
    def __init__(self, use_case, conversation=None):
        self.use_case = use_case
        self.conversation = conversation or Conversation()

    def handle_user_message(self, user_message):
        "Agrega el mensaje del usuario, genera el prompt y retorna la respuesta del caso de uso."
        user_msg = Message(to="Usuario", body=user_message)
        self.conversation.add_message(user_msg)
        prompt = self.conversation.get_prompt()
        try:
            response = self.use_case.execute(prompt)
            bot_msg = Message(to="Bot", body=response)
            self.conversation.add_message(bot_msg)
            return response
        except ValueError as e:
            return f"Error: {e}"

    def handle_prompt(self, prompt):
        "Recibe un prompt completo, ejecuta el caso de uso y agrega la respuesta al historial."
        try:
            response = self.use_case.execute(prompt)
            bot_msg = Message(to="Bot", body=response)
            self.conversation.add_message(bot_msg)
            return response
        except ValueError as e:
            return f"Error: {e}"

    def clear_conversation(self):
        "Limpia el historial de la conversación."
        self.conversation.clear()
