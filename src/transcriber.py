"""
Path: src/transcriber.py
"""

import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def transcribe_ogg(file_path):
    "Transcribe an OGG audio file to text."
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Convert OGG to WAV using pydub
    wav_path = file_path + ".wav"
    try:
        audio = AudioSegment.from_ogg(file_path)
        audio.export(wav_path, format="wav")
    except FileNotFoundError as e:
        return f"Converter not found: {e}"
    except CouldntDecodeError as e:
        return f"Converter not found or could not decode audio: {e}"
    except OSError as e:
        return f"OS error during OGG to WAV conversion: {e}"
    except ValueError as e:
        return f"Value error during OGG to WAV conversion: {e}"
    except TypeError as e:
        return f"Type error during OGG to WAV conversion: {e}"

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the WAV file
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    # Transcribe audio to text
    try:
        text = recognizer.recognize_google(audio_data, language="es-ES")
        return text
    except sr.UnknownValueError:
        return "Audio unintelligible"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        # Clean up the temporary WAV file
        if os.path.exists(wav_path):
            os.remove(wav_path)
