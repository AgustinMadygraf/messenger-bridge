"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram con soporte para Markdown V2."
    def present(self, message: Message) -> list:
        """
        Presenta la respuesta escapando correctamente para MarkdownV2.
        Si el texto es muy largo, lo divide en partes de hasta 4096 caracteres.
        Retorna una lista de diccionarios compatibles con la API de Telegram.
        """
        telegram_format = self._convert_to_telegram_markdown_v2(message.body)
        MAX_LEN = 4096
        parts = [telegram_format[i:i+MAX_LEN] for i in range(0, len(telegram_format), MAX_LEN)]
        total = len(parts)
        result = []
        for idx, part in enumerate(parts, start=1):
            prefix = f"\\-\\-mensaje {idx} de {total}\\-\\-\n"  # Escapa los guiones
            result.append({
                "text": prefix + part,
                "parse_mode": "MarkdownV2"
            })
        return result


    def _convert_to_telegram_markdown_v2(self, text: str) -> str:
        """
        Convierte el formato markdown estándar (**bold**, *italic*) a Telegram MarkdownV2 y escapa caracteres especiales.
        """
        import re

        # 1. Convertir **bold** a *bold* y *italic* a _italic_
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        text = re.sub(r'\*(?!\*)([^*]+?)\*(?!\*)', r'_\1_', text)

        # 2. Escapar todos los caracteres especiales de MarkdownV2 excepto * y _
        # (ya que los usamos para formato)
        special_chars = r'[\[\]\(\)~`>#+\-=|{}\.!]'
        def escape(match):
            return '\\' + match.group(0)
        text = re.sub(special_chars, escape, text)

        return text

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
