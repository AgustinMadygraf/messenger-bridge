"""
Path: src/interface_adapter/controller/telegram_message_controller.py
"""

from src.entities.message import Message

class TelegramMessageController:
    "Controlador para manejar mensajes entrantes de Telegram."
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    async def handle(self, chat_id, text):
        "Maneja un mensaje entrante de Telegram usando memoria conversacional y Gemini."
        response = self.use_case.execute(
            conversation_id=str(chat_id),
            sender="User",
            user_message=text
        )
        # Envolver la respuesta en un objeto Message
        message = Message(to="Bot", body=response)
        return chat_id, self.presenter.present(message)
