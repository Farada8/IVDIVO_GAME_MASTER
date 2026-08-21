import json
from pathlib import Path

import pytest

from tools.ivdivo_registry_transaction import cmd_compact, cmd_register, cmd_rollback, sha256_file


class Args:
    pass


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate(cid="SI-0008", status="DEVELOPING"):
    return {
        "candidate_id": cid,
        "title": "candidate",
        "candidate_type": "TOOLING_OR_AUTOMATION",
        "status": status,
        "scope": "UNIVERSAL_IVDIVO",
        "source_provenance": [{"source_type": "GITHUB", "locator": "fixture"}],
        "problem_or_opportunity": "problem",
        "proposed_mechanism": "mechanism",
        "owner_role": "tester",
        "next_action": "next",
        "next_gate": "gate",
        "application_targets": ["x"],
        "verification_evidence": ["evidence"] if status == "VERIFIED_CURRENT" else [],
        "hold_trigger": "trigger" if status == "HOLD_WITH_TRIGGER" else None,
        "terminal_reason": "reason" if status in {"REJECTED", "REJECTED_WITH_REASON", "SUPERSEDED", "ROLLED_BACK"} else None,
    }


def make_repo(tmp_path: Path):
    base = tmp_path / "31_IDEAS" / "CURRENT_IMPROVEMENT_REGISTRY.json"
    ext = tmp_path / "31_IDEAS" / "REGISTRY_EXTENSIONS"
    family = tmp_path / "31_IDEAS" / "CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json"
    write_json(base, {"schema_version": "1.0", "candidates": [candidate("SI-0007", "VERIFIED_CURRENT")]})
    write_json(family, {
        "schema_version": "1.2",
        "base_registry": "31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json",
        "extension_directory": "31_IDEAS/REGISTRY_EXTENSIONS/",
        "known_extensions": [],
    })
    return base, ext, family


def reg_args(tmp_path: Path, candidate_path: Path, expected_sha=None, txn_id="txn-test"):
    a = Args()
    a.repo_root = str(tmp_path)
    a.family = "31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json"
    a.candidate = str(candidate_path)
    a.expected_family_sha = expected_sha
    a.txn_id = txn_id
    return a


def test_positive_commit_and_idempotent_noop(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    src = tmp_path / "candidate.json"
    write_json(src, candidate("SI-0008"))
    before = sha256_file(family)
    assert cmd_register(reg_args(tmp_path, src, before)) == 0
    assert (ext / "SI-0008.json").exists()
    data = json.loads(capsys.readouterr().out)
    assert data["status"] == "COMMITTED"
    assert cmd_register(reg_args(tmp_path, src, sha256_file(family), txn_id="txn-noop")) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["status"] == "NOOP_EXISTING"


def test_duplicate_id_conflict_does_not_mutate(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    existing = candidate("SI-0008")
    write_json(ext / "SI-0008.json", existing)
    fam = json.loads(family.read_text())
    fam["known_extensions"] = ["31_IDEAS/REGISTRY_EXTENSIONS/SI-0008.json"]
    write_json(family, fam)
    before_family = family.read_bytes()
    before_shard = (ext / "SI-0008.json").read_bytes()
    altered = candidate("SI-0008")
    altered["title"] = "different"
    src = tmp_path / "candidate.json"
    write_json(src, altered)
    assert cmd_register(reg_args(tmp_path, src, sha256_file(family))) == 4
    assert json.loads(capsys.readouterr().out)["status"] == "DUPLICATE_ID_CONFLICT"
    assert family.read_bytes() == before_family
    assert (ext / "SI-0008.json").read_bytes() == before_shard


def test_malformed_lifecycle_fails_before_write(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    bad = candidate("SI-0008")
    bad["status"] = "MAGIC_CURRENT"
    src = tmp_path / "candidate.json"
    write_json(src, bad)
    before = family.read_bytes()
    assert cmd_register(reg_args(tmp_path, src, sha256_file(family))) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "INVALID_CANDIDATE"
    assert family.read_bytes() == before
    assert not (ext / "SI-0008.json").exists()


def test_stale_base_fails_before_write(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    src = tmp_path / "candidate.json"
    write_json(src, candidate("SI-0008"))
    assert cmd_register(reg_args(tmp_path, src, "0" * 64)) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "STALE_BASE"
    assert not (ext / "SI-0008.json").exists()


def test_injected_interruption_rolls_back_byte_exact(tmp_path, capsys, monkeypatch):
    _, ext, family = make_repo(tmp_path)
    src = tmp_path / "candidate.json"
    write_json(src, candidate("SI-0008"))
    before_family = family.read_bytes()
    monkeypatch.setenv("IVDIVO_REGISTRY_TXN_FAIL_AFTER", "SHARD")
    assert cmd_register(reg_args(tmp_path, src, sha256_file(family), txn_id="txn-fail")) == 5
    assert json.loads(capsys.readouterr().out)["status"] == "ROLLED_BACK_ON_ERROR"
    assert family.read_bytes() == before_family
    assert not (ext / "SI-0008.json").exists()


def test_explicit_rollback_restores_previous_bytes(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    src = tmp_path / "candidate.json"
    write_json(src, candidate("SI-0008"))
    before_family = family.read_bytes()
    assert cmd_register(reg_args(tmp_path, src, sha256_file(family), txn_id="txn-rollback")) == 0
    capsys.readouterr()
    a = Args()
    a.repo_root = str(tmp_path)
    a.txn_id = "txn-rollback"
    assert cmd_rollback(a) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ROLLED_BACK"
    assert family.read_bytes() == before_family
    assert not (ext / "SI-0008.json").exists()


def test_deterministic_compaction_roundtrip(tmp_path, capsys):
    _, ext, family = make_repo(tmp_path)
    for cid in ["SI-0009", "SI-0008"]:
        write_json(ext / f"{cid}.json", candidate(cid))
    fam = json.loads(family.read_text())
    fam["known_extensions"] = [
        "31_IDEAS/REGISTRY_EXTENSIONS/SI-0009.json",
        "31_IDEAS/REGISTRY_EXTENSIONS/SI-0008.json",
    ]
    write_json(family, fam)
    a = Args()
    a.repo_root = str(tmp_path)
    a.family = "31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json"
    a.output = "31_IDEAS/BUILD/compact.json"
    a.manifest = "31_IDEAS/BUILD/manifest.json"
    assert cmd_compact(a) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "PASS"
    compact = json.loads((tmp_path / a.output).read_text())
    assert [x["candidate_id"] for x in compact["candidates"]] == ["SI-0007", "SI-0008", "SI-0009"]
    manifest = json.loads((tmp_path / a.manifest).read_text())
    assert manifest["readback_status"] == "PASS"
    first_hash = manifest["output_sha256"]
    assert cmd_compact(a) == 0
    capsys.readouterr()
    manifest2 = json.loads((tmp_path / a.manifest).read_text())
    assert manifest2["output_sha256"] == first_hash
