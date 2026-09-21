#!/usr/bin/env python3
from common import *
log=setup("epg_inventory");a=parser("Inventaire applications et EPG").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("fvAp","fvAEPg"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("applications_epgs",result))

