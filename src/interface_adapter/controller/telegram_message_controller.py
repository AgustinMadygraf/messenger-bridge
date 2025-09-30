"""
Path: src/interface_adapter/controller/telegram_message_controller.py

Controlador para manejar mensajes entrantes de Telegram usando Rasa.
"""

from src.entities.message import Message

class TelegramMessageController:
    "Controlador para manejar mensajes entrantes de Telegram usando Rasa."
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    async def handle(self, chat_id, text):
        print(f"[CONTROLLER] chat_id: {chat_id}, texto: {text}")  # Depuración
        user_message = Message(to=chat_id, body=text)
        response_message = self.use_case.execute(chat_id, user_message)
        print(f"[CONTROLLER] Respuesta final: {response_message.body}")  # Depuración
        response_text = response_message.body.strip() if response_message.body else "No tengo una respuesta en este momento."
        return chat_id, response_text
