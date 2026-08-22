from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any


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


class AIProvider(ABC):
    name: str

    @abstractmethod
    def describe(self) -> ProviderDescriptor:
        raise NotImplementedError

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError

    def resolve_model(self, request: ProviderRequest) -> str:
        descriptor = self.describe()
        model = request.model or descriptor.default_model
        if not model:
            raise ProviderUnavailableError(
                f"{self.name} requires an explicit model or configured default model"
            )
        return model
