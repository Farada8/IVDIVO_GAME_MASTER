#!/usr/bin/env python3
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / 'CURRENT_IVDIVO_SYSTEM_STATE.json'
PORTFOLIO = ROOT / 'CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json'
PROJECT = ROOT / 'PROJECT_STATES' / 'IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json'
PROJECT_PATH = 'PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json'


def _active_from_project(project: dict) -> dict:
    if project.get('project_id') != 'IVDIVO_BOOK_3_SMITH':
        raise ValueError('UNEXPECTED_SMITH_PROJECT_ID')
    if not project.get('manuscript_frontier', {}).get('ch25_authorized'):
        raise ValueError('CH25_NOT_AUTHORIZED')
    nxt = project.get('next_obligation')
    if not nxt:
        raise ValueError('SMITH_NEXT_OBLIGATION_MISSING')
    return {
        'project_id': project['project_id'],
        'title': 'SMITH',
        'mode': project['status'],
        'project_state_path': PROJECT_PATH,
        'source_transition_from': 'PROJECTS/THE_WIFE_AT_HIS_WEDDING/CURRENT_STATE.md',
        'next_unblocked_obligation': nxt,
        'authority_boundary': 'PROJECT_SPECIFIC_SMITH_STATE_CONTROLS; DO_NOT_DRAFT_CH26_BEFORE_CH25_LOCAL_GATE',
        'do_not_repeat': list(project.get('do_not', [])),
    }


def patch_system(system: dict, project: dict) -> dict:
    out = copy.deepcopy(system)
    out['portfolio_frontier']['active_project'] = _active_from_project(project)
    marker = 'SMITH_CH24_PASS_CH25_AUTHORIZED_CURRENT_STATE_ROUTED'
    recent = list(out.get('recent_verified_main_integration', []))
    if marker not in recent:
        recent.append(marker)
    out['recent_verified_main_integration'] = recent
    out['state_status'] = (
        'D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120; '
        'SMITH_CH24_PASS_CH25_AUTHORIZED_NEXT_DRAFT_CH25_CASCADE; '
        'D09_PENDING_FOUNDER_LOCK; NO_D10_E25; ENGINE_V11_2_MACHINE_EXECUTION_ROUTED_VERIFIED'
    )
    return out


def patch_portfolio(portfolio: dict, project: dict) -> dict:
    out = copy.deepcopy(portfolio)
    out['purpose'] = (
        'Non-destructive portfolio-frontier overlay for CURRENT_IVDIVO_SYSTEM_STATE.json. '
        'Project-specific authority/state remains higher. D10 and D01 are Founder-locked; '
        'SMITH project-specific state is active through CH24 PASS with CH25 CASCADE authorized.'
    )
    out['active_project'] = _active_from_project(project)
    queue = list(out.get('queue_after_d01_founder_lock', []))
    if queue:
        queue[0] = 'IVDIVO_BOOK_3_SMITH_ACTIVE_CH24_PASS_CH25_AUTHORIZED'
    out['queue_after_d01_founder_lock'] = queue
    out['state_status'] = (
        'D10_FOUNDER_LOCKED; D01_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED; '
        'SMITH_CH24_PASS_CH25_AUTHORIZED_NEXT_DRAFT_CH25_CASCADE; '
        'D09_READY_FOR_FOUNDER_LOCK_DECISION'
    )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    system = json.loads(SYSTEM.read_text(encoding='utf-8'))
    portfolio = json.loads(PORTFOLIO.read_text(encoding='utf-8'))
    project = json.loads(PROJECT.read_text(encoding='utf-8'))
    (out_dir / SYSTEM.name).write_text(json.dumps(patch_system(system, project), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out_dir / PORTFOLIO.name).write_text(json.dumps(patch_portfolio(portfolio, project), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
