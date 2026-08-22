from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class SiteObservation:
    site_id: str
    ordinary_control_usable: bool
    material_incremental_ai_defect: bool
    reproduced: bool
    actionable: bool


def classify(obs: SiteObservation) -> Mapping[str, object]:
    counts = all((
        obs.ordinary_control_usable,
        obs.material_incremental_ai_defect,
        obs.reproduced,
        obs.actionable,
    ))
    return {
        "site_id": obs.site_id,
        "counts": counts,
        "ordinary_control_usable": obs.ordinary_control_usable,
        "incremental_ai_defect": obs.material_incremental_ai_defect,
        "proof_promotion": False,
    }


def evaluate(observations: Iterable[SiteObservation]) -> Mapping[str, object]:
    observations = tuple(observations)
    if len(observations) != 3:
        return {"status": "HOLD_EXACTLY_THREE_SITES_REQUIRED", "pass": False, "proof_promotion": False}
    if len({x.site_id for x in observations}) != 3:
        return {"status": "HOLD_DUPLICATE_SITE", "pass": False, "proof_promotion": False}

    rows = tuple(classify(x) for x in observations)
    count = sum(bool(r["counts"]) for r in rows)

    if count >= 2:
        status = "PASS_INTERNAL_DIFFERENTIAL_2_OF_3_OR_BETTER"
    elif count == 1:
        status = "AMBIGUOUS_INTERNAL_DIFFERENTIAL_1_OF_3"
    else:
        status = "FAIL_INTERNAL_DIFFERENTIAL_0_OF_3"

    return {
        "status": status,
        "pass": count >= 2,
        "count": count,
        "sample": 3,
        "buyer_behavior": False,
        "willingness_to_pay": None,
        "transaction": None,
        "proof_promotion": False,
        "next64_increment": 0,
    }


CURRENT_OBSERVATIONS = (
    SiteObservation("PALLAS", True, True, True, True),
    SiteObservation("CLISSMANN", True, True, True, True),
    SiteObservation("TOWNSEND", True, False, False, False),
)


def current_result() -> Mapping[str, object]:
    return evaluate(CURRENT_OBSERVATIONS)
