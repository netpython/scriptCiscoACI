#!/usr/bin/env python3
from common import *
log=setup("snapshot");a=parser("Snapshot configuration").parse_args();classes=("fabricNode","fvTenant","fvCtx","fvBD","fvAEPg","vzBrCP","l3extOut","infraAttEntityP");snapshot={}
with APIC(config(a.config)) as apic:
 for cls in classes:snapshot[cls]=rows(apic.cls(cls))
log.info("%s",write_json("aci_snapshot",snapshot))

