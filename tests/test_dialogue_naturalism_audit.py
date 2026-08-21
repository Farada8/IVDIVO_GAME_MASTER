from tools.dialogue_naturalism_audit import audit


def test_counts_repeated_frames_without_calling_them_defects():
    text = '“I know.” “That is not the question.” “Apparently.”'
    report = audit(text, script_format=False)
    assert report["global_frame_counts"]["i_know"] == 1
    assert report["global_frame_counts"]["that_is_not"] == 1
    assert report["global_frame_counts"]["apparently"] == 1
    assert "cannot authorize rewriting" in report["disclaimer"]


def test_script_mode_builds_speaker_profiles():
    text = """ETHAN: I know.\nAOIFE: That is not what I asked.\nETHAN: Exactly.\nAOIFE: Fine.\n"""
    report = audit(text, script_format=True)
    assert set(report["speaker_profiles"]) == {"AOIFE", "ETHAN"}
    assert report["document"]["dialogue_units"] == 4


def test_cluster_signal_is_only_a_signal():
    text = """A: I know.\nB: That is not the question.\nA: Exactly.\nB: Fine.\n"""
    report = audit(text, script_format=True)
    assert len(report["cleverness_cluster_signals"]) == 1
    assert report["required_next_step"].startswith("Human/LLM naturalism review")
