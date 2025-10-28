"""
Path: src/infrastructure/audio/vosk/vosk_transcriber.py
"""

import os
import wave
import json
import shutil
import zipfile
import urllib.request
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

from src.shared.logger import get_logger

logger = get_logger("vosk-transcriber")

VOSK_ES_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
VOSK_ES_MODEL_ZIP = "vosk-model-small-es-0.42.zip"
VOSK_ES_MODEL_DIR = "vosk-model-small-es-0.42"

class VoskTranscriber:
    "Transcriptor de audio usando Vosk (offline)."
    def __init__(self, model_path: str = "model"):
        self.vosk_enabled = False
        self.vosk_model = None
        # Si no existe el modelo, descargar y descomprimir
        if not os.path.isdir(model_path):
            logger.warning("El modelo Vosk no se encontró en %s. Descargando...", model_path)
            self._download_and_extract_model(model_path)

        try:
            if Model is not None and KaldiRecognizer is not None and os.path.isdir(model_path):
                logger.info("Intentando cargar modelo Vosk en %s.", model_path)
                self.vosk_model = Model(model_path)
                self.vosk_enabled = True
                logger.info("Modelo Vosk cargado correctamente.")
            else:
                logger.warning("Vosk no está disponible o el modelo no se encontró.")
        except (OSError, RuntimeError) as e:
            logger.error("Error al cargar el modelo Vosk: %s", e)
            self.vosk_enabled = False
            self.vosk_model = None

    def _download_and_extract_model(self, model_path):
        try:
            # Descargar el modelo zip si no existe
            if not os.path.exists(VOSK_ES_MODEL_ZIP):
                logger.info("Descargando modelo Vosk español desde %s...", VOSK_ES_MODEL_URL)
                urllib.request.urlretrieve(VOSK_ES_MODEL_URL, VOSK_ES_MODEL_ZIP)
                logger.info("Descarga completada: %s", VOSK_ES_MODEL_ZIP)
            else:
                logger.info("El archivo zip del modelo ya existe: %s", VOSK_ES_MODEL_ZIP)

            # Extraer el zip
            logger.info("Descomprimiendo modelo...")
            with zipfile.ZipFile(VOSK_ES_MODEL_ZIP, 'r') as zip_ref:
                zip_ref.extractall(".")
            logger.info("Modelo descomprimido.")

            # Mover/cambiar nombre de la carpeta al destino esperado
            if os.path.exists(VOSK_ES_MODEL_DIR):
                shutil.move(VOSK_ES_MODEL_DIR, model_path)
                logger.info("Modelo movido a: %s", model_path)

            # Eliminar el archivo zip después de descomprimir
            if os.path.exists(VOSK_ES_MODEL_ZIP):
                os.remove(VOSK_ES_MODEL_ZIP)
                logger.info("Archivo zip eliminado: %s", VOSK_ES_MODEL_ZIP)
        except (OSError, zipfile.BadZipFile, urllib.error.URLError) as e:
            logger.error("Error descargando o descomprimiendo el modelo Vosk: %s", e)

    def transcribe(self, wav_path: str) -> str:
        "Transcribe un archivo WAV usando Vosk."
        if not self.vosk_enabled or self.vosk_model is None:
            logger.warning("Vosk no está habilitado.")
            return None
        try:
            wf = wave.open(wav_path, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                audio = AudioSegment.from_wav(wav_path).set_channels(1).set_sample_width(2)
                audio.export(wav_path, format="wav")
                wf = wave.open(wav_path, "rb")
            rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    part_result = rec.Result()
                    try:
                        part_json = json.loads(part_result)
                        results.append(part_json.get("text", ""))
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.warning("Error decodificando resultado parcial de Vosk: %s", e)
            # Procesar resultado final
            final_result = rec.FinalResult()
            try:
                final_json = json.loads(final_result)
                results.append(final_json.get("text", ""))
            except (json.JSONDecodeError, TypeError) as e:
                logger.error("Error decodificando resultado final de Vosk: %s", e)
            text = " ".join([r for r in results if r]).strip()
            if not text:
                logger.warning("Vosk no pudo transcribir el audio.")
                return "Vosk no pudo transcribir el audio."
            logger.info("Transcripción exitosa con Vosk.")
            return text
        except (OSError, RuntimeError, wave.Error, json.JSONDecodeError) as e:
            logger.error("Error usando Vosk: %s", e)
            return f"Error usando Vosk: {e}"
