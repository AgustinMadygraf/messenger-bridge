"""
Path: src/interface_adapter/controller/incoming_message_controller.py
"""


class IncomingMessageController:
    "Controlador para manejar mensajes entrantes."
    def __init__(self, use_case, conversation):
        self.use_case = use_case
        self.conversation = conversation

    def handle(self, _from_number, user_message):
        "Procesa el mensaje entrante y retorna la respuesta generada."
        self.conversation.add_message(user_message)
        prompt = self.conversation.get_prompt()
        response = self.use_case.execute(prompt)
        return response
