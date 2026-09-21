#!/usr/bin/env python3
import time
from rich.console import Console
from rich.table import Table
from common import *
p=parser("Monitoring live faults");p.add_argument("--refresh",type=int,default=60);p.add_argument("--alerts-only",action="store_true");a=p.parse_args();cfg=config(a.config);console=Console()
try:
 with APIC(cfg) as apic:
  while True:
   data=rows(apic.cls("faultInst",{"query-target-filter":'ne(faultInst.severity,"cleared")'}));table=Table(title="ACI Active Faults")
   for c in ("Severity","Code","Description","DN","Last transition"):table.add_column(c)
   for r in data:table.add_row(r.get("severity",""),r.get("code",""),r.get("descr","")[:80],r.get("dn","")[:70],r.get("lastTransition",""))
   console.clear();console.print(table);console.print(f"Actualisation {a.refresh}s — Ctrl+C pour quitter");time.sleep(a.refresh)
except KeyboardInterrupt:console.print("[yellow]Monitoring arrêté proprement.[/yellow]")
