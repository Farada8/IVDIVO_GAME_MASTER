from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from providers import (
    AIProvider,
    AnthropicProvider,
    MockProvider,
    OllamaProvider,
    OpenAIProvider,
    ProviderConfig,
    ProviderRequest,
    ProviderUnavailableError,
    default_registry,
    provider_from_config,
)
from providers.http import JsonHTTPResponse


class FakeTransport:
    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    def post_json(
        self,
        *,
        provider: str,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout: float,
    ) -> JsonHTTPResponse:
        self.calls.append(
            {
                "provider": provider,
                "url": url,
                "headers": dict(headers),
                "payload": dict(payload),
                "timeout": timeout,
            }
        )
        return JsonHTTPResponse(status=200, headers={}, data=self.responses[provider])


class ProviderAbstractionTest(unittest.TestCase):
    def test_contract_exposes_all_four_required_methods(self) -> None:
        for method in ("generate", "analyze", "classify", "extract"):
            self.assertTrue(callable(getattr(AIProvider, method)))

    def test_mock_runs_all_four_operations_without_network(self) -> None:
        provider = MockProvider()
        request = ProviderRequest(prompt="A client asks for an insulation quote")
        generated = provider.generate(request)
        analyzed = provider.analyze(request, instruction="Identify the request")
        classified = provider.classify(request, labels=["LEAD", "SUPPORT", "OTHER"])
        extracted = provider.extract(request, schema={"service": "string", "price": "number|null"})
        self.assertEqual(generated.metadata["network_used"], False)
        self.assertEqual(analyzed.metadata["operation"], "analyze")
        self.assertEqual(classified.metadata["operation"], "classify")
        self.assertEqual(extracted.metadata["operation"], "extract")
        self.assertIn("ANALYZE", analyzed.text)
        self.assertIn("CLASSIFY", classified.text)
        self.assertIn("EXTRACT", extracted.text)

    def test_required_canonical_provider_class_names_exist(self) -> None:
        self.assertTrue(issubclass(OpenAIProvider, AIProvider))
        self.assertTrue(issubclass(AnthropicProvider, AIProvider))
        self.assertTrue(issubclass(OllamaProvider, AIProvider))
        self.assertTrue(issubclass(MockProvider, AIProvider))

    def test_config_supports_required_fields_without_secret_value(self) -> None:
        secret_value = "NEVER-SERIALIZE-ME"
        config = ProviderConfig(
            provider="openai",
            model="model-test",
            temperature=0.25,
            max_tokens=321,
            endpoint="https://example.invalid/v1",
            secret_env="OPENAI_API_KEY",
        )
        rendered = json.dumps(config.public_dict(), sort_keys=True)
        self.assertNotIn(secret_value, rendered)
        self.assertIn("OPENAI_API_KEY", rendered)
        request = config.request("hello")
        self.assertEqual(request.model, "model-test")
        self.assertEqual(request.temperature, 0.25)
        self.assertEqual(request.max_output_tokens, 321)

    def test_unknown_provider_fails_closed(self) -> None:
        with self.assertRaises(KeyError):
            provider_from_config(ProviderConfig(provider="unknown"), env={})
        registry = default_registry(env={})
        with self.assertRaises(KeyError):
            registry.generate("unknown", ProviderRequest(prompt="x"))

    def test_unconfigured_paid_providers_do_not_fallback_to_mock(self) -> None:
        registry = default_registry(env={})
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("openai", ProviderRequest(prompt="x", model="model"))
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("anthropic", ProviderRequest(prompt="x", model="model"))
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("ollama", ProviderRequest(prompt="x"))

    def test_registry_exposes_all_four_operations(self) -> None:
        registry = default_registry(env={})
        request = ProviderRequest(prompt="hello")
        self.assertEqual(registry.generate("mock", request).provider, "mock")
        self.assertEqual(registry.analyze("mock", request).metadata["operation"], "analyze")
        self.assertEqual(
            registry.classify("mock", request, labels=["A", "B"]).metadata["operation"],
            "classify",
        )
        self.assertEqual(
            registry.extract("mock", request, schema={"x": "string"}).metadata["operation"],
            "extract",
        )

    def test_openai_adapter_with_fake_transport(self) -> None:
        fake = FakeTransport(
            {
                "openai": {
                    "id": "resp_1",
                    "model": "gpt-test",
                    "output": [
                        {"type": "message", "content": [{"type": "output_text", "text": "ok"}]}
                    ],
                    "usage": {"input_tokens": 2, "output_tokens": 1, "total_tokens": 3},
                }
            }
        )
        provider = OpenAIProvider(api_key="secret", default_model="gpt-test", transport=fake)
        response = provider.generate(ProviderRequest(prompt="question"))
        self.assertEqual(response.text, "ok")
        self.assertEqual(fake.calls[0]["provider"], "openai")
        self.assertEqual(fake.calls[0]["headers"]["Authorization"], "Bearer secret")

    def test_anthropic_adapter_with_fake_transport(self) -> None:
        fake = FakeTransport(
            {
                "anthropic": {
                    "id": "msg_1",
                    "model": "claude-test",
                    "content": [{"type": "text", "text": "ok"}],
                    "usage": {"input_tokens": 2, "output_tokens": 1},
                }
            }
        )
        provider = AnthropicProvider(api_key="secret", default_model="claude-test", transport=fake)
        response = provider.generate(ProviderRequest(prompt="question"))
        self.assertEqual(response.text, "ok")
        self.assertEqual(fake.calls[0]["headers"]["x-api-key"], "secret")

    def test_ollama_adapter_with_fake_transport(self) -> None:
        fake = FakeTransport(
            {
                "ollama": {
                    "model": "local-test",
                    "created_at": "time",
                    "message": {"role": "assistant", "content": "ok"},
                    "done": True,
                    "prompt_eval_count": 2,
                    "eval_count": 1,
                }
            }
        )
        provider = OllamaProvider(default_model="local-test", transport=fake)
        response = provider.generate(ProviderRequest(prompt="question"))
        self.assertEqual(response.text, "ok")
        self.assertEqual(fake.calls[0]["url"], "http://localhost:11434/api/chat")

    def test_operation_validation_is_fail_closed(self) -> None:
        provider = MockProvider()
        request = ProviderRequest(prompt="x")
        with self.assertRaises(ValueError):
            provider.classify(request, labels=[])
        with self.assertRaises(ValueError):
            provider.extract(request, schema="   ")
        with self.assertRaises(ValueError):
            ProviderConfig(provider="mock", max_tokens=0)
        with self.assertRaises(ValueError):
            ProviderRequest(prompt="x", temperature=3)


if __name__ == "__main__":
    unittest.main()
