"""
Path: src/infrastructure/cli/cli_service.py
"""

from src.shared.logger import get_logger

logger = get_logger("twilio-bot.cli")

def run_cli_mode():
    "Configura y ejecuta el modo CLI usando Rasa."
    from src.interface_adapter.gateways.agent_gateway import AgentService
    from src.interface_adapter.presenters.telegram_presenter import TelegramMessagePresenter
    from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
    from src.entities.conversation_manager import ConversationManager
    from src.entities.message import Message

    # Puedes cambiar la URL si tu Rasa corre en otro puerto/host
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    rasa_service = AgentService(rasa_url)
    conversation_manager = ConversationManager()
    use_case = GenerateAgentResponseUseCase(rasa_service, conversation_manager)
    presenter = TelegramMessagePresenter()

    logger.info("[CLI] Modo respuesta Rasa. Escribe un mensaje para simular recepción (escribe 'salir' para terminar):")
    try:
        while True:
            user_input = input("Usuario: ")
            if user_input.strip().lower() in ("salir", "exit", "quit"):
                logger.info("Saliendo del modo CLI respuesta.")
                break

            # Usamos 'cli' como conversation_id
            user_message = Message(to="cli", body=user_input)
            response_message = use_case.execute("cli", user_message)
            formatted_response = presenter.present(response_message)
            print(formatted_response)

    except KeyboardInterrupt:
        logger.info("Interrupción detectada. Saliendo del modo CLI respuesta.")
