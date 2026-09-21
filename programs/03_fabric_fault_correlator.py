#!/usr/bin/env python3
"""Corrèle faults par nœud, code, sévérité et objet impacté."""
from __future__ import annotations
import re, sys
from collections import Counter, defaultdict
from pathlib import Path
from openpyxl import Workbook
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import *
log = setup('fault_correlator')
a = parser('Corrélation faults ACI').parse_args()
cfg = config(a.config)
with APIC(cfg) as apic:
    faults = rows(apic.cls('faultInst', {'query-target-filter': 'ne(faultInst.severity,"cleared")'}))
details = []
groups = defaultdict(list)
for f in faults:
    node = (re.search('node-(\\d+)', f.get('dn', '')) or [None, 'fabric'])[1]
    key = (node, f.get('code'), f.get('severity'))
    groups[key].append(f)
    details.append({'node': node, 'code': f.get('code'), 'severity': f.get('severity'), 'description': f.get('descr'), 'dn': f.get('dn'), 'created': f.get('created'), 'last_transition': f.get('lastTransition')})
summary = [{'node': k[0], 'code': k[1], 'severity': k[2], 'count': len(v), 'sample': v[0].get('descr', '')} for k, v in groups.items()]
summary.sort(key=lambda x: x['count'], reverse=True)
wb = Workbook()
wb.remove(wb.active)
for title, data in (('Summary', summary), ('Faults', details)):
    ws = wb.create_sheet(title)
    headers = sorted({k for r in data for k in r}) or ['result']
    ws.append(headers)
    for r in data:
        ws.append([r.get(h, '') for h in headers])
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
path = OUTPUT / f'fault_correlator_{stamp()}.xlsx'
wb.save(path)
log.info('%s', path)
