# ROOM917 E01 — Master Escrow + P003A2 Analyzer v1

Two executable, provider-independent tools for the current post-render frontier.

## 1. `master_escrow.py`

Copies a critical asset to a controlled filesystem destination using temp-file + atomic rename, verifies SHA-256 and size before/after, and emits an escrow manifest. It does **not** claim Google Drive persistence; a Drive connector/operator must upload the verified file and read it back/register the resulting pointer.

## 2. `p003a2_interval_analyzer.py`

Reads real PCM WAV bytes, measures fixed 100 ms RMS windows, extracts exact contiguous runs below configurable dBFS thresholds, and writes JSON + CSV. It is fail-closed: amplitude alone never proves a defect; without explicit authoritative cue evidence every interval remains `UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE`.

ROOM917 current usage once the exact full master bytes are recovered:

```bash
python p003a2_interval_analyzer.py \
  ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav \
  --segment-start 0 \
  --segment-end 444.980 \
  --window-ms 100 \
  --thresholds -85 -50 -45 \
  --expected-sha256 231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8 \
  --output-json ROOM917_E01_P003A2_INTERVALS_v1.json \
  --output-csv ROOM917_E01_P003A2_INTERVALS_v1.csv
```

Then join the measured runs to **accepted live Scene1/2 cue lineage** and classify only as:

- `PROTECTED_AUTHORED_PAUSE`
- `VALID_LOW_DENSITY`
- `MISSING_ROOM_OR_AMBIENCE_SUPPORT`
- `MISSING_CAUSAL_OVERLAP_CANDIDATE`
- `UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE`

No interval is patch-authorized merely because it is quiet.

## Validation

`python tests/test_tools.py`

Synthetic 24-bit stereo validation checks threshold extraction and byte-parity escrow. Real Scene3 smoke validation matches current authority: 0 s below −85 / −50 / −45 dBFS on 100 ms windows.

## Windows wrappers

```powershell
pip install -r .\requirements.txt
.\RUN_MASTER_ESCROW.ps1 -SourceFile "C:\path\master.wav" -EscrowDir "D:\IVDIVO_ESCROW\ROOM917" -AssetId "ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K" -ExpectedSha256 "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
.\RUN_ROOM917_P003A2.ps1 -MasterWav "D:\IVDIVO_ESCROW\ROOM917\ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav"
```

The P003A2 wrapper is deliberately hard-bound to the accepted E01 full-master SHA-256 and pre-Scene3 endpoint `444.980 s`. A different file fails closed.
