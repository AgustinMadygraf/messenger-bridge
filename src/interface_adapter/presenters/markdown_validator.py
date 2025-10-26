"""
Path: src/interface_adapter/presenters/markdown_validator.py
"""

class MarkdownValidator:
    "Validador simple para verificar el balanceo de ciertos elementos de MarkdownV2."
    def validate(self, text: str):
        "Valida que los elementos de MarkdownV2 estén balanceados."
        if text.count('*') % 2 != 0:
            raise ValueError("MarkdownV2 desbalanceado: número impar de asteriscos (*)")
        if text.count('_') % 2 != 0:
            raise ValueError("MarkdownV2 desbalanceado: número impar de guiones bajos (_)")
