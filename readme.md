# Twilio WhatsApp Bot

## Descripción
Este proyecto implementa un bot para enviar mensajes a través de WhatsApp utilizando la API de Twilio. Está diseñado siguiendo los principios de arquitectura limpia (Clean Architecture) para mantener una separación clara de responsabilidades y facilitar pruebas y mantenimiento.

El sistema permite dos modos de operación:
- **Modo Twilio**: Envía mensajes reales usando la API de Twilio
- **Modo CLI**: Simula el envío de mensajes (útil para desarrollo y pruebas)

## Estructura del proyecto
```
.
├── run.py                           # Punto de entrada principal
└── src/                             # Código fuente
    ├── entities/                    # Entidades de dominio
    │   └── whatsapp_message.py      # Entidad de mensaje WhatsApp
    ├── infrastructure/              # Implementaciones concretas
    │   └── twilio/                  # Servicios relacionados con Twilio
    │       └── twilio_service.py    # Implementación de servicio Twilio
    ├── interface_adapter/           # Adaptadores de interfaz
    │   ├── controller/              # Controladores
    │   ├── gateways/                # Gateways para servicios externos
    │   └── presenters/              # Presentadores de datos
    ├── shared/                      # Componentes compartidos
    │   ├── config.py                # Gestión de configuración
    │   └── logger.py                # Servicios de logging
    └── use_cases/                   # Casos de uso de la aplicación
        └── send_whatsapp_message_use_case.py
```

## Requisitos
- Python 3.6+
- Cuenta de Twilio con:
  - Account SID
  - Auth Token
  - Número de WhatsApp configurado
  - Template de contenido aprobado

## Instalación
1. Clonar este repositorio
2. Crear un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Copiar .env.example a .env y completar con tus credenciales:
   ```
   cp .env.example .env
   ```

## Configuración
Edita el archivo .env con tus credenciales de Twilio:

```
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_CONTENT_SID=tu_content_sid
TWILIO_CONTENT_VARIABLES={"body":"Mensaje de ejemplo"}
TWILIO_WHATSAPP_TO=whatsapp:+1234567890
```

## Uso
### Modo Twilio (envío real)
```bash
python run.py --twilio
```

### Modo CLI (simulación)
```bash
python run.py --cli
```

## Variables de contenido
El formato de las variables de contenido debe coincidir con la plantilla configurada en Twilio. Para un template que espera variables específicas, configura `TWILIO_CONTENT_VARIABLES` en formato JSON según las necesidades de tu plantilla.

Por ejemplo:
```json
{"1": "valor1", "2": "valor2", "body": "Mensaje principal"}
```

## Arquitectura
Este proyecto implementa una arquitectura limpia (Clean Architecture) con las siguientes capas:
- **Entidades**: Objetos de negocio (WhatsappMessage)
- **Casos de uso**: Lógica de aplicación independiente de infraestructura
- **Adaptadores**: Conversión entre capas externas y casos de uso
- **Infraestructura**: Implementaciones concretas (API de Twilio)

Esta estructura permite cambiar fácilmente componentes (como el proveedor de mensajería) sin afectar la lógica central.