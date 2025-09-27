"""
Path: run.py
"""

import argparse
import json
from src.shared.logger import get_logger
from src.composer_root import (
    compose_twilio_plantilla,
    compose_cli_plantilla,
    compose_cli_respuesta,
    compose_twilio_respuesta
)

if __name__ == "__main__":
    logger = get_logger("twilio-bot.run")
    parser = argparse.ArgumentParser(description="Enviar mensaje WhatsApp por Twilio o CLI (plantilla)")
    parser.add_argument('--twilio-plantilla', action='store_true', help='Usar Twilio para enviar el mensaje con plantilla')
    parser.add_argument('--cli-plantilla', action='store_true', help='Simular envío de mensaje por CLI con plantilla')
    parser.add_argument('--cli-respuesta', action='store_true', help='Simular recepción y respuesta de mensajes por CLI')
    parser.add_argument('--twilio-respuesta', action='store_true', help='Recibir y responder mensajes reales por Twilio (webhook)')
    args = parser.parse_args()

    if args.twilio_plantilla:
        controller, presenter, config = compose_twilio_plantilla()
    elif args.cli_plantilla:
        controller, presenter, config = compose_cli_plantilla()
    elif args.cli_respuesta:
        controller, presenter = compose_cli_respuesta()
        conversation_history = []
        print("[CLI] Modo respuesta. Escribe un mensaje para simular recepción (escribe 'salir' para terminar):")
        try:
            while True:
                user_input = input("Usuario: ")
                if user_input.strip().lower() in ("salir", "exit", "quit"):
                    print("Saliendo del modo CLI respuesta.")
                    break
                conversation_history.append(f"Usuario: {user_input}")
                PROMPT = "\n".join(conversation_history)
                response = controller.handle_prompt(PROMPT)
                conversation_history.append(f"Bot: {response}")
                print(presenter.present(response))
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo del modo CLI respuesta.")
        exit(0)
    elif args.twilio_respuesta:
        run_flask_webhook = compose_twilio_respuesta()
        run_flask_webhook()
        exit(0)
    else:
        logger.error("Debe especificar --twilio-plantilla, --cli-plantilla, --cli-respuesta o --twilio-respuesta")
        exit(1)

    # Solo para los modos plantilla
    if args.twilio_plantilla or args.cli_plantilla:
        content_variables = config["CONTENT_VARIABLES"]
        if isinstance(content_variables, str):
            try:
                content_variables = json.loads(content_variables)
            except json.JSONDecodeError:
                logger.warning("CONTENT_VARIABLES no es JSON válido, usando como body")
                content_variables = {"body": content_variables}
        logger.debug("content_variables antes de enviar al controlador: %s (tipo: %s)", content_variables, type(content_variables))
        result = controller.send_message(
            content_sid=config["CONTENT_SID"],
            content_variables=content_variables,
            to=config["WHATSAPP_TO"]
        )
        logger.info(presenter.present(result))
