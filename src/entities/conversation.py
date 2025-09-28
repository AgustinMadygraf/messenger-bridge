"""
Path: src/entities/conversation.py
"""

from typing import List, Optional
from src.entities.message import Message

class Conversation:
    "Representa una conversación con un historial de mensajes."
    def __init__(self, conversation_id: Optional[str] = None):
        self.conversation_id = conversation_id
        self.history: List[Message] = []

    def add_message(self, message: Message) -> None:
        "Agrega un mensaje Message al historial."
        self.history.append(message)

    def get_history(self) -> List[Message]:
        "Devuelve el historial completo como lista de Message."
        return self.history

    def clear(self) -> None:
        "Limpia el historial de la conversación."
        self.history.clear()

    def get_prompt(self) -> str:
        "Devuelve el historial como un solo string para modelos generativos."
        return "\n".join(
            f"{msg.to}: {msg.body}" + (f" [media: {msg.media_url}]" if msg.is_media() else "")
            for msg in self.history
        )
