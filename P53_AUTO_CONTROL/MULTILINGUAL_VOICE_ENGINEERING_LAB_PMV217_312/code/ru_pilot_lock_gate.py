#!/usr/bin/env python3
import json,sys
from pathlib import Path
REQ=["ru_text_locked","provider_snapshot_pass","provisional_voice_lock","slice_pass","full_e01_qc_pass","blind_listener_pass","no_unresolved_actionable_pickups"]
def gate(d):
    missing=[x for x in REQ if not d.get(x)]
    return {"artifact":"BODYGUARD_RU_E01_PILOT_LOCK_GATE_v1","verdict":"LOCK" if not missing else "HOLD","missing":missing,
      "lock_scope":"RU_E01_PILOT_ONLY","season_lock":False}
if __name__=="__main__":
    d=json.loads(Path(sys.argv[1]).read_text()); Path(sys.argv[2]).write_text(json.dumps(gate(d),indent=2))
