"""
Path: cli_gemini.py
"""

from src.shared.logger import get_logger
from src.infrastructure.google_generativeai.gemini_service import GeminiService
from src.interface_adapter.gateways.gemini_gateway import GeminiGateway
from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
from src.interface_adapter.controller.gemini_controller import GeminiController
from src.interface_adapter.presenters.gemini_presenter import GeminiPresenter

logger = get_logger("gemini-service")


try:
    # Crear el servicio de infraestructura
    gemini_service = GeminiService()

    # Crear el gateway y pasarlo al caso de uso
    gemini_gateway = GeminiGateway(gemini_service)
    use_case = GenerateGeminiResponseUseCase(gemini_gateway)

    # Crear el controlador
    controller = GeminiController(use_case)
    presenter = GeminiPresenter()

    user_input = input("Usuario: ")
    response = controller.handle_prompt(user_input)
    print(presenter.present(response))
except ValueError as e:
    logger.critical("Error fatal en CLI: %s", e)
except (KeyError, AttributeError, RuntimeError) as e:
    logger.critical("Ocurrió un error inesperado: %s", e)
