from __future__ import annotations

from typing import Any

from .service import BusinessResearchService as _BaseBusinessResearchService
from .service import ResearchInputError


class BusinessResearchService(_BaseBusinessResearchService):
    """Fail-closed PL-07 public service.

    The base packet builder provides deterministic persistence/provenance. This
    wrapper adds the evidence-ceiling rules found by independent Red Team:

    * evidence dated after the research ``as_of`` may be recorded in the packet
      but may not support a claim or calculation;
    * a conclusion may not claim a stronger epistemic status than its support.

    The wrapper deliberately does not create VERIFIED_FACT records. PL-03 owns
    explicit verification and remains the only route to that evidence class.
    """

    @staticmethod
    def _reject_future_sources(
        source_keys: list[Any],
        source_lookup: dict[str, dict[str, Any]],
        context: str,
    ) -> None:
        for raw_key in source_keys:
            key = str(raw_key).strip()
            row = source_lookup.get(key)
            if row is None:
                # Let the base implementation emit the canonical unknown-key error.
                continue
            if row.get("freshness_status") == "FUTURE":
                raise ResearchInputError(
                    f"{context} cannot use future-dated source {key!r} for the research as_of date"
                )

    def _run_calculations(
        self,
        project_id: str,
        request: dict[str, Any],
        source_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        for index, item in enumerate(request.get("calculations", [])):
            if isinstance(item, dict):
                source_keys = item.get("source_keys", [])
                if isinstance(source_keys, list):
                    self._reject_future_sources(
                        source_keys, source_lookup, f"calculations[{index}]"
                    )
        return super()._run_calculations(project_id, request, source_lookup)

    def _persist_claims(
        self,
        project_id: str,
        request: dict[str, Any],
        source_lookup: dict[str, dict[str, Any]],
        calculation_lookup: dict[str, dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
        for index, item in enumerate(request.get("claims", [])):
            if isinstance(item, dict):
                source_keys = item.get("source_keys", [])
                if isinstance(source_keys, list):
                    self._reject_future_sources(source_keys, source_lookup, f"claims[{index}]")
        return super()._persist_claims(
            project_id, request, source_lookup, calculation_lookup
        )

    def _validate_conclusions(
        self,
        request: dict[str, Any],
        claim_lookup: dict[str, dict[str, Any]],
        calculation_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        conclusions = super()._validate_conclusions(
            request, claim_lookup, calculation_lookup
        )

        for index, (raw, resolved) in enumerate(
            zip(request.get("conclusions", []), conclusions, strict=True)
        ):
            claim_statuses = [
                claim_lookup[key]["status"] for key in resolved["claim_keys"]
            ]
            calculation_statuses = [
                calculation_lookup[calc_id]["status"]
                for calc_id in resolved["calculation_ids"]
            ]
            status = resolved["status"]

            if status == "OBSERVED":
                if not claim_statuses:
                    raise ResearchInputError(
                        f"conclusions[{index}] OBSERVED requires at least one OBSERVED claim"
                    )
                if calculation_statuses or any(
                    item_status != "OBSERVED" for item_status in claim_statuses
                ):
                    raise ResearchInputError(
                        f"conclusions[{index}] OBSERVED cannot be supported by calculated, inferred, or unknown evidence"
                    )

            elif status == "CALCULATED":
                if any(
                    item_status not in {"OBSERVED", "CALCULATED"}
                    for item_status in claim_statuses
                ) or any(
                    item_status != "CALCULATED"
                    for item_status in calculation_statuses
                ):
                    raise ResearchInputError(
                        f"conclusions[{index}] CALCULATED cannot exceed inferred/unknown support"
                    )
                if not calculation_statuses and "CALCULATED" not in claim_statuses:
                    raise ResearchInputError(
                        f"conclusions[{index}] CALCULATED requires a successful calculation"
                    )

            elif status == "INFERRED":
                supporting_statuses = claim_statuses + calculation_statuses
                if not any(
                    item_status in {"OBSERVED", "CALCULATED", "INFERRED"}
                    for item_status in supporting_statuses
                ):
                    raise ResearchInputError(
                        f"conclusions[{index}] INFERRED requires at least one non-UNKNOWN support item"
                    )

            elif status == "UNKNOWN":
                # UNKNOWN is the floor: retaining stronger references does not
                # launder them upward and may explain why a decision remains open.
                pass
            else:  # pragma: no cover - base class already validates statuses.
                raise ResearchInputError(
                    f"unsupported conclusion status: {raw.get('status') if isinstance(raw, dict) else status}"
                )

        return conclusions
