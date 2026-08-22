from __future__ import annotations

from providers.base import (
    AIProvider,
    ProviderDescriptor,
    ProviderRequest,
    ProviderResponse,
    ProviderUsage,
)


class MockProvider(AIProvider):
    name = "mock"

    def __init__(self, fixed_text: str | None = None) -> None:
        self.fixed_text = fixed_text

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=True,
            network_required=False,
            endpoint=None,
            default_model="mock-v1",
            contract="deterministic_test_provider",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        model = self.resolve_model(request)
        text = self.fixed_text if self.fixed_text is not None else f"MOCK_RESPONSE: {request.prompt}"
        return ProviderResponse(
            provider=self.name,
            model=model,
            text=text,
            request_id="mock-request",
            usage=ProviderUsage(),
            metadata={"deterministic": True, "network_used": False},
        )
