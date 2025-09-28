"""
Path: src/infrastructure/cli/cli_service.py
"""

from src.shared.logger import get_logger

logger = get_logger("twilio-bot.cli")

def run_cli_mode():
    "Configures and returns components for CLI interaction mode."
    from src.infrastructure.google_generativeai.gemini_service import GeminiService
    from src.interface_adapter.gateways.gemini_gateway import GeminiGateway
    from src.interface_adapter.controller.gemini_controller import GeminiController
    from src.interface_adapter.presenters.gemini_presenter import GeminiPresenter
    from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
    from src.entities.conversation import Conversation
    from src.entities.message import Message

    gemini_service = GeminiService(
        instructions_json_path="src/infrastructure/google_generativeai/system_instructions.json"
    )
    gemini_gateway = GeminiGateway(gemini_service)
    use_case = GenerateGeminiResponseUseCase(gemini_gateway)
    conversation = Conversation()
    controller = GeminiController(use_case, conversation)
    presenter = GeminiPresenter()

    logger.info("[CLI] Modo respuesta. Escribe un mensaje para simular recepción (escribe 'salir' para terminar):")
    try:
        while True:
            user_input = input("Usuario: ")
            if user_input.strip().lower() in ("salir", "exit", "quit"):
                logger.info("Saliendo del modo CLI respuesta.")
                break

            response = controller.handle_user_message(user_input)
            formatted_response = presenter.present(Message(to="Bot", body=response))
            print(formatted_response)

    except KeyboardInterrupt:
        logger.info("Interrupción detectada. Saliendo del modo CLI respuesta.")
