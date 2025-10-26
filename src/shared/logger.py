"""
Path: src/shared/logger.py
"""

import logging
from src.shared.config import get_config

class FlaskStyleFormatter(logging.Formatter):
    "Formatter que imita el estilo de logging de Flask con colores."
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        fmt = f"{color}[%(levelname)s] %(name)s: %(message)s{self.RESET}"
        formatter = logging.Formatter(fmt)
        return formatter.format(record)

def get_logger(name="twilio-bot"):
    "Configura y devuelve un logger con formato estilo Flask."
    config = get_config()
    log_level = config.get("LOG_LEVEL", "DEBUG").upper()
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(FlaskStyleFormatter())
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, log_level, logging.DEBUG))
        logger.propagate = False  # <--- Evita duplicación de logs
    return logger
