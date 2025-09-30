@echo off
call .\venv\Scripts\activate.bat
cd src/infrastructure/rasa
rasa run --enable-api