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
        "LOG_LEVEL": os.getenv('LOG_LEVEL', 'DEBUG'),
        "TELEGRAM_API_KEY": os.getenv('TELEGRAM_API_KEY'),
        "TELEGRAM_MODE": os.getenv('TELEGRAM_MODE', 'polling'),
        "RASA_API_URL": os.getenv('RASA_API_URL', 'http://localhost:5005/webhooks/rest/webhook'),
        "NGROK_DOMAIN": os.getenv('NGROK_DOMAIN'),
    }

    if not config["ACCOUNT_SID"] or not config["AUTH_TOKEN"]:
        raise ValueError("Twilio credentials not set in environment variables.")

    return config
