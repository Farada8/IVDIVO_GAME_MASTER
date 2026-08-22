from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from providers import (
    AIProvider,
    ProviderDescriptor,
    ProviderRegistry,
    ProviderRequest,
    ProviderResponse,
    ProviderUsage,
)
from review import MultiModelReviewService, ReviewInputError, ReviewIntegrityError


class CapturingProvider(AIProvider):
    def __init__(self, name: str, text: str, *, network_required: bool = False) -> None:
        self.name = name
        self.text = text
        self.network_required = network_required
        self.requests: list[ProviderRequest] = []

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=True,
            network_required=self.network_required,
            endpoint="https://provider.test" if self.network_required else None,
            default_model=f"{self.name}-v1",
            contract="test_capture_provider",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        self.requests.append(request)
        return ProviderResponse(
            provider=self.name,
            model=request.model or f"{self.name}-v1",
            text=self.text,
            request_id=f"req-{self.name}-{len(self.requests)}",
            usage=ProviderUsage(),
            metadata={"network_used": self.network_required},
        )


class MultiModelReviewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        ProjectStateManager(self.home).create_project("demo", "Demo")
        self.p1 = CapturingProvider("criticone", "OUTPUT_A")
        self.p2 = CapturingProvider("critictwo", "OUTPUT_B")
        registry = ProviderRegistry()
        registry.register(self.p1)
        registry.register(self.p2)
        self.service = MultiModelReviewService(self.home, registry=registry)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def request(provider1: str = "criticone", provider2: str = "critictwo") -> dict:
        return {
            "content": "FROZEN TARGET CONTENT — alpha beta gamma",
            "critics": [
                {
                    "id": "logic",
                    "provider": provider1,
                    "model": "model-logic",
                    "instruction": "Find logical contradictions.",
                    "required": True,
                },
                {
                    "id": "evidence",
                    "provider": provider2,
                    "model": "model-evidence",
                    "instruction": "Audit evidence quality.",
                    "required": True,
                },
            ],
        }

    def test_critics_are_isolated_until_aggregation(self) -> None:
        started = self.service.start("demo", self.request())
        review_id = started["manifest"]["review_id"]
        root = Path(started["root"])
        frozen_hash = started["manifest"]["frozen_input_sha256"]
        self.assertFalse((root / "aggregate.json").exists())

        first = self.service.run_critic("demo", review_id, "logic")
        self.assertEqual(first["status"], "COMPLETE")
        self.assertFalse((root / "aggregate.json").exists())
        with self.assertRaisesRegex(RuntimeError, "aggregation blocked"):
            self.service.aggregate("demo", review_id)

        second = self.service.run_critic("demo", review_id, "evidence")
        self.assertEqual(second["status"], "COMPLETE")
        self.assertEqual(len(self.p1.requests), 1)
        self.assertEqual(len(self.p2.requests), 1)
        prompt1 = self.p1.requests[0].prompt
        prompt2 = self.p2.requests[0].prompt
        self.assertIn("FROZEN TARGET CONTENT", prompt1)
        self.assertIn("FROZEN TARGET CONTENT", prompt2)
        self.assertIn(frozen_hash, prompt1)
        self.assertIn(frozen_hash, prompt2)
        self.assertNotIn("OUTPUT_B", prompt1)
        self.assertNotIn("OUTPUT_A", prompt2)
        self.assertIn("You have not been given any other critic output", prompt1)
        self.assertIn("You have not been given any other critic output", prompt2)

        aggregate = self.service.aggregate("demo", review_id)
        self.assertEqual(aggregate["status"], "COMPLETE")
        self.assertEqual(aggregate["agreement"], "DISAGREEMENT")
        self.assertFalse(aggregate["consensus_claimed"])
        self.assertFalse(aggregate["truth_claimed"])
        self.assertEqual(
            {item["response"] for item in aggregate["critic_results"]},
            {"OUTPUT_A", "OUTPUT_B"},
        )
        self.assertTrue((root / "aggregate.json").is_file())

    def test_critic_result_is_immutable_and_idempotent(self) -> None:
        started = self.service.start("demo", self.request())
        review_id = started["manifest"]["review_id"]
        first = self.service.run_critic("demo", review_id, "logic")
        second = self.service.run_critic("demo", review_id, "logic")
        self.assertEqual(first, second)
        self.assertEqual(len(self.p1.requests), 1)

    def test_exact_match_is_not_promoted_to_truth(self) -> None:
        same1 = CapturingProvider("sameone", "SAME")
        same2 = CapturingProvider("sametwo", "SAME")
        registry = ProviderRegistry()
        registry.register(same1)
        registry.register(same2)
        service = MultiModelReviewService(self.home, registry=registry)
        aggregate = service.run_all("demo", self.request("sameone", "sametwo"))
        self.assertEqual(aggregate["agreement"], "EXACT_MATCH")
        self.assertEqual(aggregate["status"], "COMPLETE")
        self.assertFalse(aggregate["consensus_claimed"])
        self.assertFalse(aggregate["truth_claimed"])

    def test_network_critic_without_authorization_becomes_explicit_hold(self) -> None:
        local = CapturingProvider("local", "LOCAL")
        remote = CapturingProvider("remote", "REMOTE", network_required=True)
        registry = ProviderRegistry()
        registry.register(local)
        registry.register(remote)
        service = MultiModelReviewService(self.home, registry=registry)
        request = self.request("local", "remote")
        started = service.start("demo", request)
        review_id = started["manifest"]["review_id"]
        service.run_critic("demo", review_id, "logic")
        held = service.run_critic("demo", review_id, "evidence", allow_network=False)
        self.assertEqual(held["status"], "HOLD")
        self.assertEqual(held["failure_class"], "NETWORK_NOT_AUTHORIZED")
        self.assertEqual(remote.requests, [])
        aggregate = service.aggregate("demo", review_id)
        self.assertEqual(aggregate["status"], "HOLD")
        self.assertEqual(aggregate["required_failures"], ["evidence"])
        self.assertEqual(aggregate["agreement"], "INSUFFICIENT_COMPLETED_CRITICS")

    def test_unknown_provider_is_terminal_failure_not_missing_critic(self) -> None:
        started = self.service.start("demo", self.request("criticone", "missing-provider"))
        review_id = started["manifest"]["review_id"]
        self.service.run_critic("demo", review_id, "logic")
        failed = self.service.run_critic("demo", review_id, "evidence")
        self.assertEqual(failed["status"], "FAILED")
        self.assertEqual(failed["failure_class"], "UNKNOWN_PROVIDER")
        aggregate = self.service.aggregate("demo", review_id)
        self.assertEqual(aggregate["status"], "HOLD")
        self.assertEqual(aggregate["required_failures"], ["evidence"])

    def test_tampered_critic_payload_blocks_aggregation(self) -> None:
        started = self.service.start("demo", self.request())
        review_id = started["manifest"]["review_id"]
        self.service.run_critic("demo", review_id, "logic")
        self.service.run_critic("demo", review_id, "evidence")
        path = Path(started["root"]) / "critics" / "logic.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["response"] = "TAMPERED"
        path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ReviewIntegrityError, "payload hash mismatch"):
            self.service.aggregate("demo", review_id)

    def test_tampered_frozen_input_blocks_next_critic(self) -> None:
        started = self.service.start("demo", self.request())
        review_id = started["manifest"]["review_id"]
        path = Path(started["root"]) / "frozen_input.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["content"] = "CHANGED"
        path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(ReviewIntegrityError):
            self.service.run_critic("demo", review_id, "logic")

    def test_aggregate_persists_output_memory(self) -> None:
        aggregate = self.service.run_all("demo", self.request())
        memory = MemoryStore(self.home / "runtime" / "state.db").get(aggregate["output_memory_id"])
        self.assertEqual(memory["kind"], "OUTPUT")
        self.assertEqual(memory["project_id"], "demo")
        self.assertEqual(memory["metadata"]["review_id"], aggregate["review_id"])
        self.assertEqual(memory["metadata"]["agreement"], "DISAGREEMENT")

    def test_request_validation_fails_closed(self) -> None:
        with self.assertRaises(ReviewInputError):
            self.service.start("demo", {"content": "x", "critics": []})
        request = self.request()
        request["critics"][1]["id"] = "logic"
        with self.assertRaisesRegex(ReviewInputError, "duplicate critic id"):
            self.service.start("demo", request)
        request = self.request()
        request["critics"][0]["temperature"] = 3
        with self.assertRaises(ReviewInputError):
            self.service.start("demo", request)


if __name__ == "__main__":
    unittest.main()
