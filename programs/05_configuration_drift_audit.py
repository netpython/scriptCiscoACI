#!/usr/bin/env python3
"""Crée un snapshot canonique et compare la fabric avec une baseline JSON."""
from __future__ import annotations
import argparse, difflib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
p = parser('Dérive configuration ACI')
p.add_argument('--baseline', default='aci_baseline.json')
p.add_argument('--update-baseline', action='store_true')
a = p.parse_args()
classes = ('fvTenant', 'fvCtx', 'fvBD', 'fvAEPg', 'fvSubnet', 'vzBrCP', 'vzSubj', 'vzFilter', 'vzEntry', 'l3extOut', 'infraAttEntityP')
snapshot = {}
with APIC(config(a.config)) as apic:
    for cls in classes:
        snapshot[cls] = sorted(rows(apic.cls(cls)), key=lambda x: x.get('dn', ''))
for values in snapshot.values():
    for obj in values:
        for volatile in ('modTs', 'uid', 'status', 'lcOwn'):
            obj.pop(volatile, None)
current = json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False)
baseline = Path(a.baseline)
previous = baseline.read_text(encoding='utf-8') if baseline.exists() else ''
diff = '\n'.join(difflib.unified_diff(previous.splitlines(), current.splitlines(), fromfile='baseline', tofile='current', lineterm=''))
folder = OUTPUT / f'aci_drift_{stamp()}'
folder.mkdir()
(folder / 'snapshot.json').write_text(current, encoding='utf-8')
(folder / 'drift.diff').write_text(diff, encoding='utf-8')
summary = {'baseline_exists': bool(previous), 'changed': bool(previous and previous != current), 'diff_lines': len(diff.splitlines()), 'classes': {k: len(v) for k, v in snapshot.items()}}
(folder / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
if a.update_baseline or not baseline.exists():
    baseline.write_text(current, encoding='utf-8')
setup('aci_drift').info('Rapport: %s', folder)
