from typing import Any
from pydantic import BaseModel
from dialtone.types import (
    ChatCompletionChunk,
    FallbackConfig,
    ProviderConfig,
    RouterModelConfig,
    ChatCompletion,
    Choice,
    ChatMessage,
    Tool,
    DialtoneClient,
    Dials,
    RouteDecision,
    TokenUsage,
    ToolsConfig,
)
from dialtone.dialtone.dialtone_base import DialtoneBase
from dialtone.utils.api import (
    convert_dict_to_type_stream,
    dialtone_post_request_async,
    dialtone_streaming_post_request_async,
)
from dialtone.utils.prepare_payload import prepare_chat_completion, prepare_chat_route
from dialtone.config import DEFAULT_BASE_URL


class Completions(BaseModel):
    client: DialtoneClient

    async def create(
        self,
        messages: list[ChatMessage] | list[dict],
        stream: bool = False,
        tools: list[Tool] = [],
    ):
        # validate inputs
        if stream and len(tools) > 0:
            raise ValueError(
                "Error: Streaming with tools is not supported by Dialtone yet. Either set stream to False or omit tools."
            )

        headers, params = prepare_chat_completion(
            messages=messages, stream=stream, tools=tools, client=self.client
        )

        if stream:
            return convert_dict_to_type_stream(
                dialtone_streaming_post_request_async(
                    url=f"{self.client.base_url}/chat/completions",
                    data=params,
                    headers=headers,
                ),
                ChatCompletionChunk,
            )

        response_json = await dialtone_post_request_async(
            url=f"{self.client.base_url}/chat/completions",
            data=params,
            headers=headers,
        )

        return ChatCompletion(
            model=response_json["model"],
            provider=response_json["provider"],
            choices=[
                Choice(
                    message=response_json["message"],
                )
            ],
            usage=TokenUsage(**response_json["usage"]),
        )


class Chat(BaseModel):
    client: DialtoneClient
    completions: Completions

    def __init__(self, client: DialtoneClient):
        completions = Completions(client=client)
        super().__init__(client=client, completions=completions)

    async def route(
        self, messages: list[ChatMessage] | list[dict[str, Any]], tools: list[Tool] = []
    ):
        headers, params = prepare_chat_route(
            messages=messages, tools=tools, client=self.client
        )

        response_json = await dialtone_post_request_async(
            url=f"{self.client.base_url}/chat/route",
            data=params,
            headers=headers,
            timeout=15,
        )

        return RouteDecision(
            model=response_json["model"],
            providers=response_json["providers"],
            quality_predictions=response_json["quality_predictions"],
            routing_strategy=response_json["routing_strategy"],
        )


class AsyncDialtone(DialtoneBase):
    chat: Chat
    client: DialtoneClient

    def __init__(
        self,
        api_key: str,
        provider_config: ProviderConfig | dict[str, Any],
        dials: Dials | dict[str, Any] = Dials(),
        router_model_config: RouterModelConfig | dict[str, Any] = RouterModelConfig(),
        fallback_config: FallbackConfig | dict[str, Any] = FallbackConfig(),
        tools_config: ToolsConfig | dict[str, Any] = ToolsConfig(),
        base_url: str = DEFAULT_BASE_URL,
    ):
        super().validate_inputs(
            provider_config=provider_config,
            dials=dials,
            router_model_config=router_model_config,
            fallback_config=fallback_config,
            tools_config=tools_config,
        )

        if isinstance(dials, dict):
            dials = Dials(**dials)
        if isinstance(provider_config, dict):
            provider_config = ProviderConfig(**provider_config)
        if isinstance(router_model_config, dict):
            router_model_config = RouterModelConfig(**router_model_config)
        if isinstance(fallback_config, dict):
            fallback_config = FallbackConfig(**fallback_config)
        if isinstance(tools_config, dict):
            tools_config = ToolsConfig(**tools_config)

        self.client = DialtoneClient(
            api_key=api_key,
            dials=dials,
            provider_config=provider_config,
            router_model_config=router_model_config,
            fallback_config=fallback_config,
            tools_config=tools_config,
            base_url=base_url,
        )
        self.chat = Chat(client=self.client)
