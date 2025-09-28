"""
Path: src/infrastructure/google_generativeai/gemini_service.py
"""

import json
import google.generativeai as genai

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.entities.gemini_responder import GeminiResponder

logger = get_logger("gemini-service")

class GeminiService(GeminiResponder):
    "Servicio para interactuar con el modelo Gemini de Google."
    def __init__(self, api_key=None, instructions_json_path=None):
        try:
            config = get_config()
            self.api_key = api_key or config.get("GOOGLE_GEMINI_API_KEY")
            logger.debug("API Key utilizada: %s", self.api_key)
            if not self.api_key:
                logger.error("Falta GOOGLE_GEMINI_API_KEY en variables de entorno.")
                raise ValueError("Falta GOOGLE_GEMINI_API_KEY en variables de entorno.")
            genai.configure(api_key=self.api_key)
            logger.info("GeminiService inicializado correctamente.")
            self.system_instructions = None
            if instructions_json_path:
                logger.debug("Cargando instrucciones de sistema desde: %s", instructions_json_path)
                self.system_instructions = self.load_system_instructions_from_json(instructions_json_path)
                if not self.system_instructions:
                    logger.error("No se pudieron cargar las instrucciones de sistema. El bot funcionará sin ellas.")
                else:
                    logger.debug("Instrucciones de sistema cargadas: %s", self.system_instructions)
            else:
                logger.debug("No se proporcionó ruta para instrucciones de sistema.")
        except Exception as e:
            logger.error("Error al inicializar GeminiService: %s", e)
            raise

    @staticmethod
    def load_system_instructions_from_json(json_path, key="instructions"):
        """
        Carga instrucciones de sistema desde un archivo JSON.
        :param json_path: Ruta al archivo JSON.
        :param key: Clave donde están las instrucciones.
        :return: str | None
        """
        try:
            logger.debug("Leyendo archivo JSON de instrucciones: %s", json_path)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.debug("Contenido JSON leído: %s", data)
            return data.get(key)
        except FileNotFoundError as e:
            logger.error("Archivo JSON no encontrado: %s", e)
            return None
        except json.JSONDecodeError as e:
            logger.error("Error al decodificar JSON: %s", e)
            return None
        except OSError as e:
            logger.error("Error de sistema al acceder al archivo JSON: %s", e)
            return None

    def get_response(self, prompt, system_instructions=None):
        "Genera una respuesta usando el modelo Gemini, opcionalmente con instrucciones de sistema."
        try:
            config = get_config()
            model_name = config.get("GOOGLE_GEMINI_MODEL", "models/gemini-2.5-flash")
            logger.debug("Usando modelo Gemini: %s", model_name)
            model = genai.GenerativeModel(model_name)
            instructions = system_instructions or self.system_instructions
            logger.debug("Instrucciones de sistema utilizadas: %s", instructions)
            logger.debug("Prompt recibido: %s", prompt)
            if instructions:
                prompt_final = f"{instructions}\n\n{prompt}"
                logger.debug("Prompt final enviado al modelo: %s", prompt_final)
                response = model.generate_content(prompt_final)
            else:
                logger.debug("No se proporcionaron instrucciones de sistema.")
                response = model.generate_content(prompt)
            logger.info("Respuesta generada correctamente.")
            logger.debug("Respuesta cruda del modelo: %s", response)
            return response.text if hasattr(response, "text") else str(response)
        except ValueError as e:
            logger.error("Error al generar respuesta: %s", e)
            return f"Error al generar respuesta con Gemini: {e}"
