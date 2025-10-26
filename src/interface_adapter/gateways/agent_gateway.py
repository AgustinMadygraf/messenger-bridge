"""
Path: src/interface_adapter/gateways/agent_gateway.py
"""



class AgentGateway:
    "Interfaz para comunicarse con un modelo Rasa."
    def __init__(self, agent_bot_url: str, http_client):
        self.agent_bot_url = agent_bot_url
        self.http_client = http_client

    def get_response(self, message_or_text) -> str:
        "Envía un mensaje al bot Rasa y devuelve la respuesta."
        if isinstance(message_or_text, str):
            payload = {"sender": "user", "message": message_or_text}
        else:
            payload = {"sender": "user", "message": message_or_text.body}
            if hasattr(message_or_text, 'media_url') and message_or_text.media_url:
                payload["media_url"] = message_or_text.media_url
                payload["media_type"] = message_or_text.media_type

        try:
            response = self.http_client.post(self.agent_bot_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return " ".join([msg.get("text", "") for msg in data if "text" in msg])
        except (ValueError, AttributeError) as e:
            return f"[Error procesando la respuesta de Rasa: {e}]"
