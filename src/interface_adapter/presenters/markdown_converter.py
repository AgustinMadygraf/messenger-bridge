"""
Path: src/interface_adapter/presenters/markdown_converter.py
"""

import re

class MarkdownConverter:
    "Convierte formato Markdown estándar a MarkdownV2 para Telegram."
    def convert(self, text: str) -> str:
        "Convierte negritas y cursivas a formato MarkdownV2 y escapa caracteres especiales."
        text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
        text = re.sub(r'\*(?!\*)([^*]+?)\*(?!\*)', r'_\1_', text)
        return self._escape_markdown_v2(text)

    def _escape_markdown_v2(self, text: str) -> str:
        "Escapa caracteres especiales según las reglas de MarkdownV2."
        special_chars = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '\\']
        return ''.join(['\\' + c if c in special_chars else c for c in text])
