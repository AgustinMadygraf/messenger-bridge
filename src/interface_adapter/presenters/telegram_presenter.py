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
        # Caracteres que requieren escape en MarkdownV2
        special_chars = ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+',
                        '-', '=', '|', '{', '}', '.', '!', '\\']

        # Primero identificamos todos los pares de asteriscos para formato bold
        format_positions = []
        for i, char in enumerate(text):
            if char == '*':
                # Verificar si es parte de una lista de viñetas (bullet point)
                # Un asterisco que es bullet point generalmente tiene espacio después
                if i > 0 and text[i-1] == '\n' and i < len(text)-1 and text[i+1] == ' ':
                    continue  # Ignorar asteriscos de viñetas
                format_positions.append(i)

        # Resultado final con escapes
        result = ""
        in_bold = False
        for i, char in enumerate(text):
            # Si es un marcador de formato bold
            if i in format_positions:
                in_bold = not in_bold
                result += '*'
            # Si es un asterisco de viñeta, escaparlo
            elif char == '*' and i > 0 and text[i-1] == '\n' and i < len(text)-1 and text[i+1] == ' ':
                result += '\\*'
            # Para otros caracteres especiales
            elif char in special_chars:
                result += '\\' + char
            # Caracteres normales
            else:
                result += char

        return result
