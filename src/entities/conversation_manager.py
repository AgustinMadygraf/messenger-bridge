"""
Path: src/entities/conversation_manager.py
"""

from typing import Dict, List, Any

class ConversationManager:
    " Gestiona múltiples conversaciones identificadas por un ID único."
    def __init__(self):
        self._conversations: Dict[str, List[Any]] = {}

    def add_message(self, conversation_id: str, message: Any) -> None:
        "Agrega un mensaje a la conversación especificada."
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []
        self._conversations[conversation_id].append(message)

    def get_history(self, conversation_id: str) -> List[Any]:
        "Obtiene el historial de mensajes de la conversación especificada."
        return self._conversations.get(conversation_id, [])

    def clear_history(self, conversation_id: str) -> None:
        "Limpia el historial de mensajes de la conversación especificada."
        if conversation_id in self._conversations:
            self._conversations[conversation_id] = []

    def remove_conversation(self, conversation_id: str) -> None:
        "Elimina completamente una conversación."
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
