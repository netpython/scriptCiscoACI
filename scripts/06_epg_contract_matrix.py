#!/usr/bin/env python3
from common import *
log=setup("epg_contract_matrix");a=parser("Matrice EPG contrats").parse_args();result=[]
with APIC(config(a.config)) as apic:
 for cls,relation in (("fvRsProv","provider"),("fvRsCons","consumer")):
  for r in rows(apic.cls(cls)):
   if a.tenant and f"uni/tn-{a.tenant}/" not in r.get("dn",""):continue
   result.append({"tenant":a.tenant or "ALL","relation":relation,"epg_dn":r.get("dn","").rsplit("/rs",1)[0],"contract":r.get("tnVzBrCPName","")})
log.info("%s",write_csv("epg_contract_matrix",result))

