from __future__ import annotations

import os
from collections.abc import Mapping

from providers.base import AIProvider, ProviderConfig, ProviderRequest, ProviderResponse
from providers.canonical import AnthropicProvider, OllamaProvider, OpenAIProvider
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

    def analyze(
        self,
        provider_name: str,
        request: ProviderRequest,
        *,
        instruction: str | None = None,
    ) -> ProviderResponse:
        return self.get(provider_name).analyze(request, instruction=instruction)

    def classify(
        self,
        provider_name: str,
        request: ProviderRequest,
        *,
        labels: list[str] | tuple[str, ...],
    ) -> ProviderResponse:
        return self.get(provider_name).classify(request, labels=labels)

    def extract(
        self,
        provider_name: str,
        request: ProviderRequest,
        *,
        schema: Mapping[str, object] | str,
    ) -> ProviderResponse:
        return self.get(provider_name).extract(request, schema=schema)


def provider_from_config(
    config: ProviderConfig,
    *,
    env: Mapping[str, str] | None = None,
    transport: JsonTransport | None = None,
) -> AIProvider:
    source = os.environ if env is None else env
    name = config.provider.strip().lower()
    if name == "mock":
        return MockProvider()
    if name == "openai":
        secret_name = config.secret_env or "OPENAI_API_KEY"
        return OpenAIProvider(
            api_key=source.get(secret_name),
            default_model=config.model,
            endpoint=config.endpoint or "https://api.openai.com/v1/responses",
            transport=transport,
        )
    if name == "anthropic":
        secret_name = config.secret_env or "ANTHROPIC_API_KEY"
        return AnthropicProvider(
            api_key=source.get(secret_name),
            default_model=config.model,
            endpoint=config.endpoint or "https://api.anthropic.com/v1/messages",
            transport=transport,
        )
    if name == "ollama":
        return OllamaProvider(
            base_url=config.endpoint or "http://localhost:11434",
            default_model=config.model,
            transport=transport,
        )
    raise KeyError(f"unknown provider: {config.provider}")


def default_registry(
    *,
    env: Mapping[str, str] | None = None,
    transport: JsonTransport | None = None,
) -> ProviderRegistry:
    source = os.environ if env is None else env
    registry = ProviderRegistry()
    registry.register(MockProvider())
    registry.register(
        provider_from_config(
            ProviderConfig(
                provider="openai",
                model=source.get("OPENAI_MODEL"),
                endpoint=source.get("OPENAI_RESPONSES_URL"),
                secret_env="OPENAI_API_KEY",
            ),
            env=source,
            transport=transport,
        )
    )
    registry.register(
        provider_from_config(
            ProviderConfig(
                provider="anthropic",
                model=source.get("ANTHROPIC_MODEL"),
                endpoint=source.get("ANTHROPIC_MESSAGES_URL"),
                secret_env="ANTHROPIC_API_KEY",
            ),
            env=source,
            transport=transport,
        )
    )
    registry.register(
        provider_from_config(
            ProviderConfig(
                provider="ollama",
                model=source.get("OLLAMA_MODEL"),
                endpoint=source.get("OLLAMA_BASE_URL"),
            ),
            env=source,
            transport=transport,
        )
    )
    return registry
