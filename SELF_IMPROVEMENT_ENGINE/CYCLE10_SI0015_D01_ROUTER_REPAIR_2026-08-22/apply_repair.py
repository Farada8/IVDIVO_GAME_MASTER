from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'patched'
OUT.mkdir(exist_ok=True)

SYSTEM=ROOT/'CURRENT_IVDIVO_SYSTEM_STATE.json'
PORTFOLIO=ROOT/'CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json'

D01_LOCK='D01_THE_WIFE_AT_HIS_WEDDING_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED'
SMITH={
  'project_id':'IVDIVO_BOOK_3_SMITH_FULL_NOVEL',
  'title':'SMITH',
  'mode':'FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE',
  'project_state_path':None,
  'source_transition_from':'PROJECTS/THE_WIFE_AT_HIS_WEDDING/CURRENT_STATE.md',
  'next_unblocked_obligation':'FRESH_AUTHORITY_RECONCILIATION_THEN_PREVIOUS_BOOK_CONSEQUENCE_CONTINUITY_CHECK_THEN_STORY_CORE_THEN_HUMAN_SCENE_DIALOGUE_CALIBRATION_THEN_CAUSAL_ARCHITECTURE_THEN_PRE_PROSE_STORY_GATE',
  'authority_boundary':'NO_SMITH_PROSE_UNTIL_FRESH_AUTHORITY_AND_PRE_PROSE_STORY_GATE',
  'do_not_repeat':['D01_E91_E120_DRAFTING','D01_FINAL_REGRESSION','D01_FOUNDER_LOCK','D01_E121_GENERATION']
}


def _replace_d01_entry(items):
    out=[]
    found=False
    for x in items:
        if x.startswith('D01_'):
            if not found: out.append(D01_LOCK); found=True
        else: out.append(x)
    if not found: out.append(D01_LOCK)
    return out


def patch_system(d):
    pf=d['portfolio_frontier']
    pf['text_locked_or_text_complete']=_replace_d01_entry(pf['text_locked_or_text_complete'])
    pf['active_project']=dict(SMITH)
    d['recent_verified_main_integration']=[
        x for x in d.get('recent_verified_main_integration',[])
        if x not in {'CENTRAL_ROUTER_REBASED_TO_D01_WORKING_FRONTIER','D01_E96_WORKING_FRONTIER_PERSISTED_TO_DRIVE_AND_PR85_BRANCH'}
    ]
    for x in ['D01_FOUNDER_STORY_LOCK_AND_RECORDING_AUTHORITY','D01_E01_E120_CURRENT_STATE_ROUTED']:
        if x not in d['recent_verified_main_integration']: d['recent_verified_main_integration'].append(x)
    d['state_status']='D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120; SMITH_NEXT_FRESH_AUTHORITY_RECONCILIATION_BEFORE_PROSE; D09_PENDING_FOUNDER_LOCK; NO_D10_E25; ENGINE_V11_2_MACHINE_EXECUTION_ROUTED_VERIFIED'
    return d


def patch_portfolio(d):
    d['purpose']='Non-destructive portfolio-frontier overlay for CURRENT_IVDIVO_SYSTEM_STATE.json. Project-specific authority/state remains higher. D10 and D01 are Founder-locked; next portfolio production obligation is SMITH fresh authority/continuity reconciliation before prose.'
    d['text_complete_or_locked']=_replace_d01_entry(d['text_complete_or_locked'])
    d['d01_founder_lock']={
      'project_id':'D01','title':'THE WIFE AT HIS WEDDING','status':'FOUNDER_LOCKED',
      'locked_frontier':'E01-E120_STORY_TEXT','recording_authority':'ISSUED',
      'project_state':'PROJECTS/THE_WIFE_AT_HIS_WEDDING/CURRENT_STATE.md',
      'founder_lock_artifact_drive_id':'1eueZnnYaUGktaSXCcMIiOAUUcINmCTV6xATBdZ9B9UA',
      'final_story_gate_drive_id':'1C-VzyTORtauuDFZToJ4bx5Nic9dOwsrPfRudL3dAOcM',
      'season_regression_drive_id':'1-kXiIx3utxWTmIlPUuudiWVsXLfCHbBTOAADrrLrGF8',
      'reopen_rule':'ONLY_NEW_FATAL_MAJOR_EVIDENCE_OR_NEW_FOUNDER_INSTRUCTION'
    }
    d['active_project']=dict(SMITH)
    d['queue_after_d01_founder_lock']=[
      'IVDIVO_BOOK_3_SMITH_FRESH_AUTHORITY_RECONCILIATION_HUMAN_SCENE_DIALOGUE_CALIBRATION_COMPLETE_ARCHITECTURE_FULL_NOVEL_AND_LOCK',
      'IVDIVO_BOOK_4_AFTER_BOOK_3_CONSEQUENCES_LOCK','WHOLE_PORTFOLIO_TEXT_LOCK_AUDIT','AUDIO_NOVEL_STUDIO_BATCH_INGEST_AND_PRODUCTION'
    ]
    d['state_status']='D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED; SMITH_NEXT_FRESH_AUTHORITY_RECONCILIATION_BEFORE_PROSE; D09_READY_FOR_FOUNDER_LOCK_DECISION'
    return d


def main():
    s=patch_system(json.loads(SYSTEM.read_text()))
    p=patch_portfolio(json.loads(PORTFOLIO.read_text()))
    (OUT/SYSTEM.name).write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
    (OUT/PORTFOLIO.name).write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
    print('PATCHED',SYSTEM.name,PORTFOLIO.name)

if __name__=='__main__': main()
