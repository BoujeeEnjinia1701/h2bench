---
doc_id: HBN-REQ-001
title: H2Bench requirements
project: H2Bench
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with first-order status
---

# H2Bench requirements

These are first-pass requirements for the concept. Targets are proposals for review. The status column gives the first-order estimate from HBN-PRC-001; every "met" is an estimate to be checked by calculation at TRL 3 and by test later. Two requirements are **not met** (R9 and R14) and two are at risk (R8 and R10).

Table 1. Requirements.

| ID | Requirement | Target | Status (estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Measure the efficiency of each stage | Electrolyzer, storage, fuel cell and round trip, each to within ±5 % relative | Expected met: power to ±1 %, hydrogen quantity to about ±2 % by pressure and temperature | Uncertainty calculation (CAL) |
| R2 | Complete a full cycle in one lesson | Fill and discharge within 60 min of run time | Met: about 18 min fill plus about 29 min discharge | Energy and flow calculation |
| R3 | Electrolyzer power | 100 W or less electrical input | Met: about 70 W | Stack datasheet |
| R4 | Fuel cell power | 50 W or less; 10 W or more net to run a visible load | Met: about 11 W net | Stack datasheet |
| R5 | Limit the hydrogen inventory | 10 L or less at 20 °C and 101.3 kPa | Met: about 7.9 L (0.66 g) at the relief setting | Gas law calculation |
| R6 | Limit storage pressure | Working pressure 300 kPa gauge or less; relief at 350 kPa gauge or less; vessel rated 1 MPa or more | Met by design | Component ratings |
| R7 | No flammable mixture in the room from a total release | Full inventory mixed into a 30 m³ room below 25 % of the lower flammable limit | Met: about 0.03 % by volume, under 1 % of LFL | Calculation |
| R8 | Interlock shuts down on a leak | H2Guard alarm cuts electrolyzer power and closes the tank solenoid within 2 s; fan runs | At risk: depends on H2Guard, not yet specified | H2Guard design review |
| R9 | Hydrogen quality at the fuel cell | Purity as the stack requires (the 12 W class specifies 99.995 % or better) | **Not met on paper:** electrolyzer purity after the drier is not yet known | Supplier data, later gas test |
| R10 | Electrolyzer tolerates tank back-pressure | H2 side rated to 300 kPa gauge or more over the O2 side | At risk: must be confirmed for the chosen stack | Supplier data |
| R11 | Water quality | Conductivity 1 µS/cm or less at the stack inlet, shown to students | Met by design (mixed-bed resin and conductivity check) | Datasheet |
| R12 | Log data students can analyze | Voltage, current, power, tank pressure and temperature at 1 Hz, saved as CSV | Met by design | Firmware sketch review |
| R13 | Fit an existing lab bench | Footprint 1,000 x 500 mm or less; height 800 mm or less; mass 25 kg or less | Met: 900 x 450 mm, about 770 mm, about 18 kg (estimate) | Massing model |
| R14 | Low cost and buildable | Parts cost $450 or less, excluding H2Guard; hand tools only; no welding | **Not met:** about $845 (about $780 without the bench supply) | Priced BOM |
| R15 | Guard people from pressure parts | Tank inside a guard; relief and vent piped to the hood; no pressurized fitting that can be opened without a tool | Met by design | Design review |
| R16 | Set up and shut down quickly | Setup 15 min or less; tank vented and bench safe in 5 min or less | Expected met | Walk-through at TRL 3 |

## Assumptions

- Electrolyzer: 4 cells at about 1.95 V and 9 A, Faraday efficiency 95 %; hydrogen higher heating value (HHV) 285.8 kJ/mol.
- Tank: 2.0 L internal, filled from 70 to 300 kPa gauge (171 to 401 kPa absolute) at 20 °C; below 70 kPa gauge the regulator cannot hold the fuel cell supply.
- Fuel cell: 13 cells at 0.60 V and 1.5 A, fuel utilization 95 % (the rest purged), about 0.9 W for fan and controls.
- Room: 30 m³, well mixed. The canopy hood exists because mixing near the leak is not instant; see HBN-PRC-001.
- Round-trip figures use the HHV basis. On a lower heating value (LHV) basis the hydrogen energy is about 15 % lower and the fuel cell efficiency correspondingly higher.
