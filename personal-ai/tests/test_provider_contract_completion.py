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
        self.calls.append({
            "provider": provider,
            "url": url,
            "headers": dict(headers),
            "payload": dict(payload),
            "timeout": timeout,
        })
        return JsonHTTPResponse(status=200, headers={}, data=self.responses[provider])


class ProviderContractCompletionTest(unittest.TestCase):
    def test_ai_provider_exposes_four_required_methods(self) -> None:
        for method in ("generate", "analyze", "classify", "extract"):
            self.assertTrue(callable(getattr(AIProvider, method)))

    def test_mock_executes_all_four_without_network(self) -> None:
        provider = MockProvider()
        request = ProviderRequest(prompt="client asks for insulation quote")
        generated = provider.generate(request)
        analyzed = provider.analyze(request, instruction="identify requested service")
        classified = provider.classify(request, labels=["LEAD", "OTHER"])
        extracted = provider.extract(request, schema={"service": "string", "price": "number|null"})
        self.assertFalse(generated.metadata["network_used"])
        self.assertEqual(analyzed.metadata["operation"], "analyze")
        self.assertEqual(classified.metadata["operation"], "classify")
        self.assertEqual(extracted.metadata["operation"], "extract")
        self.assertIn("ANALYZE", analyzed.text)
        self.assertIn("CLASSIFY", classified.text)
        self.assertIn("EXTRACT", extracted.text)

    def test_canonical_class_names_exist(self) -> None:
        self.assertTrue(issubclass(OpenAIProvider, AIProvider))
        self.assertTrue(issubclass(AnthropicProvider, AIProvider))
        self.assertTrue(issubclass(OllamaProvider, AIProvider))

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

    def test_registry_all_four_operations(self) -> None:
        registry = default_registry(env={})
        request = ProviderRequest(prompt="hello")
        self.assertEqual(registry.generate("mock", request).provider, "mock")
        self.assertEqual(registry.analyze("mock", request).metadata["operation"], "analyze")
        self.assertEqual(registry.classify("mock", request, labels=["A", "B"]).metadata["operation"], "classify")
        self.assertEqual(registry.extract("mock", request, schema={"x": "string"}).metadata["operation"], "extract")

    def test_unknown_and_unconfigured_providers_fail_closed(self) -> None:
        with self.assertRaises(KeyError):
            provider_from_config(ProviderConfig(provider="unknown"), env={})
        registry = default_registry(env={})
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("openai", ProviderRequest(prompt="x", model="model"))
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("anthropic", ProviderRequest(prompt="x", model="model"))
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("ollama", ProviderRequest(prompt="x"))

    def test_openai_canonical_adapter_fake_transport(self) -> None:
        fake = FakeTransport({"openai": {"id": "r1", "model": "gpt-test", "output_text": "ok", "usage": {"input_tokens": 2, "output_tokens": 1, "total_tokens": 3}}})
        provider = OpenAIProvider(api_key="secret", default_model="gpt-test", transport=fake)
        self.assertEqual(provider.generate(ProviderRequest(prompt="q")).text, "ok")
        self.assertEqual(fake.calls[0]["provider"], "openai")

    def test_anthropic_canonical_adapter_fake_transport(self) -> None:
        fake = FakeTransport({"anthropic": {"id": "m1", "model": "claude-test", "content": [{"type": "text", "text": "ok"}], "usage": {"input_tokens": 2, "output_tokens": 1}}})
        provider = AnthropicProvider(api_key="secret", default_model="claude-test", transport=fake)
        self.assertEqual(provider.generate(ProviderRequest(prompt="q")).text, "ok")

    def test_ollama_canonical_adapter_fake_transport(self) -> None:
        fake = FakeTransport({"ollama": {"model": "local-test", "created_at": "time", "message": {"role": "assistant", "content": "ok"}, "done": True, "prompt_eval_count": 2, "eval_count": 1}})
        provider = OllamaProvider(default_model="local-test", transport=fake)
        self.assertEqual(provider.generate(ProviderRequest(prompt="q")).text, "ok")

    def test_validation_is_fail_closed(self) -> None:
        provider = MockProvider()
        request = ProviderRequest(prompt="x")
        with self.assertRaises(ValueError):
            provider.classify(request, labels=[])
        with self.assertRaises(ValueError):
            provider.extract(request, schema="   ")
        with self.assertRaises(ValueError):
            ProviderConfig(provider="mock", max_tokens=0)


if __name__ == "__main__":
    unittest.main()
