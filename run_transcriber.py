"""
Path: run_transcriber.py
"""

import os
from src.transcriber import transcribe_ogg

def main():
    "Main function to run the OGG transcription process."
    # Prompt the user for the path of the OGG file
    ogg_file_path = input("Please enter the path of the OGG file: ")

    # Check if the file exists
    if not os.path.isfile(ogg_file_path):
        print("The specified file does not exist. Please check the path and try again.")
        return

    # Transcribe the OGG file
    transcription = transcribe_ogg(ogg_file_path)

    # Display the transcription result
    print("Transcription Result:")
    print(transcription)

if __name__ == "__main__":
    main()
