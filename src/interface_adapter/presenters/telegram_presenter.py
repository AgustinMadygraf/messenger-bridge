"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram con soporte para Markdown V2."
    def present(self, message: Message) -> dict:
        """
        Presenta la respuesta escapando correctamente para MarkdownV2.
        Retorna un diccionario compatible con la API de Telegram.
        """
        # Primero convertimos al formato de Telegram y luego escapamos
        telegram_format = self._convert_to_telegram_markdown(message.body)
        escaped_text = self._escape_markdown_v2(telegram_format)
        return {
            "text": escaped_text,
            "parse_mode": "MarkdownV2"
        }

    def _convert_to_telegram_markdown(self, text: str) -> str:
        """
        Convierte el formato markdown estándar al formato específico de Telegram MarkdownV2.
        """
        # Convertir **texto** (markdown común) a *texto* (Telegram)
        result = ""
        i = 0
        while i < len(text):
            # Si encontramos '**', lo reemplazamos por '*' para formato de Telegram
            if i < len(text) - 1 and text[i:i+2] == "**":
                result += "*"
                i += 2
            else:
                result += text[i]
                i += 1
        return result

    def _escape_markdown_v2(self, text: str) -> str:
        """
        Escapa los caracteres especiales de MarkdownV2 preservando los formatos.
        """
        special_chars = ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+', 
                        '-', '=', '|', '{', '}', '.', '!', '\\']
        
        result = ""
        in_format = False
        
        i = 0
        while i < len(text):
            if text[i] == '*':
                # No escapar asteriscos que son parte del formato
                result += '*'
                in_format = not in_format
            elif in_format:
                # Dentro de formato (entre asteriscos) no escapamos
                result += text[i]
            else:
                # Fuera de formato, escapamos caracteres especiales
                if text[i] in special_chars:
                    result += '\\' + text[i]
                else:
                    result += text[i]
            i += 1
            
        return result
