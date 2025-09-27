"""
Path: src/interface_adapter/controller/incoming_message_controller.py
"""

from src.use_cases.process_incoming_message_use_case import ProcessIncomingMessageUseCase

class IncomingMessageController:
    "Controlador para manejar mensajes entrantes."
    def __init__(self, use_case: ProcessIncomingMessageUseCase):
        self.use_case = use_case

    def handle(self, from_number: str, user_message: str) -> str:
        "Orquesta el procesamiento del mensaje entrante."
        return self.use_case.execute(from_number, user_message)
