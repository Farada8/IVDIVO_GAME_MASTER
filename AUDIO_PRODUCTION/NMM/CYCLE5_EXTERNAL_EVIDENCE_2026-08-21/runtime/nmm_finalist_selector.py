"""Select at most two whistle pairs only from human/device evidence."""
from __future__ import annotations

def select(rows:list[dict], *, min_accuracy=.75, min_realism=3.5, limit=2)->dict:
    eligible=[]
    for r in rows:
        if r.get('human_listeners',0)>=2 and r.get('phone_accuracy',0)>=min_accuracy and r.get('headphone_accuracy',0)>=min_accuracy and r.get('mean_realism',0)>=min_realism:
            eligible.append(r)
    eligible=sorted(eligible,key=lambda r:(r.get('phone_accuracy',0),r.get('mean_realism',0)),reverse=True)[:limit]
    return {'status':'FINALISTS_SELECTED' if eligible else 'NO_FINALISTS','finalists':eligible,'max_finalists':limit}
