from __future__ import annotations

import os
from collections.abc import Mapping

from providers.adapters import AnthropicMessagesProvider, OllamaChatProvider, OpenAIResponsesProvider
from providers.base import AIProvider, ProviderRequest, ProviderResponse
from providers.http import JsonTransport
from providers.mock import MockProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        name = provider.name.strip().lower()
        if not name:
            raise ValueError("provider name cannot be empty")
        if name in self._providers:
            raise ValueError(f"provider already registered: {name}")
        self._providers[name] = provider

    def get(self, name: str) -> AIProvider:
        key = name.strip().lower()
        try:
            return self._providers[key]
        except KeyError as exc:
            raise KeyError(f"unknown provider: {name}") from exc

    def describe_all(self) -> list[dict]:
        return [self._providers[name].describe().to_dict() for name in sorted(self._providers)]

    def generate(self, provider_name: str, request: ProviderRequest) -> ProviderResponse:
        return self.get(provider_name).generate(request)


def default_registry(
    *,
    env: Mapping[str, str] | None = None,
    transport: JsonTransport | None = None,
) -> ProviderRegistry:
    source = os.environ if env is None else env
    registry = ProviderRegistry()
    registry.register(MockProvider())
    registry.register(
        OpenAIResponsesProvider(
            api_key=source.get("OPENAI_API_KEY"),
            default_model=source.get("OPENAI_MODEL"),
            endpoint=source.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses"),
            transport=transport,
        )
    )
    registry.register(
        AnthropicMessagesProvider(
            api_key=source.get("ANTHROPIC_API_KEY"),
            default_model=source.get("ANTHROPIC_MODEL"),
            endpoint=source.get("ANTHROPIC_MESSAGES_URL", "https://api.anthropic.com/v1/messages"),
            api_version=source.get("ANTHROPIC_API_VERSION", "2023-06-01"),
            transport=transport,
        )
    )
    registry.register(
        OllamaChatProvider(
            base_url=source.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            default_model=source.get("OLLAMA_MODEL"),
            transport=transport,
        )
    )
    return registry
