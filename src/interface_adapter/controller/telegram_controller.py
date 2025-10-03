"""
Path: src/interface_adapter/controller/telegram_controller.py
"""

from src.entities.message import Message

class TelegramMessageController:
    "Controlador para manejar mensajes entrantes de Telegram usando Rasa."
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    async def handle(self, chat_id, text, entities=None):
        "Maneja un mensaje entrante de Telegram y genera una respuesta usando Rasa."
        # Procesar entidades para preservar formato
        formatted_text = self._apply_markdown_formatting(text, entities) if entities else text
        print(f"[CONTROLLER] chat_id: {chat_id}, texto con formato: {formatted_text}")

        user_message = Message(to=chat_id, body=formatted_text)
        response_message = self.use_case.execute(chat_id, user_message)
        print(f"[CONTROLLER] Respuesta final: {response_message.body}")
        response_text = response_message.body.strip() if response_message.body else "No tengo una respuesta en este momento."
        return chat_id, response_text

    def _apply_markdown_formatting(self, text, entities):
        """Convierte las entidades de Telegram a formato Markdown."""
        if not entities:
            return text

        # Ordenar entidades por posición para procesarlas correctamente
        sorted_entities = sorted(entities, key=lambda e: e['offset'])

        # Texto resultante con marcadores markdown
        result = ""
        last_index = 0

        for entity in sorted_entities:
            offset = entity['offset']
            length = entity['length']
            type_ = entity['type']

            # Añadir texto previo a la entidad
            result += text[last_index:offset]

            # Añadir marcadores según tipo
            if type_ == 'bold':
                result += f"**{text[offset:offset+length]}**"
            elif type_ == 'italic':
                result += f"*{text[offset:offset+length]}*"
            # Añadir más tipos según necesidad
            else:
                result += text[offset:offset+length]

            last_index = offset + length

        # Añadir texto restante
        result += text[last_index:]
        return result
