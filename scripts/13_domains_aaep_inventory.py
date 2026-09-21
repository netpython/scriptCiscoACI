#!/usr/bin/env python3
from common import *
log=setup("domains_aaep");a=parser("Domaines et AAEP").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("physDomP","vmmDomP","infraAttEntityP"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("domains_aaep",result))

