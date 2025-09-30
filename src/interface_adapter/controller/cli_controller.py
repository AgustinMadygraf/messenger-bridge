"""
Path: src/interface_adapter/controller/cli_controller.py
"""

from src.entities.message import Message

class CliMessageController:
    "Controlador para orquestar la interacción CLI con el caso de uso y el presentador."
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    def handle(self, conversation_id: str, user_input: str) -> str:
        """
        Procesa el mensaje del usuario, obtiene la respuesta del caso de uso
        y la presenta en formato CLI.
        """
        user_message = Message(to=conversation_id, body=user_input)
        response_message = self.use_case.execute(conversation_id, user_message)
        return self.presenter.present(response_message)
