from regulatory_shock_engine import *

def run():
    good = Opportunity("AI handoff",0,True,True)
    assert governor(good) == "TARGETED_OUTREACH_MAX_5"
    assert not may_build_software(good)
    interested = Opportunity("AI handoff",0,True,True,e3_events=1)
    assert governor(interested) == "DISCOVERY_AND_PRICE_TEST"
    assert may_build_software(interested)
    paid = Opportunity("AI handoff",0,True,True,e4_events=1)
    assert governor(paid) == "DELIVER_PAID_PILOT_AND_MEASURE"
    assert may_seek_acceleration_finance(paid)
    dead = Opportunity("old offer",0,True,True,qualified_contacts=20,e3_events=1,e4_events=0)
    assert governor(dead) == "KILL_OR_MATERIAL_PIVOT"
    risky = Opportunity("legal certification",0,True,True,legal_or_certification_claim=True)
    assert governor(risky) == "ESCALATE_SPECIALIST"
    cash = Opportunity("inventory business",100,True,True)
    assert governor(cash) == "REJECT_ZERO_CASH"
    stale = Opportunity("unsourced",0,False,True)
    assert governor(stale) == "HOLD_SOURCE"
    print("7 PASS / 0 FAIL")

if __name__ == "__main__":
    run()
