"""
Path: src/infrastructure/twilio/twilio_service.py
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.interface_adapter.gateways.agent_gateway import AgentGateway
from src.use_cases.generate_agent_response_use_case import GenerateAgentResponseUseCase
from src.entities.conversation_manager import ConversationManager

class TwilioMessageSender:
    " Implementación de MessageSender usando Twilio y Rasa. "
    def __init__(self, from_number, rasa_url="http://localhost:5005/webhooks/rest/webhook"):
        self.from_number = from_number
        self.logger = get_logger("twilio-bot.twilio_service")
        self.rasa_service = AgentGateway(rasa_url)
        self.conversation_manager = ConversationManager()
        self.rasa_use_case = GenerateAgentResponseUseCase(self.rasa_service, self.conversation_manager)

    def send_message(self, message, _content_sid=None, _content_variables=None):
        "Genera respuesta con Rasa y la envía por WhatsApp usando Twilio."
        config = get_config()
        client = Client(config["ACCOUNT_SID"], config["AUTH_TOKEN"])

        # Genera la respuesta con Rasa
        response_message = self.rasa_use_case.execute(message.to, message)
        text_to_send = response_message.body

        try:
            twilio_message = client.messages.create(
                from_=self.from_number,
                body=text_to_send,
                to=message.to
            )
            self.logger.info("Mensaje enviado correctamente. SID: %s", twilio_message.sid)
            return twilio_message.sid
        except TwilioRestException as e:
            self.logger.error("Error al enviar mensaje por Twilio: %s", e)
            return None
