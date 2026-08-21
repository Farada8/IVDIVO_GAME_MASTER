#!/usr/bin/env python3
import json,sys
GRAPH={'EN_SOURCE':[],'RU_GLOSSARY':['RU_TEXT','RU_PRON_DICT'],'RU_TEXT':['RU_ANCHORS','RU_RENDER_PLAN','RU_SEMANTIC_CHECK'],'RU_ANCHORS':['RU_VOICE_AUDITION'],'RU_PRON_DICT':['RU_RENDER_PLAN','RU_AUDIO'],'RU_VOICE_AUDITION':['RU_VOICE_LOCK'],'RU_VOICE_LOCK':['RU_AUDIO','EN_VOICE_BRIDGE'],'RU_RENDER_PLAN':['RU_AUDIO'],'RU_AUDIO':['RU_MIX','RU_LISTENER_GATE'],'RU_MIX':['RU_LISTENER_GATE'],'RU_LISTENER_GATE':['RU_PILOT_LOCK'],'RU_PILOT_LOCK':['EN_VOICE_BRIDGE']}
def descendants(nodes):
    seen=set(); stack=list(nodes)
    while stack:
        n=stack.pop()
        for x in GRAPH.get(n,[]):
            if x not in seen: seen.add(x); stack.append(x)
    return sorted(seen)
if __name__=='__main__':
    changed=sys.argv[1:] or ['RU_GLOSSARY']
    print(json.dumps({'artifact':'DEPENDENCY_INVALIDATION','changed':changed,'invalidate':descendants(changed),'rollback':'restore prior version ids/hashes; never overwrite source authority'},indent=2))
