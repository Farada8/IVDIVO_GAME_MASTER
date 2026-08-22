from __future__ import annotations
import importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[3]
C10 = ROOT / "SELF_IMPROVEMENT_STUDIO/2026-08-22_CYCLE10_DECISION_EVIDENCE_YIELD_32_TO_64/runtime/cycle10_governance.py"
DATA = HERE.parents[1] / "01_PROSPECTIVE_PILOTS.json"


def load_governance():
    spec = importlib.util.spec_from_file_location("cycle10_governance", C10)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def meaningful_delta(delta: dict) -> bool:
    keys = ("gate_changed", "selected_test_changed", "artifact_changed", "next_action_changed", "decision_changed")
    return any(bool(delta.get(k)) for k in keys)


def stop_after_two_no_delta(deltas) -> bool:
    streak = 0
    for delta in deltas:
        streak = 0 if meaningful_delta(delta) else streak + 1
        if streak >= 2:
            return True
    return False


def evaluate():
    governance = load_governance()
    data = json.loads(DATA.read_text())
    results = []
    for pilot in data["pilots"]:
        dy = governance.decision_yield(
            pilot["test_disposition"],
            pilot["uncertainty"],
            pilot["smallest_decisive_test"],
            pilot["production_return"],
        )
        tests = [
            {
                "id": "SMALLEST",
                "decision_consumer": pilot["production_return"],
                "decision_flip": int(pilot["delta"]["decision_changed"] or pilot["delta"]["next_action_changed"]),
                "evidence_independence": 1,
                "burden": 1,
                "risk": 1,
            },
            {
                "id": "BROAD_NOT_EXECUTED",
                "decision_consumer": pilot["production_return"],
                "decision_flip": 0,
                "evidence_independence": 0,
                "burden": 3,
                "risk": 2,
            },
        ]
        voi = governance.ordinal_voi_route(tests)
        results.append({
            "id": pilot["id"],
            "decision_yield": dy["status"],
            "voi_route": voi,
            "meaningful_delta": meaningful_delta(pilot["delta"]),
            "external_evidence_claimed": pilot["external_evidence_claimed"],
        })
    passed = all(
        r["decision_yield"] == "PASS_BOUNDED_META_ACTION"
        and r["voi_route"]["selected"] == "SMALLEST"
        and r["meaningful_delta"]
        and not r["external_evidence_claimed"]
        for r in results
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "results": results,
        "b15_triggered_on_real_three": stop_after_two_no_delta([p["delta"] for p in data["pilots"]]),
        "b16": data["b16_disposition"],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
