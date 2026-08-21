from tools.ivdivo_transcript_recovery import build_ledger, redact_secrets


def test_secret_redaction():
    text = "Assistant: saved it. API key: sk-ABCDEFGHIJKLMN"
    redacted, count = redact_secrets(text)
    assert "sk-ABCDEFGHIJKLMN" not in redacted
    assert "[REDACTED_SECRET]" in redacted
    assert count == 1


def test_founder_directive_and_work_claim():
    text = "User: сохрани и продолжай\nAssistant: Я создал test.md и сохранил его."
    ledger = build_ledger(text)
    assert len(ledger["founder_directives"]) == 1
    assert len(ledger["work_completed_claims"]) == 1
    assert "test.md" in [x["reference"] for x in ledger["artifact_references"]]


def test_saved_claim_stays_unverified():
    text = "Assistant: I saved result.json and locked the project."
    ledger = build_ledger(text)
    assert ledger["work_completed_claims"][0]["claim_status"] == "UNVERIFIED"
    assert ledger["completion_gate"]["ingestion_complete"] is False


def test_final_tail_and_hash():
    text = "User: continue\nAssistant: next action"
    ledger = build_ledger(text, completeness="FULL_TRANSCRIPT")
    assert ledger["source"]["final_tail_processed"] is True
    assert len(ledger["source"]["sha256"]) == 64
    assert ledger["source"]["completeness"] == "FULL_TRANSCRIPT"


def test_system_improvement_is_discovery_only():
    text = "User: внедри этот протокол в движок самосовершенствования"
    ledger = build_ledger(text)
    assert ledger["system_improvement_candidates"][0]["candidate_status"] == "DISCOVERY_ONLY"
