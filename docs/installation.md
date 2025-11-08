# Guía de instalación - Messenger Bridge

Esta guía contiene las instrucciones detalladas para instalar, configurar y ejecutar el sistema Messenger Bridge.

## Requisitos previos

- Python 3.10 o superior
- Cuenta en Twilio con configuración de WhatsApp Business API
- Bot de Telegram (token generado a través de BotFather)
- Motor conversacional funcional (por ejemplo, [`rasa-gemini-bot`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt))
- Cuenta en ngrok (recomendado el plan con dominio personalizado fijo)

## Proceso de instalación

### 1. Clonar el repositorio:

```bash
git clone https://github.com/AgustinMadygraf/messenger-bridge
cd messenger-bridge
```

### 2. Crear y activar entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# En Windows:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias:

```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno:

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración detallada

Edita el archivo `.env` con tus credenciales:

```
# NGROK configuration
API_DOMAIN=your_domain_here.ngrok-free.app

# Telegram Bot configuration
TELEGRAM_API_KEY=your_telegram_api_key_here

# Twilio configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here

# Rasa configuration
LOG_LEVEL=INFO

# Rasa server URL
RASA_API_URL=http://localhost:5005/webhooks/rest/webhook
```

### Configuración de ngrok

Para utilizar un dominio personalizado de ngrok:
1. Registra una cuenta en [ngrok](https://ngrok.com/)
2. Configura un dominio fijo en el panel de control
3. Asegúrate de que la variable `API_DOMAIN` en `.env` contenga tu dominio personalizado

### Configuración de Telegram

1. Crea un bot en Telegram mediante [@BotFather](https://t.me/botfather)
2. Obtén el token de API y colócalo en la variable `TELEGRAM_API_KEY`
3. Una vez que el sistema esté funcionando, ejecuta `python set_telegram_webhook.py` para configurar el webhook

### Configuración de Twilio/WhatsApp

1. Crea una cuenta en [Twilio](https://www.twilio.com/)
2. Configura el Sandbox de WhatsApp Business
3. Obtén las credenciales y colócalas en las variables `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN`
4. Configura el webhook URL en el panel de Twilio para que apunte a tu dominio ngrok + `/twilio/webhook`

## Uso del sistema

### Iniciar el servicio completo:

```bash
python run.py
```

Esto iniciará:
1. Un túnel ngrok en el puerto 8443
2. El servidor FastAPI para manejar webhooks



## Solución de problemas comunes

### Error al iniciar ngrok

Si ves errores relacionados con ngrok:

- Verifica que tu cuenta de ngrok esté correctamente autenticada
- Asegúrate de que no haya otro túnel ngrok ejecutándose
- Verifica que el dominio personalizado esté configurado correctamente

### Error en la comunicación con el motor conversacional

Si el sistema no logra comunicarse con el motor:

- Verifica que la URL en `RASA_API_URL` sea correcta
- Comprueba que el servicio del motor esté funcionando
- Revisa los logs para identificar errores específicos

## Integración con el motor conversacional

Para integrar con el repositorio [`rasa-gemini-bot`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt):

1. Configura y ejecuta el motor conversacional según sus instrucciones
2. Asegúrate de que la URL configurada en `RASA_API_URL` apunte al endpoint correcto
3. Verifica que el formato de mensajes sea compatible entre ambos sistemas



### instalación de ffmpeg con Winget para Windows 11

```
# Buscar el paquete para confirmar ID
winget search ffmpeg

# Instalar (ID exacto)
winget install -e --id Gyan.FFmpeg

# Verificar
ffmpeg -version
where ffmpeg
```