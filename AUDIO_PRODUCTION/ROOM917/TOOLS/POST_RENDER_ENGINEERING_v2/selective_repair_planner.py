#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--classified",required=True); ap.add_argument("--lineage",required=True); ap.add_argument("--master-sha256",required=True); ap.add_argument("--out",required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.classified).read_text(encoding="utf-8")); lineage=json.loads(Path(args.lineage).read_text(encoding="utf-8"))
    patches=[]; holds=[]
    for i,r in enumerate(data.get("rows",[]),1):
        if r.get("classification")!="MISSING_ROOM_OR_AMBIENCE_SUPPORT" or not r.get("patch_authorized"):
            holds.append({"interval":r,"reason":"NOT_AUTHORIZED_BY_CLASSIFICATION_CONTRACT"}); continue
        s=float(r["start_seconds"]); e=float(r["end_seconds"]); blocks=[]
        for b in lineage.get("blocks",[]):
            if "start_seconds" in b and "end_seconds" in b: bs=float(b["start_seconds"]); be=float(b["end_seconds"])
            elif "start_s" in b and "end_s" in b: bs=float(b["start_s"]); be=float(b["end_s"])
            else: continue
            if max(s,bs)<min(e,be): blocks.append(b)
        if not blocks:
            holds.append({"interval":r,"reason":"NO_RESOLVED_BLOCK_FOR_ASSET_BINDING"}); continue
        beds=sorted({b["required_bed"] for b in blocks})
        if len(beds)!=1:
            holds.append({"interval":r,"reason":"CROSSES_MULTIPLE_BED_DOMAINS"}); continue
        patches.append({"patch_id":f"P004A_BED_{i:04d}","source_master_sha256":args.master_sha256,"interval_start_seconds":s,"interval_end_seconds":e,"defect_id":"D003","classification":"MISSING_ROOM_OR_AMBIENCE_SUPPORT","repair_layer":"ROOM_WEATHER_MATERIAL_BED","source_asset":beds[0],"fade_in_ms":150,"fade_out_ms":200,"protected_invariants":["LOCKED_STORY","SCENE3_V1_3E_LINEAGE","NO_MUSIC_AS_BED_REPAIR","NO_BLANKET_FILL"],"regression_tests":["FORMAT_DURATION_STABILITY","NO_CLIPPING","PROTECTED_RANGES_UNCHANGED","SCENE3_BYTES_UNCHANGED","UNAUTHORIZED_RANGES_UNCHANGED"],"rollback":"RESTORE_SOURCE_MASTER_AND_DISCARD_PATCH_RENDER"})
    out={"schema_version":"room917.selective_repair_plan/1.0","status":"READY" if patches else "HOLD","patches":patches,"holds":holds}
    Path(args.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"{out['status']} patches={len(patches)} holds={len(holds)}")
if __name__=="__main__": main()
