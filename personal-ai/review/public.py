from __future__ import annotations

from pathlib import Path
from typing import Any

from . import service as core


class MultiModelReviewService(core.MultiModelReviewService):
    def run_critic(
        self,
        project_id: str,
        review_id: str,
        critic_id: str,
        *,
        allow_network: bool = False,
    ) -> dict[str, Any]:
        root, manifest, frozen = self._load_verified(project_id, review_id)
        critic_id = core._safe_id(critic_id, "critic_id")
        critic = next((item for item in manifest["critics"] if item["id"] == critic_id), None)
        if critic is None:
            raise core.ReviewInputError(f"unknown critic_id: {critic_id}")
        output_path = root / "critics" / f"{critic_id}.json"
        if output_path.exists():
            return self._read_verified_critic(output_path, manifest, frozen)
        try:
            self.registry.get(critic["provider"])
        except KeyError:
            result = {
                "schema": "ivdivo.personal_ai.critic_result/0.1",
                "review_id": review_id,
                "project_id": project_id,
                "critic_id": critic_id,
                "provider": critic["provider"],
                "requested_model": critic.get("model"),
                "required": critic["required"],
                "frozen_input_sha256": manifest["frozen_input_sha256"],
                "instruction_sha256": core._sha_text(critic["instruction"]),
                "network_authorized": bool(allow_network),
                "network_required": None,
                "response": None,
                "response_sha256": None,
                "provider_model": None,
                "provider_request_id": None,
                "provider_metadata": None,
                "failure_class": "UNKNOWN_PROVIDER",
                "status": "FAILED",
            }
            result["payload_sha256"] = core._payload_hash(result)
            core._write_json(output_path, result)
            return result
        return super().run_critic(project_id, review_id, critic_id, allow_network=allow_network)

    def _read_verified_critic(
        self,
        path: Path,
        manifest: dict[str, Any],
        frozen: dict[str, Any],
    ) -> dict[str, Any]:
        result = super()._read_verified_critic(path, manifest, frozen)
        expected_id = path.stem
        expected = next(
            (item for item in manifest["critics"] if item["id"] == expected_id),
            None,
        )
        if expected is None:
            raise core.ReviewIntegrityError(
                f"critic file is not declared in manifest: {path.name}"
            )
        expected_fields = {
            "critic_id": expected_id,
            "provider": expected["provider"],
            "requested_model": expected.get("model"),
            "required": expected["required"],
            "instruction_sha256": core._sha_text(expected["instruction"]),
        }
        for field, expected_value in expected_fields.items():
            if result.get(field) != expected_value:
                raise core.ReviewIntegrityError(
                    f"critic result does not match frozen spec: {path.name}:{field}"
                )
        return result
