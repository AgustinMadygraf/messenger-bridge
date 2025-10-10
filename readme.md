# Messenger Bridge

## 📢 Descripción
Messenger Bridge es un sistema de integración avanzado que conecta diferentes plataformas de mensajería (WhatsApp vía Twilio y Telegram) con motores conversacionales inteligentes. Permite mantener conversaciones fluidas a través de distintos canales de comunicación, centralizando la lógica de negocio en un solo lugar.

Este puente facilita que cualquier motor conversacional interactúe con usuarios reales a través de las plataformas de mensajería más populares, sin preocuparse por la complejidad de cada API.

## ✨ Características principales
- 🤖 **Integración con múltiples motores**: Compatible con Rasa, GPT4All, OpenAI, Gemini y cualquier sistema con API REST
- 📱 **Soporte para WhatsApp**: Integración completa con WhatsApp Business API a través de Twilio
- ✈️ **Soporte para Telegram**: Implementación robusta del API de bots de Telegram
- 🔊 **Procesamiento avanzado de audio**: Transcripción de mensajes de voz (online y offline)
- 🌐 **Exposición de webhooks**: Configuración automática mediante ngrok para desarrollo y pruebas
- 🧩 **Arquitectura modular**: Fácilmente extensible para añadir nuevos canales o funcionalidades
- 🔄 **Conversaciones contextuales**: Mantiene el contexto entre diferentes mensajes y plataformas

## 🚀 Casos de uso

- **Atención al cliente**: Chatbots multicanal que responden consultas en tiempo real
- **Asistentes personales**: Servicios automatizados accesibles desde WhatsApp o Telegram
- **Educación**: Plataformas de aprendizaje interactivas a través de mensajería
- **Herramientas internas**: Bots empresariales para consultas a sistemas internos
- **Accesibilidad**: Interfaces conversacionales para personas con discapacidad visual

## 🔧 Inicio rápido

1. Clonar el repositorio
   ```bash
   git clone https://github.com/AgustinMadygraf/messenger-bridge.git
   ```
2. Configurar el archivo `.env` (basado en `.env.example`)
3. Ejecutar `python run.py`

Para instrucciones detalladas, consulte la [guía de instalación](docs/installation.md).

## 🔌 Integración

Este sistema está diseñado para funcionar con el repositorio [`AgustinMadygraf/rasa-gemini-bot`](https://github.com/AgustinMadygraf/rasa-gemini-bot.gt) u otros motores conversacionales compatibles que implementen la API esperada.

### Diagrama de flujo
```
Usuario (WhatsApp/Telegram) → Messenger Bridge → Motor Conversacional → Messenger Bridge → Usuario
```

## 🏗️ Arquitectura

El proyecto sigue principios de **Clean Architecture**, facilitando pruebas, mantenimiento y extensibilidad:

- **entities/**: Objetos de dominio independientes de frameworks
- **use_cases/**: Lógica de negocio y reglas de la aplicación
- **interface_adapter/**: Controladores, presentadores e interfaces para servicios
- **infrastructure/**: Implementaciones concretas para cada plataforma
- **shared/**: Utilidades compartidas entre capas

## 💡 ¿Por qué contribuir?

- **Proyecto en crecimiento**: Oportunidad de impactar desde etapas tempranas
- **Aprendizaje valioso**: Experiencia con arquitectura limpia, APIs de mensajería y sistemas conversacionales
- **Aplicación práctica**: Solución a problemas reales de comunicación automatizada
- **Comunidad activa**: Colaboración con otros desarrolladores interesados en IA conversacional

## 🗺️ Roadmap

Estas son algunas mejoras y nuevas funcionalidades que planeamos incorporar:

- [ ] Transcripción automática de mensajes de audio
- [ ] Almacenamiento de conversaciones con MongoDB
- [ ] Soporte para Discord como nuevo canal de mensajería
- [ ] Panel web para administración y monitoreo de conversaciones

Si tienes ideas o sugerencias, ¡no dudes en compartirlas!

## 🤝 Cómo contribuir

¿Te gustaría colaborar? Consulta la [guía de contribución](docs/CONTRIBUTING.md) para ver los pasos y recomendaciones.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Puedes consultar los detalles en el archivo [LICENSE](LICENSE).

---

<p align="center">
  Desarrollado con ❤️ por la comunidad
</p>