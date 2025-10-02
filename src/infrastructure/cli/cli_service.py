"""
Path: src/infrastructure/cli/cli_service.py
"""

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.interface_adapter.gateways.cli_gateway import CliGateway
from src.interface_adapter.presenters.cli_presenter import CliPresenter
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.interface_adapter.controller.cli_controller import CliMessageController
from src.entities.message import Message

logger = get_logger("twilio-bot.cli")

class CliSender:
    "Implementación concreta para enviar mensajes por CLI."
    def send_message(self, message: Message, _content_sid: str = "", _content_variables: dict = None):
        "Envía el mensaje imprimiéndolo en la consola."
        print(message.body)

def run_cli_mode():
    "Configura y ejecuta el modo CLI usando Rasa."
    config = get_config()
    agent_bot_url = config.get("RASA_API_URL", "http://localhost:5005/webhooks/rest/webhook")
    agent_bot_service = AgentGateway(agent_bot_url)
    use_case = GenerateAgentResponseUseCase(agent_bot_service)
    presenter = CliPresenter()
    controller = CliMessageController(use_case, presenter)
    sender = CliSender()
    gateway = CliGateway(sender)

    logger.info("[CLI] Modo respuesta Rasa. Escribe un mensaje para simular recepción (escribe 'salir' para terminar):")
    try:
        while True:
            user_input = input("Usuario: ")
            if user_input.strip().lower() in ("salir", "exit", "quit"):
                logger.info("Saliendo del modo CLI respuesta.")
                break

            # Usamos 'cli' como conversation_id
            formatted_response = controller.handle("cli", user_input)
            gateway.send_message(Message(to="cli", body=formatted_response))

    except KeyboardInterrupt:
        logger.info("Interrupción detectada. Saliendo del modo CLI respuesta.")
