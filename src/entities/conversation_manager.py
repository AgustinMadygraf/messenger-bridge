"""
Path: src/entities/conversation_manager.py
"""

from typing import Dict
from src.entities.conversation import Conversation
from src.entities.message import Message

class ConversationManager:
    "Gestiona múltiples conversaciones identificadas por un ID único."
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}

    def add_message(self, conversation_id: str, message: Message) -> None:
        "Agrega un mensaje Message a la conversación especificada."
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = Conversation(conversation_id)
        self._conversations[conversation_id].add_message(message)

    def get_history(self, conversation_id: str):
        "Obtiene el historial de mensajes Message de la conversación especificada."
        if conversation_id in self._conversations:
            return self._conversations[conversation_id].get_history()
        return []

    def clear_history(self, conversation_id: str) -> None:
        "Limpia el historial de mensajes de la conversación especificada."
        if conversation_id in self._conversations:
            self._conversations[conversation_id].clear()

    def remove_conversation(self, conversation_id: str) -> None:
        "Elimina completamente una conversación."
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
