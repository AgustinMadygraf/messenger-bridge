"""
Path: src/interface_adapter/controller/gemini_controller.py
"""

class GeminiController:
    "Controlador para orquestar la interacción entre la entrada del usuario y el caso de uso."
    def __init__(self, use_case):
        self.use_case = use_case

    def handle_prompt(self, prompt):
        "Recibe el prompt del usuario, lo valida y retorna la respuesta del caso de uso."
        try:
            return self.use_case.execute(prompt)
        except ValueError as e:
            return f"Error: {e}"
