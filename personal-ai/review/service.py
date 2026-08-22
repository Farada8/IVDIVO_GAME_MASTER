from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from providers import ProviderError, ProviderRequest, ProviderUnavailableError, default_registry
from providers.registry import ProviderRegistry

_TERMINAL_STATUSES = {"COMPLETE", "HOLD", "FAILED"}
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ReviewInputError(ValueError):
    pass


class ReviewIntegrityError(RuntimeError):
    pass


def _clean_text(value: Any, field: str) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        raise ReviewInputError(f"{field} cannot be empty")
    return text


def _safe_id(value: Any, field: str) -> str:
    text = _clean_text(value, field)
    if not _SAFE_ID.fullmatch(text):
        raise ReviewInputError(
            f"{field} must be 1-128 safe characters: letters, digits, dot, underscore or dash"
        )
    return text


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha_json(value: Any) -> str:
    return _sha_text(_canonical_json(value))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReviewIntegrityError(f"JSON object required: {path.name}")
    return value


def _payload_hash(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("payload_sha256", None)
    return _sha_json(payload)


class MultiModelReviewService:
    """PL-10 independent critic orchestration with aggregation only after terminal isolation."""

    def __init__(self, home: Path, *, registry: ProviderRegistry | None = None) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.registry = registry or default_registry()

    def start(self, project_id: str, request: dict[str, Any]) -> dict[str, Any]:
        project = self.projects.load_project(_clean_text(project_id, "project_id"))
        normalized = self._normalize_request(request)
        review_id = f"review-{uuid.uuid4().hex}"
        root = Path(project["root"]) / "artifacts" / "reviews" / review_id
        root.mkdir(parents=True, exist_ok=False)

        frozen = {
            "schema": "ivdivo.personal_ai.review_frozen_input/0.1",
            "review_id": review_id,
            "project_id": project_id,
            "content": normalized["content"],
        }
        frozen["content_sha256"] = _sha_text(frozen["content"])
        frozen["payload_sha256"] = _payload_hash(frozen)
        _write_json(root / "frozen_input.json", frozen)

        manifest = {
            "schema": "ivdivo.personal_ai.multi_model_review/0.1",
            "review_id": review_id,
            "project_id": project_id,
            "status": "RUNNING",
            "frozen_input_sha256": frozen["content_sha256"],
            "critics": normalized["critics"],
            "critic_count": len(normalized["critics"]),
            "aggregate_path": None,
            "evidence_boundary": (
                "Critic isolation and orchestration are proven independently of model quality. "
                "Agreement does not prove truth; live provider quality/network success is not inferred from offline tests."
            ),
        }
        manifest["payload_sha256"] = _payload_hash(manifest)
        _write_json(root / "manifest.json", manifest)
        return self.load(project_id, review_id)

    def run_critic(
        self,
        project_id: str,
        review_id: str,
        critic_id: str,
        *,
        allow_network: bool = False,
    ) -> dict[str, Any]:
        root, manifest, frozen = self._load_verified(project_id, review_id)
        critic_id = _safe_id(critic_id, "critic_id")
        critic = next((item for item in manifest["critics"] if item["id"] == critic_id), None)
        if critic is None:
            raise ReviewInputError(f"unknown critic_id: {critic_id}")

        output_path = root / "critics" / f"{critic_id}.json"
        if output_path.exists():
            return self._read_verified_critic(output_path, manifest, frozen)

        provider = self.registry.get(critic["provider"])
        descriptor = provider.describe()
        base = {
            "schema": "ivdivo.personal_ai.critic_result/0.1",
            "review_id": review_id,
            "project_id": project_id,
            "critic_id": critic_id,
            "provider": critic["provider"],
            "requested_model": critic.get("model"),
            "required": critic["required"],
            "frozen_input_sha256": manifest["frozen_input_sha256"],
            "instruction_sha256": _sha_text(critic["instruction"]),
            "network_authorized": bool(allow_network),
            "network_required": bool(descriptor.network_required),
            "response": None,
            "response_sha256": None,
            "provider_model": None,
            "provider_request_id": None,
            "provider_metadata": None,
            "failure_class": None,
        }

        if descriptor.network_required and not allow_network:
            result = {
                **base,
                "status": "HOLD",
                "failure_class": "NETWORK_NOT_AUTHORIZED",
            }
        else:
            prompt = self._critic_prompt(critic, frozen)
            request = ProviderRequest(
                prompt=prompt,
                model=critic.get("model"),
                max_output_tokens=critic["max_output_tokens"],
                temperature=critic.get("temperature"),
                metadata={
                    "review_id": review_id,
                    "critic_id": critic_id,
                    "frozen_input_sha256": manifest["frozen_input_sha256"],
                },
            )
            try:
                response = provider.generate(request)
                text = response.text.strip()
                if not text:
                    result = {
                        **base,
                        "status": "FAILED",
                        "failure_class": "EMPTY_PROVIDER_RESPONSE",
                    }
                else:
                    result = {
                        **base,
                        "status": "COMPLETE",
                        "response": text,
                        "response_sha256": _sha_text(text),
                        "provider_model": response.model,
                        "provider_request_id": response.request_id,
                        "provider_metadata": response.metadata,
                    }
            except (ProviderUnavailableError, ProviderError, KeyError):
                result = {
                    **base,
                    "status": "FAILED",
                    "failure_class": "PROVIDER_CALL_FAILED",
                }

        result["payload_sha256"] = _payload_hash(result)
        _write_json(output_path, result)
        return result

    def aggregate(self, project_id: str, review_id: str) -> dict[str, Any]:
        root, manifest, frozen = self._load_verified(project_id, review_id)
        aggregate_path = root / "aggregate.json"
        if aggregate_path.exists():
            aggregate = _read_json(aggregate_path)
            self._verify_payload(aggregate, "aggregate.json")
            return aggregate

        results: list[dict[str, Any]] = []
        missing: list[str] = []
        for critic in manifest["critics"]:
            path = root / "critics" / f"{critic['id']}.json"
            if not path.exists():
                missing.append(critic["id"])
                continue
            results.append(self._read_verified_critic(path, manifest, frozen))
        if missing:
            raise RuntimeError(
                "aggregation blocked until all critics are terminal: " + ", ".join(missing)
            )
        nonterminal = [item["critic_id"] for item in results if item["status"] not in _TERMINAL_STATUSES]
        if nonterminal:
            raise ReviewIntegrityError(f"non-terminal critic result: {nonterminal}")

        required_failures = [
            item["critic_id"]
            for item in results
            if item["required"] and item["status"] != "COMPLETE"
        ]
        completed = [item for item in results if item["status"] == "COMPLETE"]
        response_hashes = [item["response_sha256"] for item in completed]
        if len(completed) < 2:
            agreement = "INSUFFICIENT_COMPLETED_CRITICS"
        elif len(set(response_hashes)) == 1:
            agreement = "EXACT_MATCH"
        else:
            agreement = "DISAGREEMENT"

        aggregate = {
            "schema": "ivdivo.personal_ai.review_aggregate/0.1",
            "review_id": review_id,
            "project_id": project_id,
            "status": "HOLD" if required_failures else "COMPLETE",
            "frozen_input_sha256": manifest["frozen_input_sha256"],
            "critic_count": len(results),
            "completed_count": len(completed),
            "required_failures": required_failures,
            "agreement": agreement,
            "consensus_claimed": False,
            "truth_claimed": False,
            "critic_results": [
                {
                    "critic_id": item["critic_id"],
                    "provider": item["provider"],
                    "provider_model": item["provider_model"],
                    "status": item["status"],
                    "response": item["response"],
                    "response_sha256": item["response_sha256"],
                    "failure_class": item["failure_class"],
                }
                for item in results
            ],
            "evidence_boundary": (
                "Aggregation preserves every critic result and disagreement. Exact text agreement is not truth proof."
            ),
        }
        aggregate["payload_sha256"] = _payload_hash(aggregate)

        output_memory = self.memory.store(
            _canonical_json(
                {
                    "review_id": review_id,
                    "status": aggregate["status"],
                    "agreement": agreement,
                    "frozen_input_sha256": manifest["frozen_input_sha256"],
                    "critic_count": len(results),
                    "required_failures": required_failures,
                }
            ),
            kind="OUTPUT",
            source="PL-10 Multi-Model Review",
            metadata={
                "review_id": review_id,
                "status": aggregate["status"],
                "agreement": agreement,
                "frozen_input_sha256": manifest["frozen_input_sha256"],
            },
            project_id=project_id,
        )
        aggregate["output_memory_id"] = output_memory["id"]
        aggregate["payload_sha256"] = _payload_hash(aggregate)
        _write_json(aggregate_path, aggregate)

        updated_manifest = dict(manifest)
        updated_manifest["status"] = aggregate["status"]
        updated_manifest["aggregate_path"] = str(aggregate_path)
        updated_manifest["payload_sha256"] = _payload_hash(updated_manifest)
        _write_json(root / "manifest.json", updated_manifest)
        return aggregate

    def run_all(
        self,
        project_id: str,
        request: dict[str, Any],
        *,
        allow_network: bool = False,
    ) -> dict[str, Any]:
        started = self.start(project_id, request)
        review_id = started["manifest"]["review_id"]
        for critic in started["manifest"]["critics"]:
            self.run_critic(
                project_id,
                review_id,
                critic["id"],
                allow_network=allow_network,
            )
        return self.aggregate(project_id, review_id)

    def load(self, project_id: str, review_id: str) -> dict[str, Any]:
        root, manifest, frozen = self._load_verified(project_id, review_id)
        critics: dict[str, Any] = {}
        for critic in manifest["critics"]:
            path = root / "critics" / f"{critic['id']}.json"
            if path.exists():
                critics[critic["id"]] = self._read_verified_critic(path, manifest, frozen)
        aggregate = None
        aggregate_path = root / "aggregate.json"
        if aggregate_path.exists():
            aggregate = _read_json(aggregate_path)
            self._verify_payload(aggregate, "aggregate.json")
        return {
            "root": str(root),
            "manifest": manifest,
            "frozen_input": frozen,
            "critics": critics,
            "aggregate": aggregate,
        }

    def _load_verified(
        self, project_id: str, review_id: str
    ) -> tuple[Path, dict[str, Any], dict[str, Any]]:
        project = self.projects.load_project(_clean_text(project_id, "project_id"))
        review_id = _safe_id(review_id, "review_id")
        if not review_id.startswith("review-"):
            raise ReviewInputError("review_id must start with review-")
        root = Path(project["root"]) / "artifacts" / "reviews" / review_id
        if not root.is_dir():
            raise FileNotFoundError(f"review not found: {review_id}")
        manifest = _read_json(root / "manifest.json")
        frozen = _read_json(root / "frozen_input.json")
        self._verify_payload(manifest, "manifest.json")
        self._verify_payload(frozen, "frozen_input.json")
        if manifest.get("review_id") != review_id or frozen.get("review_id") != review_id:
            raise ReviewIntegrityError("review id mismatch")
        if manifest.get("project_id") != project_id or frozen.get("project_id") != project_id:
            raise ReviewIntegrityError("project id mismatch")
        if _sha_text(str(frozen.get("content", ""))) != frozen.get("content_sha256"):
            raise ReviewIntegrityError("frozen review input hash mismatch")
        if manifest.get("frozen_input_sha256") != frozen.get("content_sha256"):
            raise ReviewIntegrityError("manifest/frozen input hash mismatch")
        return root, manifest, frozen

    def _read_verified_critic(
        self,
        path: Path,
        manifest: dict[str, Any],
        frozen: dict[str, Any],
    ) -> dict[str, Any]:
        result = _read_json(path)
        self._verify_payload(result, path.name)
        if result.get("review_id") != manifest.get("review_id"):
            raise ReviewIntegrityError(f"critic review id mismatch: {path.name}")
        if result.get("project_id") != manifest.get("project_id"):
            raise ReviewIntegrityError(f"critic project id mismatch: {path.name}")
        if result.get("frozen_input_sha256") != frozen.get("content_sha256"):
            raise ReviewIntegrityError(f"critic frozen input mismatch: {path.name}")
        if result.get("status") == "COMPLETE":
            response = result.get("response")
            if not isinstance(response, str) or not response.strip():
                raise ReviewIntegrityError(f"complete critic has no response: {path.name}")
            if _sha_text(response) != result.get("response_sha256"):
                raise ReviewIntegrityError(f"critic response hash mismatch: {path.name}")
        return result

    @staticmethod
    def _verify_payload(value: dict[str, Any], label: str) -> None:
        expected = value.get("payload_sha256")
        if not isinstance(expected, str) or expected != _payload_hash(value):
            raise ReviewIntegrityError(f"payload hash mismatch: {label}")

    @staticmethod
    def _critic_prompt(critic: dict[str, Any], frozen: dict[str, Any]) -> str:
        return (
            "INDEPENDENT_CRITIC_REVIEW\n"
            f"CRITIC_ID: {critic['id']}\n"
            f"INSTRUCTION: {critic['instruction']}\n"
            f"FROZEN_REVIEW_INPUT_SHA256: {frozen['content_sha256']}\n"
            "RULES:\n"
            "- Review only the frozen input below.\n"
            "- You have not been given any other critic output.\n"
            "- Do not claim consensus with other critics.\n"
            "FROZEN_REVIEW_INPUT:\n"
            f"{frozen['content']}"
        )

    @staticmethod
    def _normalize_request(request: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(request, dict):
            raise ReviewInputError("review request must be a JSON object")
        content = _clean_text(request.get("content"), "content")
        raw_critics = request.get("critics")
        if not isinstance(raw_critics, list) or not 2 <= len(raw_critics) <= 20:
            raise ReviewInputError("critics must contain between 2 and 20 critic definitions")
        critics: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, raw in enumerate(raw_critics):
            if not isinstance(raw, dict):
                raise ReviewInputError(f"critics[{index}] must be an object")
            critic_id = _safe_id(raw.get("id"), f"critics[{index}].id")
            if critic_id in seen:
                raise ReviewInputError(f"duplicate critic id: {critic_id}")
            seen.add(critic_id)
            provider = _safe_id(raw.get("provider"), f"critics[{index}].provider").lower()
            model = raw.get("model")
            if model is not None:
                model = _clean_text(model, f"critics[{index}].model")
            instruction = _clean_text(raw.get("instruction"), f"critics[{index}].instruction")
            required = raw.get("required", True)
            if not isinstance(required, bool):
                raise ReviewInputError(f"critics[{index}].required must be boolean")
            max_output_tokens = raw.get("max_output_tokens", 512)
            if isinstance(max_output_tokens, bool) or not isinstance(max_output_tokens, int) or max_output_tokens < 1:
                raise ReviewInputError(f"critics[{index}].max_output_tokens must be positive integer")
            temperature = raw.get("temperature")
            if temperature is not None:
                if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
                    raise ReviewInputError(f"critics[{index}].temperature must be numeric or null")
                temperature = float(temperature)
                if not 0 <= temperature <= 2:
                    raise ReviewInputError(f"critics[{index}].temperature must be between 0 and 2")
            critics.append(
                {
                    "id": critic_id,
                    "provider": provider,
                    "model": model,
                    "instruction": instruction,
                    "required": required,
                    "max_output_tokens": max_output_tokens,
                    "temperature": temperature,
                }
            )
        return {"content": content, "critics": critics}
