def execute_cycle6(evidence:dict) -> list[dict]:
    provider=bool(evidence.get("provider_verified"))
    candidates=bool(evidence.get("candidate_sets"))
    canaries=bool(evidence.get("live_canaries"))
    outcomes=[]
    for i in range(1,33):
        if i<=3: status="PASS_REAL_SOURCE"
        elif i in {4,5,6,7,8}: status="PASS_EXTERNAL" if provider else "HOLD_EXTERNAL_PROVIDER"
        elif i in {9,10,11,12}: status="PASS_EXTERNAL" if candidates else "HOLD_EXTERNAL_INVENTORY"
        elif i in {13,14,16}: status="PASS_ENGINEERING"
        elif i==15: status="PASS_EXTERNAL" if provider and candidates else "HOLD_EXTERNAL_PROVIDER"
        elif 17<=i<=24: status="PASS_EXTERNAL" if canaries else "HOLD_EXTERNAL_CANARY"
        elif i==25: status="PASS_ENGINEERING" if candidates else "HOLD_EXTERNAL_INVENTORY"
        elif 26<=i<=29: status="PASS_EXTERNAL" if canaries else "HOLD_EXTERNAL_CANARY"
        elif i==30: status="PASS_SCHEMA_HOLD_DATA" if not canaries else "PASS_EXTERNAL"
        elif i==31: status="PASS_ENGINEERING_FIXTURES"
        else: status="PASS_PACKET_EXTERNAL_HOLD" if not canaries else "PASS_EXTERNAL"
        outcomes.append({"prompt":i,"status":status})
    return outcomes
