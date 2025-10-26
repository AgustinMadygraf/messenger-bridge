"""
Path: src/interface_adapter/presenters/message_splitter.py
"""

class MessageSplitter:
    "Presenter para dividir mensajes largos en partes más pequeñas."
    def split(self, text: str, max_len: int) -> list:
        "Divide el texto en partes más pequeñas que cumplan con el límite de longitud."
        if not text:
            return []
        return [text[i:i+max_len] for i in range(0, len(text), max_len)]
