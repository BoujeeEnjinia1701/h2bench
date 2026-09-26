---
doc_id: HBN-REQ-001
title: H2Bench requirements
project: H2Bench
doc_type: Requirements
version: "0.4"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from HBN-CAL-001; R14 scope states that H2Guard is costed in its own project (HBN-DDR-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# H2Bench requirements

These requirements were checked by calculation at TRL 3 in HBN-CAL-001 v0.2 (`docs/04-calcs/01-sizing.md`). Version 0.4 applies the decisions Amish accepted on 2026-09-25 (HBN-DDR-002): R14's limit is now the $850 `budget_usd` (was $450), with the bench power supply in the kit and H2Guard costed in its own project; R6 records the 325 kPa gauge relief and the 310 kPa gauge supply cut; and R10's target is restated from 300 kPa to 332 kPa, the relief setting plus the check valve, because a 300 kPa rating did not cover a relief event. Ten requirements are met on paper, **two are not met (R9 and R14)**, three are at risk (R8, R10 and R13) and one (R16) cannot be verified until hardware exists. "Met" means met by calculation or design review, not by test.

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Status (HBN-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Measure the efficiency of each stage | Electrolyzer, storage, fuel cell and round trip, each to within ±5 % relative | Met: hydrogen per fill ±1.5 %, worst stage ±1.8 % | Uncertainty calculation (HBN-CAL-001 section 6) |
| R2 | Complete a full cycle in one lesson | Fill and discharge within 60 min of run time | Met: 17.7 min fill plus 29.0 min discharge, 46.7 min | Energy and flow calculation |
| R3 | Electrolyzer power | 100 W or less electrical input | Met: 70.2 W (79 W with aged cells) | Calculation; stack datasheet later |
| R4 | Fuel cell power | 50 W or less; 10 W or more net to run a visible load | Met: 10.8 W net, a 0.8 W margin (9.8 W if cells fall to 0.55 V) | Calculation; stack datasheet later |
| R5 | Limit the hydrogen inventory | 10 L or less at 20 °C and 101.3 kPa | Met: 8.5 L at 300 kPa gauge, 9.0 L at the 325 kPa gauge relief setting, 9.9 L at full relief lift on a 15 °C day | Gas law calculation |
| R6 | Limit storage pressure | Working pressure 300 kPa gauge or less; electrolyzer supply cut at 310 kPa gauge; relief at 350 kPa gauge or less; vessel rated 1 MPa or more | Met by design: cut 310 kPa gauge, relief 325 kPa gauge; hoop stress 18 MPa at 1 MPa | Component ratings |
| R7 | No flammable mixture in the room from a total release | Full inventory mixed into a 30 m³ room below 25 % of the lower flammable limit | Met: 0.030 % by volume, 0.75 % of LFL | Calculation |
| R8 | Interlock shuts down on a leak | H2Guard alarm cuts electrolyzer power and closes the tank solenoid within 2 s; fan runs | **At risk:** 1.1 s from H2Guard's TRL 2 figures, but H2Guard is at TRL 2 and its valve is 24 V against H2Bench's 12 V solenoid | H2Guard design review |
| R9 | Hydrogen quality at the fuel cell | Purity as the stack requires (the 12 W class specifies 99.995 % or better) | **Not met:** water is removed by the drier, but oxygen crossover is unknown and there is no deoxidizer | Supplier data, later gas test |
| R10 | Electrolyzer tolerates tank back-pressure | H2 side rated to 332 kPa or more over the O2 side (relief setting plus check valve; was 300 kPa) | **At risk:** the stack must hold 307 kPa while filling, 317 kPa at the supply cut and 332 kPa at the relief setting; no rating in hand | Supplier data |
| R11 | Water quality | Conductivity 1 µS/cm or less at the stack inlet, shown to students | Met by design (mixed-bed resin and conductivity check) | Datasheet |
| R12 | Log data students can analyze | Voltage, current, power, tank pressure and temperature at 1 Hz, saved as CSV | Met by design: 2,804 rows, about 224 kB per cycle | Firmware sketch review |
| R13 | Fit an existing lab bench | Footprint 1,000 x 500 mm or less; height 800 mm or less; mass 25 kg or less | **At risk:** 900 x 450 x 755 mm, but 25.3 kg (22.3 kg without the bench supply) | Parametric model and mass estimate |
| R14 | Low cost and buildable | Parts cost $850 or less (`budget_usd`, was $450), including the bench power supply and excluding H2Guard, which is costed in its own project and shipped with the bench; hand tools only; no welding | **Not met:** $885, $35 over ($820 without the bench supply) | Priced BOM |
| R15 | Guard people from pressure parts | Tank inside a guard; relief and vent piped to the hood; no pressurized fitting that can be opened without a tool | Met by design: 18 mm guard clearance; lines to the canopy in the model | Design review |
| R16 | Set up and shut down quickly | Setup 15 min or less; tank vented and bench safe in 5 min or less | Not verifiable at TRL 3: the vent takes 3.0 min at the needle valve setting; setup needs a walk-through with hardware | Walk-through when hardware exists |

## Assumptions

- Electrolyzer: 4 cells at about 1.95 V and 9 A, Faraday efficiency 95 %; hydrogen higher heating value (HHV) 285.8 kJ/mol.
- Tank: 2.000 L internal plus 0.15 L of lines at tank pressure, filled from 70 to 300 kPa gauge (171 to 401 kPa absolute) at 20 °C; below 70 kPa gauge the regulator cannot hold the fuel cell supply. The full assumption list is in HBN-CAL-001 Table 1.
- Fuel cell: 13 cells at 0.60 V and 1.5 A, fuel utilization 95 % (the rest purged), about 0.9 W for fan and controls.
- Room: 30 m³, well mixed. The canopy hood exists because mixing near the leak is not instant; see HBN-PRC-001.
- Round-trip figures use the HHV basis. On a lower heating value (LHV) basis the hydrogen energy is about 15 % lower and the fuel cell efficiency correspondingly higher.
