# Messenger Bridge

## Descripción
Messenger Bridge es un sistema de integración que conecta diferentes plataformas de mensajería (WhatsApp vía Twilio y Telegram) con un motor conversacional configurable (por ejemplo, Rasa, GPT4All, OpenAI, Gemini, etc.), permitiendo mantener conversaciones inteligentes a través de distintos canales de comunicación.

## Relación con el repositorio motor-conversacional

Este repositorio está diseñado para funcionar en conjunto con el repositorio [`AgustinMadygraf/motor-conversacional`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt), que implementa el motor conversacional configurable. Messenger Bridge actúa como puente entre las plataformas de mensajería y el motor conversacional, enviando los mensajes recibidos desde WhatsApp o Telegram al motor y devolviendo la respuesta generada al usuario final.

Puedes utilizar cualquier motor compatible que implemente la API esperada (por ejemplo, Rasa, GPT4All, OpenAI, Gemini, etc.), pero se recomienda utilizar el repositorio mencionado para una integración directa y soporte completo.

Para más detalles sobre la configuración y despliegue del motor conversacional, consulta la documentación del repositorio [`motor-conversacional`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt).

## Características
- 🤖 Integración con chatbots basados en Rasa, GPT4All, OpenAI, Gemini, etc.
- 📱 Soporte para WhatsApp (vía Twilio)
- ✈️ Soporte para Telegram
- 🔊 Transcripción de mensajes de audio (OGG a texto)
- 🌐 Exposición de webhooks mediante ngrok
- 🖥️ Interfaz CLI para pruebas locales

## Requisitos
- Python 3.10+
- Cuenta en Twilio con configuración de WhatsApp Business API
- Bot de Telegram (token generado a través de BotFather)
- Motor conversacional funcional (por ejemplo, [`motor-conversacional`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt))
- Cuenta en ngrok (recomendado el plan con dominio personalizado fijo)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/AgustinMadygraf/messenger-bridge
cd messenger-bridge
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# Copiar el archivo de ejemplo
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración

Edita el archivo `.env` con tus credenciales:

```
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TELEGRAM_API_KEY=tu_telegram_api_key_aqui
LOG_LEVEL=INFO
RASA_API_URL=http://localhost:5005/webhooks/rest/webhook
NGROK_DOMAIN=tu_dominio_fijo.ngrok-free.app
```

Asegúrate de que la URL del motor conversacional (`RASA_API_URL` o equivalente) apunte al endpoint correcto del servicio desplegado desde el repositorio [`motor-conversacional`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt).

## Uso

### Iniciar el servicio completo:
```bash
python run.py
```

### Usar el transcriptor de audio:
```bash
python run_transcriber.py
```

## Estructura del Proyecto

El proyecto sigue principios de arquitectura limpia (Clean Architecture):

- **entities/**: Objetos de dominio (Message)
- **use_cases/**: Lógica de negocio independiente de infraestructura
- **interface_adapter/**: 
  - **controller/**: Puntos de entrada para diferentes plataformas
  - **presenters/**: Formateo de respuestas 
  - **gateways/**: Interfaces para servicios externos
- **infrastructure/**: Implementaciones concretas para cada plataforma
  - **cli/**: Implementación de consola de comandos
  - **fastapi/**: Implementación de webhooks con FastAPI
  - **pyngrok/**: Configuración de túneles ngrok
  - **telegram_bot/**: Implementación del bot de Telegram
  - **twilio/**: Implementación de WhatsApp con Twilio
- **shared/**: Utilidades compartidas (configuración, logging)