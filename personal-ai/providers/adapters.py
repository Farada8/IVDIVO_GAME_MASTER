from __future__ import annotations

from typing import Any

from providers.base import (
    AIProvider,
    ProviderDescriptor,
    ProviderRequest,
    ProviderResponse,
    ProviderUnavailableError,
    ProviderUsage,
)
from providers.http import JsonTransport, UrllibJsonTransport


class OpenAIResponsesProvider(AIProvider):
    """OpenAI Responses API adapter. No SDK dependency."""

    name = "openai"

    def __init__(
        self,
        *,
        api_key: str | None,
        default_model: str | None = None,
        endpoint: str = "https://api.openai.com/v1/responses",
        transport: JsonTransport | None = None,
        timeout: float = 60.0,
    ) -> None:
        self._api_key = api_key or None
        self._default_model = default_model or None
        self._endpoint = endpoint
        self._transport = transport or UrllibJsonTransport()
        self._timeout = timeout

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=bool(self._api_key),
            network_required=True,
            endpoint=self._endpoint,
            default_model=self._default_model,
            contract="openai_responses_api",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        if not self._api_key:
            raise ProviderUnavailableError("openai is not configured: OPENAI_API_KEY is missing")
        model = self.resolve_model(request)
        payload: dict[str, Any] = {
            "model": model,
            "input": request.prompt,
            "max_output_tokens": request.max_output_tokens,
        }
        if request.system:
            payload["instructions"] = request.system
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        response = self._transport.post_json(
            provider=self.name,
            url=self._endpoint,
            headers={"Authorization": f"Bearer {self._api_key}"},
            payload=payload,
            timeout=self._timeout,
        )
        data = response.data
        text_parts: list[str] = []
        for output in data.get("output", []):
            if not isinstance(output, dict):
                continue
            for content in output.get("content", []):
                if isinstance(content, dict) and content.get("type") == "output_text":
                    text = content.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
        if not text_parts and isinstance(data.get("output_text"), str):
            text_parts.append(data["output_text"])
        usage_data = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        input_tokens = usage_data.get("input_tokens")
        output_tokens = usage_data.get("output_tokens")
        total_tokens = usage_data.get("total_tokens")
        return ProviderResponse(
            provider=self.name,
            model=str(data.get("model") or model),
            text="".join(text_parts),
            request_id=str(data["id"]) if data.get("id") is not None else None,
            usage=ProviderUsage(
                input_tokens=input_tokens if isinstance(input_tokens, int) else None,
                output_tokens=output_tokens if isinstance(output_tokens, int) else None,
                total_tokens=total_tokens if isinstance(total_tokens, int) else None,
            ),
            metadata={"http_status": response.status},
        )


class AnthropicMessagesProvider(AIProvider):
    """Claude Messages API adapter. No SDK dependency."""

    name = "anthropic"

    def __init__(
        self,
        *,
        api_key: str | None,
        default_model: str | None = None,
        endpoint: str = "https://api.anthropic.com/v1/messages",
        api_version: str = "2023-06-01",
        transport: JsonTransport | None = None,
        timeout: float = 60.0,
    ) -> None:
        self._api_key = api_key or None
        self._default_model = default_model or None
        self._endpoint = endpoint
        self._api_version = api_version
        self._transport = transport or UrllibJsonTransport()
        self._timeout = timeout

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=bool(self._api_key),
            network_required=True,
            endpoint=self._endpoint,
            default_model=self._default_model,
            contract="anthropic_messages_api",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        if not self._api_key:
            raise ProviderUnavailableError("anthropic is not configured: ANTHROPIC_API_KEY is missing")
        model = self.resolve_model(request)
        payload: dict[str, Any] = {
            "model": model,
            "max_tokens": request.max_output_tokens,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        if request.system:
            payload["system"] = request.system
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        response = self._transport.post_json(
            provider=self.name,
            url=self._endpoint,
            headers={
                "x-api-key": self._api_key,
                "anthropic-version": self._api_version,
            },
            payload=payload,
            timeout=self._timeout,
        )
        data = response.data
        text_parts: list[str] = []
        for content in data.get("content", []):
            if isinstance(content, dict) and content.get("type") == "text":
                text = content.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
        usage_data = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        input_tokens = usage_data.get("input_tokens")
        output_tokens = usage_data.get("output_tokens")
        total_tokens = (
            input_tokens + output_tokens
            if isinstance(input_tokens, int) and isinstance(output_tokens, int)
            else None
        )
        return ProviderResponse(
            provider=self.name,
            model=str(data.get("model") or model),
            text="".join(text_parts),
            request_id=str(data["id"]) if data.get("id") is not None else None,
            usage=ProviderUsage(
                input_tokens=input_tokens if isinstance(input_tokens, int) else None,
                output_tokens=output_tokens if isinstance(output_tokens, int) else None,
                total_tokens=total_tokens,
            ),
            metadata={"http_status": response.status},
        )


class OllamaChatProvider(AIProvider):
    """Local Ollama /api/chat adapter. Endpoint presence is not treated as a live health proof."""

    name = "ollama"

    def __init__(
        self,
        *,
        base_url: str = "http://localhost:11434",
        default_model: str | None = None,
        transport: JsonTransport | None = None,
        timeout: float = 120.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._default_model = default_model or None
        self._transport = transport or UrllibJsonTransport()
        self._timeout = timeout

    @property
    def endpoint(self) -> str:
        return f"{self._base_url}/api/chat"

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=bool(self._base_url),
            network_required=True,
            endpoint=self.endpoint,
            default_model=self._default_model,
            contract="ollama_local_chat_endpoint_not_health_probed",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        if not self._base_url:
            raise ProviderUnavailableError("ollama base URL is not configured")
        model = self.resolve_model(request)
        messages: list[dict[str, str]] = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        options: dict[str, Any] = {"num_predict": request.max_output_tokens}
        if request.temperature is not None:
            options["temperature"] = request.temperature
        response = self._transport.post_json(
            provider=self.name,
            url=self.endpoint,
            headers={},
            payload={"model": model, "messages": messages, "stream": False, "options": options},
            timeout=self._timeout,
        )
        data = response.data
        message = data.get("message") if isinstance(data.get("message"), dict) else {}
        text = message.get("content") if isinstance(message.get("content"), str) else ""
        input_tokens = data.get("prompt_eval_count")
        output_tokens = data.get("eval_count")
        total_tokens = (
            input_tokens + output_tokens
            if isinstance(input_tokens, int) and isinstance(output_tokens, int)
            else None
        )
        return ProviderResponse(
            provider=self.name,
            model=str(data.get("model") or model),
            text=text,
            request_id=str(data["created_at"]) if data.get("created_at") is not None else None,
            usage=ProviderUsage(
                input_tokens=input_tokens if isinstance(input_tokens, int) else None,
                output_tokens=output_tokens if isinstance(output_tokens, int) else None,
                total_tokens=total_tokens,
            ),
            metadata={
                "http_status": response.status,
                "done": bool(data.get("done")),
                "done_reason": data.get("done_reason"),
            },
        )
