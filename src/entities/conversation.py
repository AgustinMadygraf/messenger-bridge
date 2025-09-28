"""
Path: src/entities/conversation.py
"""

from typing import List, Dict

class Conversation:
    "Representa una conversación con un historial de mensajes."
    def __init__(self, conversation_id: str = None):
        self.conversation_id = conversation_id
        self.history: List[Dict[str, str]] = []

    def add_message(self, sender: str, message: str) -> None:
        "Agrega un mensaje al historial."
        self.history.append({"sender": sender, "message": message})

    def get_history(self) -> List[Dict[str, str]]:
        "Devuelve el historial completo como lista."
        return self.history

    def clear(self) -> None:
        "Limpia el historial de la conversación."
        self.history.clear()

    def get_prompt(self) -> str:
        "Devuelve el historial como un solo string para modelos generativos."
        return "\n".join(f"{m['sender']}: {m['message']}" for m in self.history)
