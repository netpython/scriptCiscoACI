#!/usr/bin/env python3
from common import *
log=setup("contracts");a=parser("Contrats ACI").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("vzBrCP","vzSubj","vzFilter","vzEntry"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("contracts",result))

