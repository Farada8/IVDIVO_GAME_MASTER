from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Dict

HERE = Path(__file__).resolve().parent
ENGINE_ROOT = HERE.parent
LADDER_PATH = ENGINE_ROOT / "runtime" / "monetization_ladder.py"

spec = importlib.util.spec_from_file_location("monetization_ladder", LADDER_PATH)
ladder = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ladder)

WIP = {
    "OW-01": {
        "name": "Agentic Commerce Merchant Readiness",
        "technical_artifact": True,
        "nontrivial_delta": True,
        "buyer_role_plausible": True,
        "paid_diagnostic_transactions": 0,
        "fixture_plane": "REAL_PUBLIC_PLUS_INTERNAL_ENGINEERING",
        "portfolio_role": "PRIMARY",
    },
    "CF-01": {
        "name": "AI Act Article 50 Technical Transparency",
        "technical_artifact": True,
        "nontrivial_delta": True,
        "buyer_role_plausible": True,
        "paid_diagnostic_transactions": 0,
        "fixture_plane": "SYNTHETIC_INTERNAL_ENGINEERING",
        "portfolio_role": "PILOT_A",
    },
    "CF-03": {
        "name": "DPP Supplier-Data / Registry Readiness",
        "technical_artifact": True,
        "nontrivial_delta": True,
        "buyer_role_plausible": True,
        "paid_diagnostic_transactions": 0,
        "fixture_plane": "SYNTHETIC_INTERNAL_ENGINEERING",
        "portfolio_role": "PILOT_B",
    },
}

EXPECTED_M1 = "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN"


def route_wip() -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for opportunity_id, data in WIP.items():
        evidence = ladder.MonetizationEvidence(
            opportunity_id=opportunity_id,
            technical_artifact=data["technical_artifact"],
            nontrivial_delta=data["nontrivial_delta"],
            buyer_role_plausible=data["buyer_role_plausible"],
            paid_diagnostic_transactions=data["paid_diagnostic_transactions"],
            external_action_authorized=False,
        )
        routed = ladder.route(evidence)
        out[opportunity_id] = {
            "name": data["name"],
            "portfolio_role": data["portfolio_role"],
            "fixture_plane": data["fixture_plane"],
            "route": routed["disposition"],
            "buyer_demand_proven": False,
            "wtp": None,
            "price": None,
            "transactions": 0,
            "external_action_authorized": False,
        }
    return out


def compare() -> dict:
    routes = route_wip()
    all_m1 = all(item["route"] == EXPECTED_M1 for item in routes.values())
    return {
        "schema": "ivdivo.general_business.pew05_wip3_comparison/1.0",
        "all_three_route_m1": all_m1,
        "routes": routes,
        "portfolio_decision": {
            "PRIMARY": "OW-01",
            "PILOT_A": "CF-01",
            "PILOT_B": "CF-03",
            "wip_count": 3,
            "add_fourth_opportunity": False,
        },
        "evidence_strength_equal": False,
        "reason": "Equal M1 ladder route reflects commercialization stage, not equal empirical evidence strength.",
        "next_frontier": "P-EW06_FIXED_SCOPE_DIAGNOSTIC_DELIVERY_SPECS_CF01_CF03",
        "proof_boundary": {
            "buyer_demand_proven": False,
            "wtp": None,
            "price": None,
            "transactions": 0,
            "profitability_proven": False,
            "external_action_authorized": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(compare(), indent=2, sort_keys=True))
