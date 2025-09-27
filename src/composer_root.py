"""
Path: src/composer_root.py
"""

from src.shared.config import get_config
from src.infrastructure.twilio.twilio_service import TwilioMessageSender
from src.interface_adapter.gateways.cli_gateway import CliGateway
from src.infrastructure.cli.cli_service import CliMessageSender
from src.interface_adapter.gateways.twilio_gateway import TwilioGateway
from src.interface_adapter.controller.whatsapp_message_controller import WhatsappMessageController
from src.interface_adapter.presenters.cli_presenter import CliPresenter

def compose_twilio_plantilla():
    "Configura y devuelve el controlador y presentador para el modo Twilio plantilla"
    config = get_config()
    sender = TwilioMessageSender(config["WHATSAPP_FROM"])
    gateway = TwilioGateway(sender, config["WHATSAPP_FROM"])
    controller = WhatsappMessageController(gateway)
    presenter = CliPresenter()
    return controller, presenter, config

def compose_cli_plantilla():
    "Configura y devuelve el controlador y presentador para el modo CLI plantilla"
    config = get_config()
    sender = CliMessageSender()
    gateway = CliGateway(sender)
    controller = WhatsappMessageController(gateway)
    presenter = CliPresenter()
    return controller, presenter, config

def compose_cli_respuesta():
    "Configura y devuelve el controlador y presentador para el modo CLI respuesta usando Gemini"
    from src.infrastructure.google_generativeai.gemini_service import GeminiService
    from src.interface_adapter.gateways.gemini_gateway import GeminiGateway
    from src.use_cases.generate_gemini_response_use_case import GenerateGeminiResponseUseCase
    from src.interface_adapter.controller.gemini_controller import GeminiController
    from src.interface_adapter.presenters.gemini_presenter import GeminiPresenter

    gemini_service = GeminiService()
    gemini_gateway = GeminiGateway(gemini_service)
    use_case = GenerateGeminiResponseUseCase(gemini_gateway)
    controller = GeminiController(use_case)
    presenter = GeminiPresenter()
    return controller, presenter

def compose_twilio_respuesta():
    "Configura y devuelve la aplicación Flask para manejar webhooks de Twilio "
    from src.infrastructure.flask.flask_webhook import run_flask_webhook
    return run_flask_webhook
