"""
Path: src/shared/config.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    "Load configuration from environment variables"

    config = {
        "ACCOUNT_SID": os.getenv('TWILIO_ACCOUNT_SID'),
        "AUTH_TOKEN": os.getenv('TWILIO_AUTH_TOKEN'),
        "WHATSAPP_FROM": os.getenv('TWILIO_WHATSAPP_FROM'),
        "CONTENT_SID": os.getenv('TWILIO_CONTENT_SID'),
        "CONTENT_VARIABLES": os.getenv('TWILIO_CONTENT_VARIABLES'),
        "WHATSAPP_TO": os.getenv('TWILIO_WHATSAPP_TO'),
        "GOOGLE_GEMINI_MODEL": os.getenv('GOOGLE_GEMINI_MODEL'),
        "GOOGLE_GEMINI_API_KEY": os.getenv('GOOGLE_GEMINI_API_KEY'),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        "LOG_LEVEL": os.getenv('LOG_LEVEL', 'DEBUG'),
        "TELEGRAM_API_KEY": os.getenv('TELEGRAM_API_KEY'),
        "RASA_API_URL": os.getenv('RASA_API_URL', 'http://localhost:5005/webhooks/rest/webhook'),
        "NGROK_DOMAIN": os.getenv('NGROK_DOMAIN'),
    }

    if not config["ACCOUNT_SID"] or not config["AUTH_TOKEN"]:
        raise ValueError("Twilio credentials not set in environment variables.")

    return config
