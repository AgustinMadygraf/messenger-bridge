"""
Path: src/interface_adapter/presenters/cli_presenter.py
"""

class CliPresenter:
    "Presentador para CLI."
    def present(self, result):
        "Convierte el resultado en un mensaje para mostrar en CLI."
        if isinstance(result, str):
            return f"[CLI] Resultado: {result}"
        else:
            return f"[CLI] Respuesta: {repr(result)}"
