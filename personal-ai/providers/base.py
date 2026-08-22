from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Mapping


class ProviderError(RuntimeError):
    """Base error for provider-layer failures."""


class ProviderUnavailableError(ProviderError):
    """Raised when a provider is not configured or cannot be used."""


class ProviderHTTPError(ProviderError):
    def __init__(self, provider: str, status: int, message: str = "provider request failed") -> None:
        super().__init__(f"{provider} HTTP {status}: {message}")
        self.provider = provider
        self.status = status


@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    model: str | None = None
    system: str | None = None
    max_output_tokens: int = 512
    temperature: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")
        if self.model is not None and not self.model.strip():
            raise ValueError("model cannot be blank")
        if self.max_output_tokens < 1:
            raise ValueError("max_output_tokens must be positive")
        if self.temperature is not None and not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")


@dataclass(frozen=True)
class ProviderUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True)
class ProviderResponse:
    provider: str
    model: str
    text: str
    request_id: str | None = None
    usage: ProviderUsage = field(default_factory=ProviderUsage)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderDescriptor:
    name: str
    configured: bool
    network_required: bool
    endpoint: str | None
    default_model: str | None
    contract: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    model: str | None = None
    temperature: float | None = None
    max_tokens: int = 512
    endpoint: str | None = None
    secret_env: str | None = None

    def __post_init__(self) -> None:
        if not self.provider.strip():
            raise ValueError("provider cannot be empty")
        if self.model is not None and not self.model.strip():
            raise ValueError("model cannot be blank")
        if self.temperature is not None and not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")

    def public_dict(self) -> dict[str, Any]:
        return asdict(self)

    def request(self, prompt: str, *, system: str | None = None) -> ProviderRequest:
        return ProviderRequest(
            prompt=prompt,
            model=self.model,
            system=system,
            max_output_tokens=self.max_tokens,
            temperature=self.temperature,
        )


class AIProvider(ABC):
    name: str

    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError

    def _operation(
        self,
        request: ProviderRequest,
        *,
        operation: str,
        prompt: str,
    ) -> ProviderResponse:
        derived = replace(
            request,
            prompt=prompt,
            metadata={**request.metadata, "operation": operation},
        )
        response = self.generate(derived)
        return replace(response, metadata={**response.metadata, "operation": operation})

    def analyze(self, request: ProviderRequest, *, instruction: str | None = None) -> ProviderResponse:
        instruction = (instruction or "Analyze the content. Distinguish observations from inference.").strip()
        if not instruction:
            raise ValueError("analysis instruction cannot be empty")
        return self._operation(
            request,
            operation="analyze",
            prompt=f"ANALYZE\nINSTRUCTION: {instruction}\nCONTENT:\n{request.prompt}",
        )

    def classify(
        self,
        request: ProviderRequest,
        *,
        labels: list[str] | tuple[str, ...],
    ) -> ProviderResponse:
        normalized = [label.strip() for label in labels if label.strip()]
        if not normalized:
            raise ValueError("classification labels cannot be empty")
        return self._operation(
            request,
            operation="classify",
            prompt=(
                "CLASSIFY\nChoose exactly one allowed label and return that label.\n"
                f"LABELS: {json.dumps(normalized, ensure_ascii=False)}\nCONTENT:\n{request.prompt}"
            ),
        )

    def extract(
        self,
        request: ProviderRequest,
        *,
        schema: Mapping[str, Any] | str,
    ) -> ProviderResponse:
        if isinstance(schema, str):
            schema_text = schema.strip()
            if not schema_text:
                raise ValueError("extraction schema cannot be empty")
        else:
            schema_text = json.dumps(dict(schema), ensure_ascii=False, sort_keys=True)
        return self._operation(
            request,
            operation="extract",
            prompt=(
                "EXTRACT\nReturn only data supported by the content. Use null for unknown fields.\n"
                f"SCHEMA: {schema_text}\nCONTENT:\n{request.prompt}"
            ),
        )

    def resolve_model(self, request: ProviderRequest) -> str:
        descriptor = self.describe()
        model = request.model or descriptor.default_model
        if not model:
            raise ProviderUnavailableError(
                f"{self.name} requires an explicit model or configured default model"
            )
        return model
