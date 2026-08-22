from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_TRANSFERS = {
    "PRESERVE_SOURCE_CLASS_AND_UNKNOWN",
    "PIN_PROTOCOL_RULESET_AND_SURFACE_DRIFT",
    "PIN_SOURCE_BASELINE_WITHOUT_REPLACING_LEGAL_REVIEW",
    "CHECK_EXISTING_DPP_ERP_PIM_NATIVE_CAPABILITY_BEFORE_BUILD",
}

BOUNDARY_VIOLATIONS = {
    "UNKNOWN_TO_COMPLIANCE_PASS",
    "QA_PASS_TO_LEGAL_CERTIFICATION",
    "PREFLIGHT_READY_TO_REGISTRY_ACCEPTANCE",
    "ASSUME_PLATFORM_DEFAULT_ERASES_STATUTORY_OBLIGATION",
    "REPLY_TO_WTP",
    "PAYMENT_TO_REPEATABILITY",
}


def transfer_disposition(case: dict[str, Any]) -> str:
    proposal = case["proposed_transfer"]
    if proposal in ALLOWED_TRANSFERS:
        return "ACCEPT_LOCAL_TRANSFER"
    if proposal in BOUNDARY_VIOLATIONS:
        return "REJECT_BOUNDARY_VIOLATION"
    return "HOLD_UNKNOWN_TRANSFER"


def monotonic_progress_guard(executed: int, remaining: int, milestone: int, total: int = 64) -> bool:
    return 0 <= milestone <= executed <= total and remaining == total - executed


def frozen_exact_counter_guard(executed: int, remaining: int, milestone: int, total: int = 64) -> bool:
    return executed == milestone and remaining == total - milestone


def validate_fixture(path: str | Path) -> dict[str, int]:
    data = json.loads(Path(path).read_text())
    transfer_pass = 0
    for case in data["cases"]:
        actual = transfer_disposition(case)
        if actual != case["expected"]:
            raise AssertionError(f"{case['id']}: expected {case['expected']} got {actual}")
        transfer_pass += 1

    guard_pass = 0
    for case in data["progress_guard_canaries"]:
        monotonic = monotonic_progress_guard(case["executed"], case["remaining"], case["milestone"])
        frozen = frozen_exact_counter_guard(case["executed"], case["remaining"], case["milestone"])
        if monotonic is not case["monotonic_expected"]:
            raise AssertionError(f"{case['id']}: monotonic mismatch")
        if frozen is not case["frozen_exact_counter_expected"]:
            raise AssertionError(f"{case['id']}: frozen counter mismatch")
        guard_pass += 1

    return {"transfer_canaries": transfer_pass, "progress_guard_canaries": guard_pass}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = validate_fixture(root / "41_P57_P64_TRANSFER_BOUNDARY_CANARIES.json")
    print(json.dumps({"status": "PASS", **result}, sort_keys=True))
