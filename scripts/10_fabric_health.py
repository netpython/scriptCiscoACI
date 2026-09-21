#!/usr/bin/env python3
from common import *
log=setup("fabric_health");a=parser("Santé fabric").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("fabricHealthTotal","healthInst"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("fabric_health",result))

