#!/usr/bin/env python3
from common import *
log=setup("vrf_bd");a=parser("VRF, BD et subnets").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls in ("fvCtx","fvBD","fvSubnet"):
  for r in rows(apic.cls(cls)):r["objectClass"]=cls;result.append(r)
log.info("%s",write_csv("vrf_bd_subnets",result))

