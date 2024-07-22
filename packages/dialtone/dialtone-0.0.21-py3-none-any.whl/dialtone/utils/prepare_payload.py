from typing import Any
from dialtone.types import ChatMessage, Tool, DialtoneClient


def prepare_chat_message(message: ChatMessage | dict[str, Any]) -> dict:
    if isinstance(message, dict):
        return message

    result: dict[str, Any] = {
        "role": message.role,
        "content": message.content,
    }
    if message.tool_calls:
        result["tool_calls"] = (
            [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": (
                            tool_call.function.name if tool_call.function else None
                        ),
                        "arguments": (
                            tool_call.function.arguments if tool_call.function else None
                        ),
                    },
                }
                for tool_call in message.tool_calls
            ]
            if message.tool_calls
            else []
        )
    return result


def prepare_chat_completion(
    client: DialtoneClient,
    messages: list[ChatMessage] | list[dict[str, Any]],
    tools: list[Tool] = [],
) -> tuple[dict, dict]:
    headers = {"Authorization": f"Bearer {client.api_key}"}
    params = {
        "messages": [prepare_chat_message(message) for message in messages],
        "dials": client.dials.model_dump(),
        "provider_config": client.provider_config.model_dump(),
    }
    if client.router_model_config:
        params["router_model_config"] = client.router_model_config.model_dump()
    if client.fallback_config:
        params["fallback_config"] = client.fallback_config.model_dump()
    if client.tools_config:
        params["tools_config"] = client.tools_config.model_dump()
    if tools:
        params["tools"] = [tool.model_dump() for tool in tools]

    return headers, params


def prepare_chat_route(
    client: DialtoneClient,
    messages: list[ChatMessage] | list[dict[str, Any]],
    tools: list[Tool] = [],
) -> tuple[dict, dict]:
    headers = {"Authorization": f"Bearer {client.api_key}"}
    params = {
        "messages": [prepare_chat_message(message) for message in messages],
        "dials": client.dials.model_dump(),
        "provider_config": client.provider_config.model_dump(),
    }
    if client.router_model_config:
        params["router_model_config"] = client.router_model_config.model_dump()
    if client.fallback_config:
        params["fallback_config"] = client.fallback_config.model_dump()
    if client.tools_config:
        params["tools_config"] = client.tools_config.model_dump()
    if tools:
        params["tools"] = [tool.model_dump() for tool in tools]

    return headers, params
