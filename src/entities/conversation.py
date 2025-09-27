"""
Path: src/entities/conversation.py
"""

class Conversation:
    "Gestiona el historial de mensajes de una conversación."
    def __init__(self):
        self.history = []

    def add_message(self, sender: str, message: str):
        "Agrega un mensaje al historial."
        self.history.append({"sender": sender, "message": message})

    def get_history(self):
        "Devuelve el historial completo como lista."
        return self.history

    def clear(self):
        "Limpia el historial de la conversación."
        self.history.clear()

    def get_prompt(self):
        "Devuelve el historial como un solo string para modelos generativos."
        return "\n".join(f"{m['sender']}: {m['message']}" for m in self.history)
