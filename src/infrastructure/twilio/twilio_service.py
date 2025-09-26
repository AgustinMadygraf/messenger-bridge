"""
Path: src/shared/infrastructure/twilio/twilio_service.py
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import json

from src.shared.config import get_config

from src.use_cases.send_whatsapp_message_use_case import MessageSender

class TwilioMessageSender(MessageSender):
    " Implementación de MessageSender usando Twilio. "
    def __init__(self, from_number):
        self.from_number = from_number

    def send_whatsapp_message(self, message, content_sid, content_variables):
        "Envía un mensaje WhatsApp usando Twilio."
        config = get_config()
        client = Client(config["ACCOUNT_SID"], config["AUTH_TOKEN"])
        if isinstance(content_variables, dict):
            content_variables = json.dumps(content_variables)
        print(f"[DEBUG] content_variables enviados a Twilio: {content_variables}")
        try:
            twilio_message = client.messages.create(
                from_=self.from_number,
                content_sid=content_sid,
                content_variables=content_variables,
                to=message.to
            )
            return twilio_message.sid
        except TwilioRestException as e:
            print(f"Error al enviar mensaje por Twilio: {e}")
            return None
