#!/usr/bin/env python3
"""Provider-independent byte escrow helper for critical IVDIVO assets.

This tool proves local/durable byte parity. It does not contain cloud credentials
and does not pretend that a local copy is a Google Drive upload. A connector or
operator may upload the verified destination file afterward and record that
external durable pointer in the emitted manifest.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, tempfile, time, wave
from pathlib import Path


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(block_size), b""):
            h.update(b)
    return h.hexdigest()


def wav_meta(path: Path) -> dict | None:
    try:
        with wave.open(str(path), "rb") as w:
            return {
                "channels": w.getnchannels(),
                "sample_width_bytes": w.getsampwidth(),
                "sample_rate_hz": w.getframerate(),
                "frames": w.getnframes(),
                "duration_seconds": round(w.getnframes() / w.getframerate(), 6),
                "compression": w.getcomptype(),
            }
    except (wave.Error, EOFError):
        return None


def fsync_file(path: Path) -> None:
    with path.open("rb") as f:
        os.fsync(f.fileno())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("--dest-dir", type=Path, required=True)
    ap.add_argument("--asset-id", required=True)
    ap.add_argument("--expected-sha256", default=None)
    ap.add_argument("--manifest", type=Path, default=None)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    src = args.source.resolve()
    if not src.is_file():
        raise SystemExit(f"Source not found: {src}")
    args.dest_dir.mkdir(parents=True, exist_ok=True)
    dest = (args.dest_dir / src.name).resolve()
    pre_size = src.stat().st_size
    pre_hash = sha256_file(src)
    if args.expected_sha256 and pre_hash != args.expected_sha256.lower():
        raise SystemExit(f"Source SHA256 mismatch: expected {args.expected_sha256}, got {pre_hash}")

    status = "COPIED_AND_READBACK_VERIFIED"
    if dest.exists():
        existing_hash = sha256_file(dest)
        if existing_hash == pre_hash and dest.stat().st_size == pre_size:
            status = "ALREADY_ESCROWED_READBACK_VERIFIED"
        elif not args.overwrite:
            raise SystemExit(f"Destination exists with different bytes: {dest}")

    if status == "COPIED_AND_READBACK_VERIFIED":
        fd, tmp_name = tempfile.mkstemp(prefix=f".{src.name}.", suffix=".tmp", dir=str(args.dest_dir))
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            shutil.copyfile(src, tmp)
            fsync_file(tmp)
            tmp_hash = sha256_file(tmp)
            if tmp.stat().st_size != pre_size or tmp_hash != pre_hash:
                raise RuntimeError("Temporary copy failed byte-parity verification")
            if dest.exists() and args.overwrite:
                dest.unlink()
            os.replace(tmp, dest)
        finally:
            if tmp.exists():
                tmp.unlink()

    post_size = dest.stat().st_size
    post_hash = sha256_file(dest)
    if post_size != pre_size or post_hash != pre_hash:
        raise SystemExit("Escrow readback failed byte-parity verification")

    manifest = {
        "schema_version": "ivdivo.asset_escrow/1.0",
        "asset_id": args.asset_id,
        "status": status,
        "source": {"path": str(src), "size_bytes": pre_size, "sha256": pre_hash},
        "escrow": {"path": str(dest), "size_bytes": post_size, "sha256": post_hash},
        "byte_parity": True,
        "wav_metadata": wav_meta(dest),
        "cloud_persistence_status": "NOT_ASSERTED_BY_THIS_TOOL",
        "next_cloud_gate": "UPLOAD_VERIFIED_BYTES_TO_FOUNDER_AUTHORIZED_DURABLE_STORAGE_THEN_READBACK_AND_REGISTER_POINTER",
        "created_unix": time.time(),
    }
    manifest_path = args.manifest or (args.dest_dir / f"{args.asset_id}.escrow.json")
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
