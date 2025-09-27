"""
Path: src/interface_adapter/controller/incoming_message_controller.py
"""


class IncomingMessageController:
    "Controlador para manejar mensajes entrantes."
    def __init__(self, use_case, conversation):
        self.use_case = use_case
        self.conversation = conversation

    def handle(self, from_number: str, user_message: str) -> str:
        "Orquesta el procesamiento del mensaje entrante."
        self.conversation.add_message(str(from_number), user_message)
        prompt = self.conversation.get_prompt()
        response = self.use_case.execute(prompt)
        self.conversation.add_message("Bot", response)
        return response
