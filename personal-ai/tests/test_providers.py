from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from providers.adapters import AnthropicMessagesProvider, OllamaChatProvider, OpenAIResponsesProvider
from providers.base import ProviderRequest, ProviderUnavailableError
from providers.http import JsonHTTPResponse
from providers.registry import default_registry


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
    def test_registry_describe_never_exposes_secrets(self) -> None:
        secret_openai = "openai-secret-value"
        secret_anthropic = "anthropic-secret-value"
        registry = default_registry(
            env={
                "OPENAI_API_KEY": secret_openai,
                "ANTHROPIC_API_KEY": secret_anthropic,
                "OPENAI_MODEL": "test-openai",
                "ANTHROPIC_MODEL": "test-anthropic",
                "OLLAMA_MODEL": "test-local",
            }
        )
        rendered = json.dumps(registry.describe_all(), sort_keys=True)
        self.assertNotIn(secret_openai, rendered)
        self.assertNotIn(secret_anthropic, rendered)
        by_name = {item["name"]: item for item in registry.describe_all()}
        self.assertTrue(by_name["mock"]["configured"])
        self.assertTrue(by_name["openai"]["configured"])
        self.assertTrue(by_name["anthropic"]["configured"])
        self.assertTrue(by_name["ollama"]["configured"])

    def test_mock_provider_is_deterministic_and_network_free(self) -> None:
        registry = default_registry(env={})
        response = registry.generate("mock", ProviderRequest(prompt="hello"))
        self.assertEqual(response.provider, "mock")
        self.assertEqual(response.model, "mock-v1")
        self.assertEqual(response.text, "MOCK_RESPONSE: hello")
        self.assertFalse(response.metadata["network_used"])

    def test_unconfigured_paid_providers_fail_closed(self) -> None:
        registry = default_registry(env={})
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("openai", ProviderRequest(prompt="x", model="some-model"))
        with self.assertRaises(ProviderUnavailableError):
            registry.generate("anthropic", ProviderRequest(prompt="x", model="some-model"))

    def test_openai_adapter_request_and_response_without_network(self) -> None:
        fake = FakeTransport(
            {
                "openai": {
                    "id": "resp_1",
                    "model": "gpt-test",
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "output_text", "text": "openai result"}],
                        }
                    ],
                    "usage": {"input_tokens": 7, "output_tokens": 3, "total_tokens": 10},
                }
            }
        )
        provider = OpenAIResponsesProvider(api_key="secret", transport=fake)
        response = provider.generate(
            ProviderRequest(
                prompt="question",
                system="system rule",
                model="gpt-test",
                max_output_tokens=77,
            )
        )
        call = fake.calls[0]
        self.assertEqual(call["url"], "https://api.openai.com/v1/responses")
        self.assertEqual(call["payload"]["input"], "question")
        self.assertEqual(call["payload"]["instructions"], "system rule")
        self.assertEqual(call["payload"]["max_output_tokens"], 77)
        self.assertEqual(call["headers"]["Authorization"], "Bearer secret")
        self.assertEqual(response.text, "openai result")
        self.assertEqual(response.usage.total_tokens, 10)

    def test_anthropic_adapter_request_and_response_without_network(self) -> None:
        fake = FakeTransport(
            {
                "anthropic": {
                    "id": "msg_1",
                    "model": "claude-test",
                    "content": [{"type": "text", "text": "claude result"}],
                    "usage": {"input_tokens": 5, "output_tokens": 4},
                }
            }
        )
        provider = AnthropicMessagesProvider(api_key="secret", transport=fake)
        response = provider.generate(
            ProviderRequest(prompt="question", system="system rule", model="claude-test")
        )
        call = fake.calls[0]
        self.assertEqual(call["url"], "https://api.anthropic.com/v1/messages")
        self.assertEqual(call["payload"]["messages"][0]["content"], "question")
        self.assertEqual(call["payload"]["system"], "system rule")
        self.assertEqual(call["headers"]["x-api-key"], "secret")
        self.assertEqual(call["headers"]["anthropic-version"], "2023-06-01")
        self.assertEqual(response.text, "claude result")
        self.assertEqual(response.usage.total_tokens, 9)

    def test_ollama_adapter_request_and_response_without_live_server(self) -> None:
        fake = FakeTransport(
            {
                "ollama": {
                    "model": "local-test",
                    "created_at": "test-time",
                    "message": {"role": "assistant", "content": "local result"},
                    "done": True,
                    "prompt_eval_count": 6,
                    "eval_count": 2,
                }
            }
        )
        provider = OllamaChatProvider(default_model="local-test", transport=fake)
        response = provider.generate(
            ProviderRequest(prompt="question", system="system rule", max_output_tokens=42)
        )
        call = fake.calls[0]
        self.assertEqual(call["url"], "http://localhost:11434/api/chat")
        self.assertFalse(call["payload"]["stream"])
        self.assertEqual(call["payload"]["messages"][0]["role"], "system")
        self.assertEqual(call["payload"]["messages"][1]["content"], "question")
        self.assertEqual(call["payload"]["options"]["num_predict"], 42)
        self.assertEqual(response.text, "local result")
        self.assertEqual(response.usage.total_tokens, 8)

    def test_cli_list_and_mock_round_trip_without_network(self) -> None:
        env = os.environ.copy()
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_MODEL", "ANTHROPIC_MODEL", "OLLAMA_MODEL"):
            env.pop(key, None)
        run_py = ROOT / "run.py"
        listed = subprocess.run(
            [sys.executable, str(run_py), "provider", "list"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        providers = {item["name"]: item for item in json.loads(listed.stdout)["providers"]}
        self.assertEqual(set(providers), {"anthropic", "mock", "ollama", "openai"})
        self.assertFalse(providers["openai"]["configured"])
        self.assertFalse(providers["anthropic"]["configured"])

        generated = subprocess.run(
            [sys.executable, str(run_py), "provider", "run", "mock", "hello cli"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        result = json.loads(generated.stdout)
        self.assertEqual(result["text"], "MOCK_RESPONSE: hello cli")
        self.assertFalse(result["metadata"]["network_used"])

    def test_cli_requires_explicit_network_authorization_before_key_use(self) -> None:
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = "DO-NOT-LEAK-THIS-KEY"
        env["OPENAI_MODEL"] = "gpt-test"
        run_py = ROOT / "run.py"
        denied = subprocess.run(
            [sys.executable, str(run_py), "provider", "run", "openai", "must not send"],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(denied.returncode, 0)
        combined = denied.stdout + denied.stderr
        self.assertIn("--allow-network", combined)
        self.assertNotIn("DO-NOT-LEAK-THIS-KEY", combined)


if __name__ == "__main__":
    unittest.main()
