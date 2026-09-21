#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,logging,os
from datetime import datetime
from pathlib import Path
from typing import Any
import requests,yaml
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/"outputs";LOGS=ROOT/"logs"
def setup(name):
 OUTPUT.mkdir(exist_ok=True);LOGS.mkdir(exist_ok=True);logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",handlers=[logging.FileHandler(LOGS/f"{name}.log"),logging.StreamHandler()]);return logging.getLogger(name)
def parser(text):
 p=argparse.ArgumentParser(description=text);p.add_argument("--tenant");p.add_argument("-c","--config",default="config.yml");return p
def config(path="config.yml"):
 p=Path(path);return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}
class APIC:
 def __init__(self,cfg):
  self.url=os.getenv("APIC_URL","").rstrip("/");self.user=os.getenv("APIC_USERNAME");self.password=os.getenv("APIC_PASSWORD");self.verify=os.getenv("APIC_VERIFY_SSL","false").lower()=="true";self.timeout=int(cfg.get("timeout",30));self.s=requests.Session()
  if not self.url or not self.user or not self.password:raise SystemExit("Définir APIC_URL, APIC_USERNAME et APIC_PASSWORD.")
  if not self.verify:disable_warnings(InsecureRequestWarning)
 def __enter__(self):
  r=self.s.post(f"{self.url}/api/aaaLogin.json",json={"aaaUser":{"attributes":{"name":self.user,"pwd":self.password}}},verify=self.verify,timeout=self.timeout);r.raise_for_status();return self
 def __exit__(self,*_):
  try:self.s.post(f"{self.url}/api/aaaLogout.json",json={"aaaUser":{"attributes":{"name":self.user}}},verify=self.verify,timeout=self.timeout)
  finally:self.s.close()
 def get(self,path,params=None):
  r=self.s.get(f"{self.url}{path}",params=params,verify=self.verify,timeout=self.timeout);r.raise_for_status();return r.json().get("imdata",[])
 def cls(self,name,params=None):return self.get(f"/api/node/class/{name}.json",params)
def attrs(item):
 obj=next(iter(item.values()));return obj.get("attributes",{})
def rows(items):return [attrs(x) for x in items]
def stamp():return datetime.now().strftime("%Y%m%d_%H%M%S")
def write_csv(name,data):
 path=OUTPUT/f"{name}_{stamp()}.csv";fields=sorted({k for r in data for k in r}) or ["result"]
 with path.open("w",newline="",encoding="utf-8-sig") as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(data)
 return path
def write_json(name,data):
 path=OUTPUT/f"{name}_{stamp()}.json";path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8");return path

