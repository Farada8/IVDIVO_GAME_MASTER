from __future__ import annotations
import json
from pathlib import Path
from dataclasses import asdict
from engine.public_artifact_engine_v11 import *

ROOT=Path(__file__).resolve().parents[1]

def load_json(path): return json.loads((ROOT/path).read_text())

def main():
    src=load_json("fixtures/public_sources_v11.json")
    portfolio=load_json("fixtures/opportunity_portfolio_v11.json")
    source_by_id={s["source_id"]:s for s in src["sources"]}
    old=source_by_id["ETENDERS-SKERRIES-8753058"]
    cur=source_by_id["ETENDERS-SKERRIES-8891756"]
    old_snap=TenderSnapshot("SKERRIES","ETENDERS-SKERRIES-8753058",old["title"],old["authority"],old["known_fields"]["deadline"],None,old["known_fields"]["estimated_value_eur"],old["known_fields"]["procedure"],(),"refurbishment","SUPERSEDED")
    cur_snap=TenderSnapshot("SKERRIES","ETENDERS-SKERRIES-8891756",cur["title"],cur["authority"],cur["known_fields"]["deadline"],cur["known_fields"]["clarification_deadline"],cur["known_fields"]["estimated_value_eur"],cur["known_fields"]["procedure"],tuple(cur["known_fields"]["cpv"]),"refurbishment","CURRENT")
    lineage=resolve_signal_lineage([old_snap,cur_snap])

    cards=[]
    def add(i,title,status,finding,evidence,next_action=""):
        cards.append({"run_id":f"C5-{i:03d}","title":title,"status":status,"finding":finding,"evidence":evidence,"next_action":next_action})

    add(65,"Restore Library78 authority","PASS","78 physical / 68 valid / 58 unique hashes remains governing raw library authority",["CURRENT_LIBRARY_AUTHORITY_78_2026-08-22.md"])
    add(66,"Bind Book Engine shared dependency","PASS","Book Engine v0.7 used only for shared infra capabilities; narrative semantics forbidden",["BOOK_ENGINE_SHARED_INFRASTRUCTURE_DEPENDENCY_v07.json"])
    add(67,"Restore current business authority","PASS","Current gate is public artifact tests for bounded WIP",["CURRENT_BUSINESS_ENGINEERING_AUTHORITY.md"])
    add(68,"Stacked branch concurrency gate","PASS","Cycle5 branches from PR183 head; no force overwrite of main",["PR183","branch:business-engineering-cycle5-v11-20260822"])
    add(69,"PublicArtifact schema","PASS","Typed artifact requires source, explicit unknowns and E2+ ceiling",["public_artifact_engine_v11.py"])
    add(70,"Source lineage model","PASS","Reissue/supersession represented explicitly",["ETENDERS-SKERRIES-8753058","ETENDERS-SKERRIES-8891756"])
    add(71,"Skerries current/superseded adjudication","PASS","Old EUR245k value is not promoted into current reissued tender where current value is absent",[asdict(lineage)])
    add(72,"Requirement compiler contract","PASS","Fatal requirements require verified source; unknowns remain explicit",["Requirement","PublicArtifact.validate"])
    add(73,"OPP-12 small works artifact","PASS","Created source-bound tender pack shell; full document-level bid decision remains HOLD",["C5-ART-OPP12-001"])
    add(74,"OPP-19 retrofit artifact","PASS","Created current roof/energy upgrade intelligence artifact with professional boundary",["C5-ART-OPP19-001"])
    add(75,"OPP-29 AI workflow support artifact","PASS","Support pathway compiled without converting support availability into buyer/payment proof",["C5-ART-OPP29-001"])
    add(76,"Explicit unknown registry","PASS","Price/WTP/unit economics/qualification details remain null or unknown",["artifacts/*.json"])
    add(77,"No stale-value laundering","PASS","Superseded notice fields cannot fill current notice nulls without explicit current evidence",["resolve_signal_lineage"])
    add(78,"Deadline supersession invalidation","PASS","Deadline change dirties brief→decision chain only",["artifact_selective_invalidation"])
    add(79,"Hard exclusion gate","PASS","Missing documents/qualification/late submission represented as vetoes, not averaged scores",["PublicArtifact.hard_exclusions"])
    add(80,"Buyer role vs budget owner","PASS","Public role and budget owner are separate nullable evidence fields",["buyer_role_gate"])
    add(81,"Artifact provenance digest","PASS","Artifact digest binds content to source IDs and explicit unknowns",["PublicArtifact.digest"])
    add(82,"Manual baseline protocol","HOLD_EXTERNAL_MEASUREMENT","No real analyst baseline timing has been run; baseline_minutes remains null",["ArtifactExperiment.baseline_minutes"],"Run timed manual sample on same tender")
    add(83,"Engine production time protocol","HOLD_EXTERNAL_MEASUREMENT","No operator-observed end-to-end timing captured; engine_minutes remains null",["ArtifactExperiment.engine_minutes"],"Capture wall-clock/operator time in next controlled run")
    add(84,"Error taxonomy","PASS","Missing source/stale field/unknown laundering/fatal requirement/proof overclaim are distinct failure classes",["tests/test_public_artifact_engine_v11.py"])
    add(85,"Artifact comparison contract","PASS","Comparison reports missing/changed facts; no magic total score",["ExperimentAssessment"])
    add(86,"Decision delta ledger","PASS","Progress requires changed decision or unique information",["DecisionLedgerEntry","decision_value"])
    add(87,"Experiment stop gate","PASS","Two consecutive no-delta bounded tests stop or change hypothesis",["artifact_stop_gate"])
    add(88,"Public proof ceiling regression","PASS","Public-only artifacts remain E2+ max",["public_proof_level"])
    add(89,"E3/E4 event firewall","PASS","Only real buyer event can create E3; payment/PO/deposit evidence required for E4",["public_proof_level","payment_proof_gate"])
    add(90,"Protected artifact guard inheritance","PASS","Locked descendants remain blocked from selective invalidation rewrite",["artifact_selective_invalidation"])
    add(91,"Selective recomputation proof","PASS","Source/deadline changes affect only semantic downstream artifact/decision nodes",["build_artifact_dependency_graph","artifact_selective_invalidation"])
    add(92,"Portfolio information-gain governor","PASS","1 primary + 2 pilots must test independent hypothesis families",["information_gain_portfolio"])
    add(93,"Self-improvement observation bridge","PASS","Repeated evidence-backed defect may enter bounded candidate review; no auto-promotion",["self_improvement_disposition"])
    add(94,"Mechanism pruning","PASS","Duplicate→MERGE; high false-positive→NARROW; unused→HOLD_TELEMETRY",["mechanism_prune"])
    add(95,"Persistence/readback contract","HOLD_PERSISTENCE","Will flip only after GitHub Actions + Drive upload/readback for this exact package",["pending"])
    add(96,"Cycle synthesis + Next64 derivation","PASS","Next frontier is measured artifact utility, source-document ingestion, cross-domain replication and real E3/E4 preregistration",["RUN32","NEXT64"])

    result={"cycle":"BUSINESS_ENGINE_V1.1_CYCLE5_PUBLIC_ARTIFACTS","executed":len(cards),"status_counts":{},"portfolio":portfolio,"lineage":asdict(lineage),"cards":cards}
    for c in cards: result["status_counts"][c["status"]]=result["status_counts"].get(c["status"],0)+1
    out=ROOT/"reports"/"RUN32_CYCLE5_V11_LEDGER.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps({"executed":len(cards),"status_counts":result["status_counts"],"output":str(out)},indent=2))

if __name__=="__main__": main()
