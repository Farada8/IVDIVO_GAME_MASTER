from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from projects.manager import ProjectStateManager
from providers import AIProvider, ProviderDescriptor, ProviderRegistry, ProviderRequest, ProviderResponse
from review import MultiModelReviewService, ReviewIntegrityError
from review.service import _payload_hash


class FixedProvider(AIProvider):
    def __init__(self, name: str, text: str) -> None:
        self.name = name
        self.text = text

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=True,
            network_required=False,
            endpoint=None,
            default_model=f"{self.name}-v1",
            contract="fixed-test-provider",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(provider=self.name, model=request.model or f"{self.name}-v1", text=self.text)


class CriticSpecIntegrityTest(unittest.TestCase):
    def test_self_rehashed_role_substitution_still_fails_against_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ProjectStateManager(home).create_project("demo", "Demo")
            registry = ProviderRegistry()
            registry.register(FixedProvider("one", "ONE"))
            registry.register(FixedProvider("two", "TWO"))
            service = MultiModelReviewService(home, registry=registry)
            request = {
                "content": "Frozen content",
                "critics": [
                    {"id": "logic", "provider": "one", "model": "m1", "instruction": "Logic audit"},
                    {"id": "evidence", "provider": "two", "model": "m2", "instruction": "Evidence audit"},
                ],
            }
            started = service.start("demo", request)
            review_id = started["manifest"]["review_id"]
            service.run_critic("demo", review_id, "logic")
            service.run_critic("demo", review_id, "evidence")

            path = Path(started["root"]) / "critics" / "logic.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["provider"] = "two"
            payload["payload_sha256"] = _payload_hash(payload)
            path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")

            with self.assertRaisesRegex(ReviewIntegrityError, "frozen spec"):
                service.aggregate("demo", review_id)


if __name__ == "__main__":
    unittest.main()
