#!/usr/bin/env python3
from common import *
log=setup("l3out");a=parser("Inventaire L3Out").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("l3extOut","l3extLNodeP","l3extLIfP","l3extRsNodeL3OutAtt","l3extRsPathL3OutAtt"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("l3out",result))

