#!/usr/bin/env python3
from common import *
log=setup("fabric_inventory");a=parser("Inventaire fabric").parse_args()
with APIC(config(a.config)) as apic:data=rows(apic.cls("fabricNode"))
data.sort(key=lambda x:(x.get("role",""),x.get("id","")));log.info("%s",write_csv("fabric_inventory",data))

