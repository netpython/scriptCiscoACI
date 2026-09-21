#!/usr/bin/env python3
"""Détecte les EPG sans contrat, contrats trop ouverts et relations asymétriques."""
from __future__ import annotations
import re,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from common import *
log=setup("epg_contract_security");a=parser("Sécurité EPG/contrats").parse_args();findings=[]
with APIC(config(a.config)) as apic:
 epgs=rows(apic.cls("fvAEPg"));providers=rows(apic.cls("fvRsProv"));consumers=rows(apic.cls("fvRsCons"));entries=rows(apic.cls("vzEntry"))
relations=defaultdict(lambda:{"provider":set(),"consumer":set()})
for kind,data in (("provider",providers),("consumer",consumers)):
 for r in data:relations[r.get("dn","").rsplit("/rs",1)[0]][kind].add(r.get("tnVzBrCPName",""))
for e in epgs:
 dn=e.get("dn","");rel=relations[dn];issues=[]
 if not rel["provider"] and not rel["consumer"]:issues.append("NO_CONTRACT")
 findings.append({"epg":e.get("name"),"dn":dn,"providers":",".join(sorted(rel["provider"])),"consumers":",".join(sorted(rel["consumer"])),"severity":"WARNING" if issues else "OK","issues":",".join(issues)})
for x in entries:
 open_proto=x.get("prot") in {"unspecified","0",""};open_ports=x.get("dFromPort") in {"unspecified","0",""} and x.get("dToPort") in {"unspecified","0",""}
 if open_proto and open_ports:findings.append({"epg":"","dn":x.get("dn"),"severity":"CRITICAL","issues":"PERMIT_ANY_FILTER_ENTRY"})
log.info("%s",write_csv("epg_contract_security",findings))

