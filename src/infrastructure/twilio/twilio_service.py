"""
Path: src/shared/infrastructure/twilio/twilio_service.py
"""

import json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from src.shared.config import get_config
from src.shared.logger import get_logger

from src.use_cases.send_whatsapp_message_use_case import MessageSender

class TwilioMessageSender(MessageSender):
    " Implementación de MessageSender usando Twilio. "
    def __init__(self, from_number):
        self.from_number = from_number
        self.logger = get_logger("twilio-bot.twilio_service")

    def send_whatsapp_message(self, message, content_sid, content_variables):
        "Envía un mensaje WhatsApp usando Twilio."
        config = get_config()
        client = Client(config["ACCOUNT_SID"], config["AUTH_TOKEN"])
        if isinstance(content_variables, dict):
            content_variables = json.dumps(content_variables)
        self.logger.debug("content_variables enviados a Twilio: %s", content_variables)
        try:
            twilio_message = client.messages.create(
                from_=self.from_number,
                content_sid=content_sid,
                content_variables=content_variables,
                to=message.to
            )
            self.logger.info("Mensaje enviado correctamente. SID: %s", twilio_message.sid)
            return twilio_message.sid
        except TwilioRestException as e:
            self.logger.error("Error al enviar mensaje por Twilio: %s", e)
            return None
