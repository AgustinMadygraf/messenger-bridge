"""
Path: cli_gemini.py
"""

from src.shared.logger import get_logger
from src.infrastructure.google_generativeai.gemini_service import GeminiService
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase

logger = get_logger("gemini-service")


try:
    # Create the infrastructure component
    gemini_service = GeminiService()
    
    # Inject it into the use case
    use_case = GenerateGeminiResponseUseCase(gemini_service)
    
    user_input = input("Usuario: ")
    print("Bot:", use_case.execute(user_input))
except ValueError as e:
    logger.critical("Error fatal en CLI: %s", e)
except (KeyError, AttributeError, RuntimeError) as e:
    logger.critical("Ocurrió un error inesperado: %s", e)
