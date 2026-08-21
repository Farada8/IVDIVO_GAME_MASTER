from __future__ import annotations
ORDER=['SOURCE_GUARDS','AUTH_PROVIDER_SNAPSHOT','VOICE_BINDINGS','S0_CANARY','S1_S4_CASTING','ASSET_HUMAN_GATE','HARD_PILOT','ALIGNMENT','DEVICE_QC','BLIND_HUMAN','SPECIALIST','ECONOMICS','FULL_E01','RELEASE']
def next_frontier(state):
 for k in ORDER:
  if not state.get(k): return k
 return 'COMPLETE'
def generic_runtime_change_allowed(defect):
 return bool(defect and defect.get('demonstrated_generic_gap') and defect.get('evidence_ref'))
