#!/usr/bin/env python3
"""Audit état physique, erreurs, descriptions et rattachement aux policies."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
log = setup('interface_policy_compliance')
a = parser('Conformité interfaces ACI').parse_args()
result = []
with APIC(config(a.config)) as apic:
    phys = {r.get('dn'): r for r in rows(apic.cls('l1PhysIf'))}
    oper = rows(apic.cls('ethpmPhysIf'))
    errors = rows(apic.cls('rmonEtherStats'))
errmap = {r.get('dn', '').split('/dbgEtherStats')[0]: r for r in errors}
for r in oper:
    dn = r.get('dn', '').replace('/phys', '')
    base = next((p for p in phys.values() if p.get('id') and p.get('id') in dn), {})
    err = next((e for k, e in errmap.items() if k in dn), {})
    issues = []
    if r.get('operSt') != 'up':
        issues.append('OPER_DOWN')
    if not base.get('descr'):
        issues.append('NO_DESCRIPTION')
    error_total = sum((int(err.get(k) or 0) for k in ('rXErrors', 'tXErrors', 'cRCAlignErrors', 'undersizePkts', 'oversizePkts') if str(err.get(k) or '0').isdigit()))
    if error_total:
        issues.append('PHYSICAL_ERRORS')
    result.append({'dn': dn, 'interface': base.get('id'), 'description': base.get('descr'), 'admin_state': base.get('adminSt'), 'oper_state': r.get('operSt'), 'speed': r.get('operSpeed'), 'error_total': error_total, 'severity': 'CRITICAL' if 'PHYSICAL_ERRORS' in issues else 'WARNING' if issues else 'OK', 'issues': ','.join(issues)})
log.info('%s', write_csv('interface_policy_compliance', result))
