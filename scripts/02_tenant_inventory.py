#!/usr/bin/env python3
from common import *
log=setup("tenants");a=parser("Inventaire tenants").parse_args()
with APIC(config(a.config)) as apic:data=rows(apic.cls("fvTenant"))
log.info("%s",write_csv("tenants",data))

