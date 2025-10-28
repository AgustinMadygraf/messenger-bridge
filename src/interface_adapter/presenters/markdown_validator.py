"""
Path: src/interface_adapter/presenters/markdown_validator.py
"""

class MarkdownValidator:
    "Validador simple para verificar el balanceo de ciertos elementos de MarkdownV2."
    def validate(self, text: str):
        "Valida que los elementos de MarkdownV2 estén balanceados."
        lines = text.splitlines()
        non_list_asterisks = 0
        for line in lines:
            # Si la línea comienza con '* ', ignora ese asterisco (lista)
            if line.startswith('* '):
                line_to_check = line[2:]
            else:
                line_to_check = line
            non_list_asterisks += line_to_check.count('*')
        if non_list_asterisks % 2 != 0:
            raise ValueError("MarkdownV2 desbalanceado: número impar de asteriscos (*) fuera de listas")
        if text.count('_') % 2 != 0:
            raise ValueError("MarkdownV2 desbalanceado: número impar de guiones bajos (_)")
