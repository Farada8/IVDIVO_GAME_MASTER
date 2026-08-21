from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

STATUS_RANK={"AUTHORITY":100,"STATE":80,"WORKING_FRONTIER":70,"MIRROR":50,"PACKAGE":45,"POST_PACKAGE_EXTENSION":40,"REFERENCE":10,"HISTORY":0,"SUPERSEDED":-1}

@dataclass(frozen=True)
class Surface:
    surface_id:str; locator:str; kind:str; scope:str; status:str; updated:str|None=None; revision:str|None=None; authority:bool=False

def compile_surface_manifest(surfaces:list[dict[str,Any]])->dict[str,Any]:
    if not surfaces: raise ValueError("NO_SURFACES")
    normalized=[]; seen=set()
    for row in surfaces:
        s=Surface(**row)
        if s.surface_id in seen: raise ValueError(f"DUPLICATE_SURFACE_ID:{s.surface_id}")
        seen.add(s.surface_id)
        if s.status not in STATUS_RANK: raise ValueError(f"UNKNOWN_SURFACE_STATUS:{s.status}")
        normalized.append(s)
    by_scope={}
    for s in normalized: by_scope.setdefault(s.scope,[]).append(s)
    routes={}
    for scope,rows in by_scope.items():
        auth=[r for r in rows if r.authority and r.status=="AUTHORITY"]
        if len(auth)!=1:
            routes[scope]={"status":"STOP","reason":"AUTHORITY_SPLIT_BRAIN" if len(auth)>1 else "AUTHORITY_MISSING","candidates":[asdict(x) for x in auth]}; continue
        usable=[r for r in rows if r.status not in {"SUPERSEDED","HISTORY"}]
        frontier=max(usable,key=lambda r:((r.updated or ""),STATUS_RANK[r.status]))
        routes[scope]={"status":"PASS","authority":asdict(auth[0]),"frontier":asdict(frontier)}
    return {"schema":"ivdivo.current_surface_manifest/0.2","routes":routes,"surfaces":[asdict(x) for x in normalized]}
