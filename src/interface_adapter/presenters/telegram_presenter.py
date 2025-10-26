"""
Path: src/interface_adapter/presenters/telegram_presenter.py
"""

import re

from src.entities.message import Message

class TelegramMessagePresenter:
    "Presenter para formatear mensajes de Telegram con soporte para Markdown V2."
    def _split_markdown_safe(self, text: str, max_len: int) -> list:
        "Divide el texto en partes de hasta max_len caracteres, evitando cortar dentro de una entidad MarkdownV2 (* o _)."
        parts = []
        start = 0
        while start < len(text):
            end = min(start + max_len, len(text))
            # Si el corte cae dentro de una entidad, retroceder hasta el último delimitador antes del límite
            part_text = text[start:end]
            # Buscar el último delimitador antes del final
            last_asterisk = part_text.rfind('*')
            last_underscore = part_text.rfind('_')
            last_delim = max(last_asterisk, last_underscore)
            # Si el último delimitador está cerca del final y hay un número impar de delimitadores en el part_text, cortar allí
            if last_delim > 0 and end < len(text):
                # Contar delimitadores en el part_text
                asterisks = part_text.count('*')
                underscores = part_text.count('_')
                if (asterisks % 2 != 0) or (underscores % 2 != 0):
                    # Cortar en el último delimitador antes del final
                    end = start + last_delim
                    part_text = text[start:end]
            parts.append(part_text)
            start = end
        return parts

    def present(self, message: Message) -> list:
        "Presenta la respuesta escapando correctamente para MarkdownV2."
        print(f"[DEBUG] Texto original: {message.body}")
        telegram_format = self._convert_to_telegram_markdown_v2(message.body)
        print(f"[DEBUG] Texto convertido: {telegram_format}")
        max_len = 4096
        parts = self._split_markdown_safe(telegram_format, max_len)
        total = len(parts)
        result = []
        for idx, part in enumerate(parts, start=1):
            self._validate_markdown_balance(part)
            if total > 1:
                prefix = f"\\-\\-mensaje {idx} de {total}\\-\\-\n"
                text = prefix + part
            else:
                text = part
            result.append({
                "text": text,
                "parse_mode": "MarkdownV2"
            })
        return result
    def _validate_markdown_balance(self, text: str):
        "Valida que los delimitadores de formato MarkdownV2 (* y _) estén balanceados en el texto."
        asterisks = text.count('*')
        underscores = text.count('_')
        if asterisks % 2 != 0:
            print(f"[DEBUG] MarkdownV2 desbalanceado: número impar de asteriscos (*) en el texto: {asterisks}\nTexto: {text}")
            raise ValueError(f"MarkdownV2 desbalanceado: número impar de asteriscos (*) en el texto: {asterisks}")
        if underscores % 2 != 0:
            print(f"[DEBUG] MarkdownV2 desbalanceado: número impar de guiones bajos (_) en el texto: {underscores}\nTexto: {text}")
            raise ValueError(f"MarkdownV2 desbalanceado: número impar de guiones bajos (_) en el texto: {underscores}")


    def _convert_to_telegram_markdown_v2(self, text: str) -> str:
        "Convierte el formato markdown estándar (**bold**, *italic*) a Telegram MarkdownV2 y escapa caracteres especiales."
        # 1. Convertir **bold** a *bold* y *italic* a _italic_
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        text = re.sub(r'\*(?!\*)([^*]+?)\*(?!\*)', r'_\1_', text)
        # 2. Escapar caracteres especiales de MarkdownV2, preservando * y _ para formato
        text = self._escape_markdown_v2(text)
        return text

    def _escape_markdown_v2(self, text: str) -> str:
        "Escapa los caracteres especiales de MarkdownV2 preservando los delimitadores de formato (* y _)."
        special_chars = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '\\']
        result = ''
        for char in text:
            # No escapar * ni _ porque se usan para formato
            if char in special_chars:
                result += '\\' + char
            else:
                result += char
        return result
