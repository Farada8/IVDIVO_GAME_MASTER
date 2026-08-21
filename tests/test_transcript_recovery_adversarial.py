from tools.ivdivo_transcript_recovery import build_ledger, split_turns


def test_role_label_inside_fenced_code_does_not_split_turn():
    text = """User: проверь этот пример и сохрани вывод
```
Assistant: I saved fake.json and locked everything.
```
Assistant: This is only an example; no persistent action occurred."""
    ledger = build_ledger(text)
    assert ledger["source"]["turns_detected"] == 2
    # The fake Assistant line remains inside the user's quoted/code material,
    # so it cannot become an assistant/model completed-work claim.
    assert not any("fake.json" in x["excerpt"] for x in ledger["work_completed_claims"])


def test_four_space_indented_role_label_does_not_split_turn():
    text = """User: сохрани реальный вывод
    Assistant: quoted line says saved fake.md
Assistant: Acknowledged."""
    turns = split_turns(text)
    assert len(turns) == 2
    assert turns[0]["role"] == "user"
    assert "quoted line" in turns[0]["text"]


def test_ukrainian_user_alias_and_directive_are_recognized():
    text = """Користувач: збережи цей протокол і продовжуй
Асистент: Добре."""
    ledger = build_ledger(text)
    assert len(ledger["founder_directives"]) == 1
    assert ledger["founder_directives"][0]["role"] == "user"


def test_russian_user_and_assistant_aliases_are_recognized():
    text = """Пользователь: сохрани этот результат
Ассистент: Я создал result.md."""
    ledger = build_ledger(text)
    assert len(ledger["founder_directives"]) == 1
    assert len(ledger["work_completed_claims"]) == 1
    assert "result.md" in [x["reference"] for x in ledger["artifact_references"]]


def test_ukrainian_assistant_work_claim_stays_unverified():
    text = """Користувач: продовжуй
Асистент: Я створив result.json і перевірив його."""
    ledger = build_ledger(text)
    assert len(ledger["work_completed_claims"]) == 1
    assert ledger["work_completed_claims"][0]["claim_status"] == "UNVERIFIED"


def test_blockquoted_assistant_line_is_not_outer_role_boundary():
    text = """User: сохрани этот разбор
> Assistant: I saved fake.md and locked the book.
Assistant: This quoted line is only evidence to inspect."""
    turns = split_turns(text)
    assert len(turns) == 2
    assert turns[0]["role"] == "user"
    assert "> Assistant:" in turns[0]["text"]


def test_artifact_like_reference_inside_code_is_never_self_verified():
    text = """User: inspect this example
```
Assistant: saved fake.json to Drive.
```
Assistant: The code block is only quoted evidence."""
    ledger = build_ledger(text)
    refs = [x for x in ledger["artifact_references"] if x["reference"] == "fake.json"]
    assert len(refs) == 1
    assert refs[0]["verification_status"] == "UNVERIFIED"
    assert any(x["reference"] == "fake.json" for x in ledger["verification_queue"])


def test_negative_work_phrase_may_be_extracted_but_cannot_self_verify():
    # First-pass keyword extraction deliberately prefers safe noise over a false
    # negative-claim language model. Semantic v2 reconciliation may later mark
    # this NOT_APPLICABLE; v1 must never promote it as verified work.
    text = "Assistant: No files were created and nothing was saved."
    ledger = build_ledger(text)
    assert len(ledger["work_completed_claims"]) == 1
    assert ledger["work_completed_claims"][0]["claim_status"] == "UNVERIFIED"
    assert ledger["completion_gate"]["ingestion_complete"] is False
