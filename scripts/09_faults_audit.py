#!/usr/bin/env python3
from common import *
log=setup("faults");a=parser("Audit faults").parse_args();cfg=config(a.config);allowed=set(cfg.get("fault_severities",["critical","major","minor"]))
with APIC(cfg) as apic:data=[r for r in rows(apic.cls("faultInst",{"query-target-filter":'ne(faultInst.severity,"cleared")'})) if r.get("severity") in allowed]
data.sort(key=lambda x:(x.get("severity",""),x.get("lastTransition","")),reverse=True);log.info("%s",write_csv("faults",data))

