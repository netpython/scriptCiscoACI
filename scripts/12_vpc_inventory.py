#!/usr/bin/env python3
from common import *
log=setup("vpc");a=parser("Inventaire vPC").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("fabricExplicitGEp","fabricNodePEp","vpcDom"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("vpc_inventory",result))

