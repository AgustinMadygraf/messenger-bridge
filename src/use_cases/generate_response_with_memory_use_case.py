"""
Path: src/use_cases/generate_response_with_memory_use_case.py
"""

from src.entities.conversation_manager import ConversationManager
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase

class GenerateResponseWithMemoryUseCase:
    """
    Orquesta la generación de respuestas usando historial de conversación y modelo generativo.
    """
    def __init__(self, conversation_manager: ConversationManager, gemini_use_case: GenerateGeminiResponseUseCase, system_instructions: str = None):
        self.conversation_manager = conversation_manager
        self.gemini_use_case = gemini_use_case
        self.system_instructions = system_instructions

    def execute(self, conversation_id: str, sender: str, user_message: str) -> str:
        # Actualiza el historial
        self.conversation_manager.add_message(conversation_id, {"sender": sender, "message": user_message})
        # Construye el prompt con historial
        history = self.conversation_manager.get_history(conversation_id)
        prompt = "\n".join(f"{m['sender']}: {m['message']}" for m in history)
        # Genera la respuesta con Gemini
        response = self.gemini_use_case.execute(prompt, system_instructions=self.system_instructions)
        # Agrega la respuesta del bot al historial
        self.conversation_manager.add_message(conversation_id, {"sender": "Bot", "message": response})
        return response