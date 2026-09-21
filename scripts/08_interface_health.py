#!/usr/bin/env python3
from common import *
log=setup("interfaces");a=parser("Santé interfaces").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("l1PhysIf","ethpmPhysIf"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("interface_health",result))

