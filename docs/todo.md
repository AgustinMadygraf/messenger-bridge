# Documento Técnico: Refactorización y Mejoras Previas a `--twilio-respuesta`

## Objetivo

Definir y priorizar las tareas de refactorización y mejora arquitectónica necesarias para robustecer el sistema antes de implementar el modo `--twilio-respuesta`, siguiendo principios de arquitectura limpia y maximizando el impacto positivo en mantenibilidad, escalabilidad y calidad.

---

## Tareas Previas (Ordenadas por Impacto)

### 1. Estandarización de Casos de Uso
**Impacto:** Muy alto  
**Descripción:**  
- Unificar la estructura de los casos de uso (`use_cases`) para que todos sean clases con métodos claros, en vez de mezclar funciones y clases.
- Ejemplo: Convertir `send_whatsapp_message_use_case.py` en una clase, similar a otros casos de uso.
**Ventajas:**  
- Facilita la extensión y el testeo.
- Mejora la legibilidad y la coherencia del código.

---

### 2. Abstracción de Conversaciones
**Impacto:** Alto  
**Descripción:**  
- Crear una entidad o servicio `Conversation` para gestionar el historial de mensajes, tanto en CLI como en Twilio.
- Centralizar la lógica de manejo de conversaciones (agregar, recuperar, limpiar historial).
**Ventajas:**  
- Permite reutilizar la lógica en diferentes modos.
- Facilita la implementación de features como contexto conversacional y persistencia.

---

### 3. Separación de Presentación y Controlador
**Impacto:** Alto  
**Descripción:**  
- Asegurar que los presentadores (`presenters`) solo formateen la salida y los controladores (`controllers`) gestionen la lógica de negocio.
- Evitar que los controladores tengan lógica de presentación.
**Ventajas:**  
- Claridad de responsabilidades.
- Facilita cambios en la presentación sin afectar la lógica.

---

### 4. Refactorización de Webhook y Servicios
**Impacto:** Medio  
**Descripción:**  
- Separar la lógica de recepción de webhooks (Flask) de la lógica de procesamiento de mensajes.
- Implementar un adaptador para webhooks que delegue al controlador correspondiente.
**Ventajas:**  
- Permite testear la lógica de negocio sin depender del framework web.
- Mejora la escalabilidad y el mantenimiento.

---

### 5. Validación y Manejo de Errores Centralizado
**Impacto:** Medio  
**Descripción:**  
- Centralizar la validación de datos y el manejo de errores en los casos de uso y controladores.
- Evitar validaciones dispersas en la capa de infraestructura.
**Ventajas:**  
- Reduce duplicidad de código.
- Mejora la robustez y la trazabilidad de errores.

---

### 6. Documentación y Pruebas Unitarias
**Impacto:** Medio  
**Descripción:**  
- Documentar los flujos principales y las responsabilidades de cada módulo.
- Implementar pruebas unitarias para los casos de uso y controladores.
**Ventajas:**  
- Facilita onboarding y mantenimiento.
- Reduce el riesgo de regresiones.

---

## Resumen de Prioridad

1. **Estandarización de Casos de Uso**
2. **Abstracción de Conversaciones**
3. **Separación de Presentación y Controlador**
4. **Refactorización de Webhook y Servicios**
5. **Validación y Manejo de Errores Centralizado**
6. **Documentación y Pruebas Unitarias**

---

## Recomendación

Aborda las tareas en el orden propuesto para maximizar el impacto y preparar una base sólida antes de trabajar en `--twilio-respuesta`. Esto garantizará que la nueva funcionalidad se integre de forma limpia, escalable y mantenible.