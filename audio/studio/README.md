# IVDIVO Audio Production Studio

Current studio router: `00_IVDIVO_AUDIO_STUDIO_INDEX_v3.0.md`.

## Quick start
1. Lock the book/script under story authority.
2. Choose delivery mode: `NARRATED`, `MULTI_VOICE`, `DRAMATIZED`, or `FULL_AUDIO_DRAMA`.
3. Initialize a project folder with `orchestrator.py`.
4. Run the 10-role prompt stack in SOP order.
5. Do provider dry run before live calls.
6. Approve a hard 3–5 minute pilot before batch rendering.
7. Lock accepted takes/assets.
8. Resolve real alignment before timeline/mix automation.
9. Mix/master from separated stems.
10. Run machine + human listening QC. Release only on GO.

Example local initialization:
```bash
python orchestrator.py init ./ROOM917_E02 ./source/ROOM917_E02.txt \
  --project-id ROOM917_E02 \
  --source-version 1.0 \
  --delivery-mode DRAMATIZED \
  --authority IVDIVO_AUDIO_CANON_v2.3 \
  --overlay ROOM917_AUDIO_OVERLAY_v2.0
```

Then:
```bash
python orchestrator.py status ./ROOM917_E02
python orchestrator.py verify-source ./ROOM917_E02
python orchestrator.py gate ./ROOM917_E02 AUTHORITY_PASS PASS
python orchestrator.py release-check ./ROOM917_E02
```

The orchestrator is intentionally provider-independent and makes no live API calls. Provider secrets are never committed.

## Main files
- `IVDIVO_AUDIO_STUDIO_OS_v3.0.md`
- `IVDIVO_AUDIO_STUDIO_10_SPECIALISTS_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_END_TO_END_SOP_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_MASTER_PROMPT_STACK_v3.0.md`
- `IVDIVO_AUDIO_STUDIO_MACHINE_CONTRACT_v1.0.yaml`
- `IVDIVO_ELEVENLABS_PROVIDER_ADAPTER_CONTRACT_v1.0.md`
- `IVDIVO_AUDIO_STUDIO_QC_RELEASE_GATES_v1.0.md`
- `orchestrator.py`
