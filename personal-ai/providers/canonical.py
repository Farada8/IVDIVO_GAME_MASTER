from __future__ import annotations

from providers.adapters import AnthropicMessagesProvider, OllamaChatProvider, OpenAIResponsesProvider


class OpenAIProvider(OpenAIResponsesProvider):
    """Canonical PL-04 OpenAI provider surface."""


class AnthropicProvider(AnthropicMessagesProvider):
    """Canonical PL-04 Anthropic provider surface."""


class OllamaProvider(OllamaChatProvider):
    """Canonical PL-04 Ollama provider surface."""
