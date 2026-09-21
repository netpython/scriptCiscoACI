#!/usr/bin/env python3
from common import *
log=setup("endpoints");a=parser("Endpoints ACI").parse_args()
with APIC(config(a.config)) as apic:data=rows(apic.cls("fvCEp"))
log.info("%s",write_csv("endpoints",data))

