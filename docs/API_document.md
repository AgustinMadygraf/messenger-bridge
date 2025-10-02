# Documentación de API - Messenger Bridge

## Introducción

Esta documentación describe los endpoints de API disponibles en el sistema Messenger Bridge, que permite la comunicación entre plataformas de mensajería (WhatsApp vía Twilio y Telegram) y un motor conversacional configurable (por ejemplo, Rasa, GPT4All, OpenAI, Gemini, etc.).

## Autenticación

La API utiliza diferentes mecanismos de autenticación según el endpoint:

- **Twilio**: Las solicitudes a los webhooks de Twilio son autenticadas mediante la validación de la firma de solicitud de Twilio.
- **Telegram**: Las solicitudes a los webhooks de Telegram son validadas a través del token de bot configurado en las variables de entorno.

## Endpoints

### Webhook de Twilio

```
POST /twilio/webhook
```

Recibe mensajes entrantes de WhatsApp a través de la plataforma Twilio.

#### Solicitud
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parámetros**:
  - `Body`: Texto del mensaje
  - `From`: Número de teléfono del remitente (formato WhatsApp: `whatsapp:+XXXXXXXXXXXX`)
  - `NumMedia`: Número de archivos multimedia adjuntos
  - `MediaUrl0`: URL del primer archivo multimedia (si existe)
  - `MediaContentType0`: Tipo MIME del primer archivo multimedia

#### Respuesta
- **Content-Type**: `application/xml`
- **Cuerpo**: TwiML XML con la respuesta generada por el motor conversacional

```xml
<Response>
  <Message>Respuesta generada por el motor conversacional</Message>
</Response>
```

### Webhook de Telegram

```
POST /telegram/webhook
```

Recibe actualizaciones del bot de Telegram configurado.

#### Solicitud
- **Content-Type**: `application/json`
- **Cuerpo**:
  ```json
  {
    "update_id": 123456789,
    "message": {
      "message_id": 123,
      "from": {
        "id": 12345678,
        "first_name": "Nombre",
        "username": "usuario"
      },
      "chat": {
        "id": 12345678,
        "type": "private"
      },
      "date": 1632154823,
      "text": "Mensaje del usuario"
    }
  }
  ```

#### Respuesta
- **Content-Type**: `text/plain`
- **Cuerpo**: `OK` (la respuesta real se envía asincrónicamente a la API de Telegram)

### Página principal

```
GET /
```

Muestra una página HTML simple con instrucciones y un código QR para conectar WhatsApp.

#### Solicitud
No requiere parámetros.

#### Respuesta
- **Content-Type**: `text/html`
- **Cuerpo**: Página HTML con QR de WhatsApp

## Integración con el motor conversacional

### Formato de solicitud al motor conversacional
El sistema utiliza `AgentGateway` para comunicarse con el motor configurado (Rasa, GPT4All, OpenAI, Gemini, etc.):

```json
{
  "sender": "user",
  "message": "Texto del mensaje del usuario"
}
```

### Formato de respuesta del motor conversacional
La API del motor conversacional debe devolver una lista de mensajes en el siguiente formato:

```json
[
  {
    "recipient_id": "user",
    "text": "Respuesta generada"
  }
]
```

## Procesamiento de audio

El sistema incluye capacidades de transcripción de audio a través de `AudioTranscriberUseCase` con implementación en `LocalAudioTranscriber`.

### Formatos de audio soportados
- OGG
- WAV
- MP3
- Otros formatos compatibles con `pydub`

## Manejo de errores

### Errores comunes
- **500 Internal Server Error**: Error en el procesamiento del mensaje
- **400 Bad Request**: Formato de solicitud inválido
- **401 Unauthorized**: Autenticación fallida

## Ejemplos

### Enviar mensaje a Twilio Webhook

```bash
curl -X POST http://localhost:8443/twilio/webhook \
  -d "Body=Hola" \
  -d "From=whatsapp:+1234567890" \
  -d "NumMedia=0"
```

### Enviar mensaje a Telegram Webhook

```bash
curl -X POST http://localhost:8443/telegram/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456789,
    "message": {
      "message_id": 123,
      "from": {"id": 12345678, "first_name": "Usuario"},
      "chat": {"id": 12345678, "type": "private"},
      "date": 1632154823,
      "text": "Hola"
    }
  }'
```

## Notas adicionales

- La API está diseñada siguiendo los principios de Clean Architecture
- Para configurar webhooks de Telegram, utilice el script set_telegram_webhook.py
- El manejo de archivos multimedia está implementado para archivos de audio