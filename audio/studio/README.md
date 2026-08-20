# IVDIVO Audio Production Studio

Current studio router: `00_IVDIVO_AUDIO_STUDIO_INDEX_v3.2.md`.

## Current audited changes
v3.2 adds provider-neutral alignment normalization, LIVE/DRY_RUN/MIXED build evidence, cross-build provenance, voice binding ledger, silent reaction anchors, provider preflight, source-vs-stem stereo-intent QC, cross-domain acoustic/pitch identity, manual-review triage, review priority queue and dependency-DAG gates.

## Quick start
1. Lock the book/script under story authority.
2. Choose delivery mode: `NARRATED`, `MULTI_VOICE`, `DRAMATIZED`, or `FULL_AUDIO_DRAMA`.
3. Initialize a project folder with `orchestrator.py`.
4. Run the 10-role prompt stack and v3.2 patch rules.
5. Build `VOICE_BINDING_LEDGER`, render blocks and dry-run requests.
6. Pass provider contract + connectivity/credential/capability preflight before live calls.
7. Approve a hard 3–5 minute pilot before batch rendering.
8. Record per-block live evidence or approved reuse provenance.
9. Lock accepted takes/assets.
10. Normalize provider alignment before timeline/mix automation.
11. Mix/master from separated stems and run source-vs-stem stereo-intent QC.
12. Build review priority queue, resolve mandatory manual reviews, then human listen.
13. Release only on GO.

Example initialization:
```bash
python orchestrator.py init ./ROOM917_E02 ./source/ROOM917_E02.txt \
  --project-id ROOM917_E02 \
  --source-version 1.0 \
  --delivery-mode DRAMATIZED \
  --authority IVDIVO_AUDIO_STUDIO_v3.2 \
  --overlay ROOM917_AUDIO_OVERLAY_v2.0
```

Useful commands:
```bash
python orchestrator.py status ./ROOM917_E02
python orchestrator.py verify-source ./ROOM917_E02
python orchestrator.py gate ./ROOM917_E02 MUSIC_PLAN_PASS NOT_APPLICABLE --reason "No score commissioned for this mode"
python orchestrator.py render-status ./ROOM917_E02 LIVE
python orchestrator.py set-render-blocks ./ROOM917_E02 --block E02_B001 --block E02_B002
python orchestrator.py record-evidence ./ROOM917_E02 --block-id E02_B001 --request req.json --response resp.json --audio take.wav --raw-alignment align.json --request-hash HASH
python orchestrator.py release-check ./ROOM917_E02
```

Alignment normalization:
```bash
python alignment_normalizer.py raw_alignment.json normalized_alignment.json --block-id E02_B001 --unit-id E02_U001
```

Stereo integrity:
```bash
python stereo_integrity_qc.py source_asset.wav rendered_stem.wav --intent NATURAL_STEREO --output stereo_report.json
```

The orchestrator is intentionally provider-independent and makes no live API calls. Provider secrets are never committed.

## Main files
- `00_IVDIVO_AUDIO_STUDIO_INDEX_v3.2.md`
- `IVDIVO_AUDIO_STUDIO_CANON_PATCH_v3.2_AUDITED.md`
- `IVDIVO_AUDIO_STUDIO_OS_v3.0.md`
- `IVDIVO_AUDIO_STUDIO_10_SPECIALISTS_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_END_TO_END_SOP_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_MASTER_PROMPT_STACK_v3.0.md`
- `IVDIVO_AUDIO_STUDIO_MACHINE_CONTRACT_v1.1.yaml`
- `IVDIVO_AUDIO_STUDIO_ARTIFACT_TEMPLATES_v1.1.json`
- `IVDIVO_ELEVENLABS_PROVIDER_ADAPTER_CONTRACT_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_QC_RELEASE_GATES_v1.0.md`
- `alignment_normalizer.py`
- `stereo_integrity_qc.py`
- `orchestrator.py`
- `tests/`
