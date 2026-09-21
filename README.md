# scriptCiscoACI

15 scripts Python en lecture seule pour auditer et documenter une fabric Cisco ACI via l'API REST APIC.

| # | Script | Fonction |
|---|---|---|
| 01 | `01_fabric_inventory.py` | Inventaire APIC, spine et leaf |
| 02 | `02_tenant_inventory.py` | Tenants, descriptions et état |
| 03 | `03_vrf_bd_inventory.py` | VRF, Bridge Domains et subnets |
| 04 | `04_epg_inventory.py` | Applications et EPG |
| 05 | `05_contract_inventory.py` | Contrats, subjects et filters |
| 06 | `06_epg_contract_matrix.py` | Matrice EPG provider/consumer |
| 07 | `07_endpoint_inventory.py` | Endpoints MAC/IP/EPG/leaf |
| 08 | `08_interface_health.py` | État et erreurs des interfaces physiques |
| 09 | `09_faults_audit.py` | Faults critiques, majeures et mineures |
| 10 | `10_fabric_health.py` | Santé globale et par objet |
| 11 | `11_l3out_inventory.py` | L3Out, nœuds et interfaces logiques |
| 12 | `12_vpc_inventory.py` | Domaines et protections vPC |
| 13 | `13_domains_aaep_inventory.py` | Domaines physiques/VMM et AAEP |
| 14 | `14_config_snapshot.py` | Snapshot JSON des objets essentiels |
| 15 | `15_live_fault_monitor.py` | Monitoring live des faults actifs |

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yml config.yml
export APIC_URL='https://apic.example.com'
export APIC_USERNAME='admin'
export APIC_PASSWORD='mot-de-passe'
```

## Exemples

```bash
python scripts/01_fabric_inventory.py
python scripts/06_epg_contract_matrix.py --tenant PROD
python scripts/09_faults_audit.py
python scripts/15_live_fault_monitor.py --refresh 60 --alerts-only
```

Tous les scripts sont en lecture seule. Les sorties sont enregistrées dans `outputs/`. Les structures MIT et certains attributs peuvent varier selon la version APIC : valider sur une fabric de test avant usage en production.

## Licence

MIT.

