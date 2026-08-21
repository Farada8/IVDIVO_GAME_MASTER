from tools.validate_story_core_causality import validate, REQUIRED_PATHS


def core():
    return {
        "hero":"A",
        "want":"recover the file",
        "why_now":"the archive will be destroyed tonight",
        "opposition":"the custodian locks access after seeing the attempt",
        "wrong_strategy":"A tries an informal favor that exposes the plan",
        "price":"A loses legitimate access and risks a colleague",
        "midpoint":"A discovers the only legal copy is in the custodian's audit trail",
        "climax_choice":"A publicly submits evidence that also implicates her own shortcut",
        "resolution":"the archive survives and the custodian's concealment is exposed",
        "series_hook":None,
        "causal_edges":[{"from":a,"to":b,"because":"the earlier state directly creates the next pressure"} for a,b in REQUIRED_PATHS],
        "climax_caused_by_hero":True,
        "resolution_closes_main_conflict":True,
        "series_hook_after_resolution":True,
    }


def test_connected_core_passes():
    assert validate(core())["status"] == "PASS"


def test_label_complete_but_missing_midpoint_to_climax_fails():
    x=core(); x["causal_edges"]=[e for e in x["causal_edges"] if not (e["from"]=="MIDPOINT" and e["to"]=="CLIMAX_CHOICE")]
    r=validate(x); assert r["status"]=="FAIL"; assert "MISSING_CAUSAL_EDGE:MIDPOINT->CLIMAX_CHOICE" in r["errors"]


def test_police_solve_climax_fails_even_if_labels_complete():
    x=core(); x["climax_caused_by_hero"]=False
    assert "CLIMAX_NOT_CAUSED_BY_HERO" in validate(x)["errors"]


def test_unclosed_main_conflict_fails():
    x=core(); x["resolution_closes_main_conflict"]=False
    assert "MAIN_CONFLICT_NOT_CLOSED" in validate(x)["errors"]


def test_series_hook_before_resolution_fails():
    x=core(); x["series_hook"]="next villain arrives"; x["series_hook_after_resolution"]=False
    assert "SERIES_HOOK_BEFORE_RESOLUTION" in validate(x)["errors"]
