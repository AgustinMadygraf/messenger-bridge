"""
Path: src/infrastructure/google_generativeai/gemini_service.py
python -m src.infrastructure.google_generativeai.gemini_service
"""

import os
import google.generativeai as genai
import dotenv

from src.shared.logger import get_logger
from src.shared.config import get_config

dotenv.load_dotenv()
logger = get_logger("gemini-service")

class GeminiService:
    "Servicio para interactuar con el modelo Gemini de Google."
    def __init__(self, api_key=None):
        try:
            config = get_config()
            self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY") or config.get("GOOGLE_GEMINI_API_KEY")
            if not self.api_key:
                logger.error("Falta GOOGLE_GEMINI_API_KEY en variables de entorno.")
                raise ValueError("Falta GOOGLE_GEMINI_API_KEY en variables de entorno.")
            genai.configure(api_key=self.api_key)
            logger.info("GeminiService inicializado correctamente.")
        except Exception as e:
            logger.error("Error al inicializar GeminiService: %s", e)
            raise

    def get_response(self, prompt):
        "Genera una respuesta usando el modelo Gemini."
        try:
            config = get_config()
            model_name = config.get("GOOGLE_GEMINI_MODEL", "models/gemini-2.5-flash")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            logger.info("Respuesta generada correctamente.")
            return response.text if hasattr(response, "text") else str(response)
        except ValueError as e:
            logger.error("Error al generar respuesta: %s", e)
            return f"Error al generar respuesta con Gemini: {e}"

# Ejemplo de uso CLI
if __name__ == "__main__":
    from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
    try:
        use_case = GenerateGeminiResponseUseCase()
        user_input = input("Usuario: ")
        print("Bot:", use_case.execute(user_input))
    except ValueError as e:
        logger.critical("Error fatal en CLI: %s", e)
    except (KeyError, AttributeError, RuntimeError) as e:
        logger.critical("Ocurrió un error inesperado: %s", e)
