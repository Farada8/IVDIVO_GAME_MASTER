"""Code unwanted sound associations while retaining verbatim source text separately."""
from __future__ import annotations
CODES={'police':['police','cop','siren'],'horror':['horror','scary','creepy'],'cartoon':['cartoon','comic'],'toy':['toy','plastic','cheap']}
def code(text:str)->list[str]:
    t=(text or '').lower(); out=[]
    for label,terms in CODES.items():
        if any(x in t for x in terms): out.append(label.upper())
    return out or ['OTHER_OR_NONE']
