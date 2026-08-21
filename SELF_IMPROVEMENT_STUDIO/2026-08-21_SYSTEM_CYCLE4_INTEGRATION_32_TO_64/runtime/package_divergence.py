from __future__ import annotations

def compare(package_files:dict,main_extensions:list[dict])->dict:
    rows=[]
    for ext in main_extensions:
        path=ext["path"]; package_hash=package_files.get(path)
        if package_hash and package_hash==ext.get("blob_hash"):status="PRESENT_IN_PACKAGE"
        elif ext.get("status")=="VERIFIED_CURRENT":status="VERIFIED_POST_PACKAGE"
        elif ext.get("status") in {"PILOTING","WORKING","GO_FOR_REVIEW"}:status="PILOT_ONLY"
        else:status="NOT_ACCEPTED"
        rows.append({"path":path,"status":status,"package_hash":package_hash,"main_hash":ext.get("blob_hash")})
    return {"rows":rows,"new_package_required":any(r["status"]!="PRESENT_IN_PACKAGE" for r in rows)}

def candidate_manifest(base_package:dict,extensions:list[dict])->dict:
    accepted=[e for e in extensions if e.get("status") in {"VERIFIED_CURRENT","ACCEPTED_FOR_NEXT_PACKAGE"}]
    return {"base_package":base_package,"accepted_extensions":accepted,"excluded":[e for e in extensions if e not in accepted],"promotion_gate":"BUILD_COLD_UNPACK_FULL_REGRESSION_CHECKSUM_READBACK"}
