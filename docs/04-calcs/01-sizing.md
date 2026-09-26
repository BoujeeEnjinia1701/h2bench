---
doc_id: HBN-CAL-001
title: H2Bench sizing calculations
project: H2Bench
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (electrolyzer and fill, inventory and pressure, fuel cell, energy balance, measurement uncertainty, hood and venting, interlock, water and drier, envelope and mass, cost, logging)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($885); R14 from not met to met
---

# H2Bench sizing calculations

On paper, H2Bench meets eleven of its sixteen requirements. **One is not met**: hydrogen purity at the fuel cell (R9), because electrolyzer oxygen crossover is unknown and there is no deoxidizer. Cost (R14) is met with no margin: the kit is $885, and on 2026-09-26 Amish approved a `budget_usd` of $885 to cover the priced BOM (HBN-DDR-002). **Three are at risk**: the H2Guard interlock (R8), electrolyzer back-pressure (R10, now 332 kPa) and mass (R13, 25.3 kg against 25 kg). Version 0.2 applies the decisions Amish accepted on 2026-09-25 (HBN-DDR-002): the relief valve moves from 350 to 325 kPa gauge, which brings R5 from at risk to met (full-lift inventory 10.5 L to 9.9 L); a pressure switch cuts the electrolyzer supply at 310 kPa gauge, so the relief valve is a backup only; and `budget_usd` rises from $450 to $850 with the bench supply in the kit. The switch and its relay add $20 and 0.15 kg. Setup time (R16) needs hardware to verify. The TRL 2 energy numbers hold: a 17.7 min fill and a 29.0 min discharge return 5.2 Wh of 20.8 Wh, a round trip of 25.1 % on the HHV basis, and students can measure each stage to within 1.8 %.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the tank and bench dimensions from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Gas constants | R = 8.314 J/(mol K), F = 96,485 C/mol, 24.05 L/mol at 20 °C and 101.3 kPa; H2 HHV 285.83 kJ/mol, LHV 241.83 kJ/mol, γ = 1.41 | Standard values; ideal gas, with a 0.24 % compressibility correction noted at 400 kPa absolute |
| Electrolyzer | 4 cells, 1.95 V per cell, 9 A, Faraday efficiency 95 %; 2.20 V per cell at end of life | HBN-PRC-001; generic 56 cm² class cells |
| Tank | 2.000 L internal (inner radius 52 mm, 200.8 mm straight, hemispherical top), 3 mm aluminium wall | `cad/src/model.py` |
| Gas volume outside the tank at tank pressure | 0.15 L (separator headspace, drier, lines) | Estimate |
| Pressures | Fill 70 to 300 kPa gauge; supply cut by a pressure switch at 310 kPa gauge; relief 325 kPa gauge with 10 % overpressure at full lift; check valve 7 kPa; kept at 20 kPa gauge overnight | HBN-PRC-001 v0.4, HBN-DDR-002, typical relief valve |
| Temperatures | Lab 20 °C; coldest 15 °C; separator gas 25 °C | HBN-PRB-001 |
| Storage loss | 2 % of the hydrogen made per cycle | Estimate, to be measured |
| Fuel cell | 13 cells, 0.60 V at 1.5 A (7.8 V, 11.7 W), fuel utilization 95 %, 0.9 W fan and controls; 0.18 L/min at full output; 45 to 55 kPa gauge supply; 99.995 % purity | Listing for the 12 W class ([Fuel Cell Store](https://www.fuelcellstore.com/horizon-12-watt-pem-fuel-cell), checked 2026-09-25) |
| Measurement | Transducer 0.25 % of 600 kPa full scale; thermistor ±1 K; tank volume ±1 % by water fill; power ±1 % | HBN-REQ-001 R1 |
| Room and hood | 30 m³ room; 60 m³/h through the canopy duct | Assumed hood share of H2Guard's 150 m³/h continuous exhaust (HGD-PRC-001) |
| H2Guard | Warning 0.4 % vol (10 % LFL), trip 1.0 % vol (25 % LFL); trip to valve closed 1.1 s | HGD-REQ-001 R2 to R4, HGD-PRC-001 (TRL 2 estimates) |
| Drier | 50 g silica gel, 10 % usable water uptake | Typical indicating gel at low humidity |
| Budget | $885 in `project.yaml` (was $450, then $850), bench supply included, H2Guard excluded | HBN-DDR-002; $885 approved by Amish on 2026-09-26 |

## 2. Electrolyzer and fill (R2, R3, R10)

The stack draws 7.8 V x 9 A = **70.2 W** (79 W with aged cells at 2.20 V), inside the 100 W limit (R3) and the 30 V, 10 A supply. Faraday's law gives 1.772 x 10⁻⁴ mol/s, or **256 mL/min** at 20 °C. Filling the 2.000 L tank from 70 to 300 kPa gauge takes 0.1887 mol (4.54 L at 20 °C and 101.3 kPa), so the fill lasts **1,065 s (17.7 min)** and uses **20.77 Wh**. The hydrogen holds 14.99 Wh (HHV): an electrolyzer efficiency of **72.2 %** (voltage efficiency 75.9 %, Faraday efficiency 95 %). The stack gives off about 19.5 W of heat.

The electrolyzer compresses its own hydrogen. The Nernst term at 300 kPa gauge is **17.4 mV per cell**, 0.89 % of the cell voltage, so no compressor is needed.

**Back-pressure (R10).** The membrane must hold the tank pressure plus the check valve cracking pressure over the oxygen side: **307 kPa** in normal filling and **317 kPa** at the 310 kPa gauge supply cut. The supply cut stops the stack before the relief valve can lift, so the relief is a backup only; if the cut failed, the membrane would see **332 kPa** at the 325 kPa gauge relief setting and 365 kPa at full lift. R10 is restated as 332 kPa or more (HBN-REQ-001 v0.4, was 300 kPa). No generic stack rating is in hand. At risk.

## 3. Inventory and pressure (R5, R6, R7)

*Table 2. Hydrogen held, expressed at 20 °C and 101.3 kPa.*

| State | Hydrogen |
| --- | --- |
| Tank at 300 kPa gauge | 0.3293 mol, 7.92 L, 0.664 g |
| Tank and lines at 300 kPa gauge | 8.52 L |
| Tank and lines at relief set, 325 kPa gauge | 9.05 L (9.20 L at 15 °C) |
| Tank and lines at full relief lift (358 kPa gauge) and 15 °C | **9.90 L** |

The TRL 2 note gave 7.9 L "at the relief setting"; that is the tank alone at the working pressure. With the relief at 350 kPa gauge (v0.1) the full-lift case on a cold day was 10.5 L. A relief set at 329 kPa gauge or less keeps even that case under 10 L, and 325 kPa gauge is now decided (HBN-DDR-002): 9.0 L at the relief set point and **9.9 L** at full lift and 15 °C. **R5 is met**, with a 0.1 L margin in the worst case.

**Pressure parts (R6).** Working 300 kPa gauge, supply cut 310 kPa gauge, relief 325 kPa gauge. The modeled vessel (110 mm outside diameter, 3 mm aluminium wall) has a hoop stress of 17.8 MPa at its 1 MPa rating and 71.3 MPa at four times that, against a 6061-T6 yield of 276 MPa. Stored pressure energy is **646 J** at 300 kPa gauge (710 J at the 325 kPa gauge relief setting), by isentropic expansion to atmosphere. Stored chemical energy is 94 kJ (HHV), 80 kJ (LHV). Met.

**Room release (R7).** The relief-set inventory mixed into a 30 m³ room gives **0.030 % by volume, 0.75 % of the lower flammable limit**; the worst case is 0.033 %. Met by a wide margin. H2Guard's proposed inventory rule (1 % of room volume, 300 L for 30 m³, HGD-REQ-001 R9) is met thirtyfold.

## 4. Fuel cell and discharge (R2, R4)

Thirteen cells at 0.60 V and 1.5 A give **11.7 W gross and 10.8 W net** after 0.9 W for the fan and controls, which meets R4 with a 0.8 W margin. At 0.58 V per cell the net is 10.4 W; at 0.55 V it falls to 9.8 W, below target. The stack reacts 146 mL/min and, at 95 % utilization, draws **154 mL/min**, inside the listed 0.18 L/min at full output. (The TRL 2 table's 146 mL/min was the reacted flow.)

After 2 % storage loss, 0.1850 mol is available, which runs the fuel cell for **1,739 s (29.0 min)** and delivers **5.22 Wh**. Net fuel cell efficiency is 35.5 % (HHV) or 42.0 % (LHV), consistent with the 40 % system efficiency listed for the 12 W class. About 18.7 W of heat and purge loss leaves the stack. The full cycle runs for **46.7 min**, inside the 60 min of R2. Met.

## 5. Energy balance

*Table 3. Energy per lesson cycle, HHV basis. These values drive `media/flow.png`.*

| Stage | Energy | Loss |
| --- | --- | --- |
| Electricity in | 20.8 Wh | |
| Hydrogen made | 15.0 Wh | Electrolyzer heat 5.8 Wh |
| After storage | 14.7 Wh | Leaks and purges 0.3 Wh |
| Fuel cell net DC | 5.2 Wh | Fuel cell heat, purge and fan 9.5 Wh |

The round trip is **25.1 %** (HHV basis), just below the 27.4 to 48 % range published for power-to-hydrogen-to-power ([Oxford Institute for Energy Studies, 2025](https://www.oxfordenergy.org/wpcms/wp-content/uploads/2025/07/ET48-Power-to-Hydrogen-to-Power.pdf)), as expected at 12 W scale. Each fill splits 3.40 g of water and vents 2.27 L of oxygen.

## 6. Measurement uncertainty (R1)

Hydrogen is counted from pressure and temperature before and after each stage: n = PV/(RT).

*Table 4. Standard uncertainty (k = 1) of the hydrogen made per fill.*

| Source | Contribution |
| --- | --- |
| Pressure, 1.5 kPa per reading, two readings | 0.92 % |
| Temperature, ±1 K, two readings | 0.65 % |
| Tank volume, ±1 % | 1.0 % |
| Combined | **1.51 %** |

The thermistor is bonded to the tank wall, so the gas temperature matters. During the fill the flow work into the tank heats the gas about 0.95 K above the wall, and the gas settles to the wall with a 15 s time constant; readings are taken 2 min after the fill ends. With power measured to ±1 %, the stage efficiencies carry: electrolyzer 1.8 %, storage 1.0 %, fuel cell 1.8 %, round trip 1.4 % and Faraday efficiency 1.8 %. All are within the ±5 % of R1. Met.

## 7. Hood, venting and interlock (R8, R15, R16)

**Hood.** At 60 m³/h (1,000 L/min) the 100 mm duct runs at 2.12 m/s. The electrolyzer's full output leaking into the hood gives only 0.026 % by volume at the duct. A leak must exceed 4.0 L/min to reach H2Guard's warning at the duct and 10 L/min to trip it. Small leaks are diluted by the extraction; the sensor at the high point catches large ones and a stopped fan (HGD-REQ-001 R5).

**Venting.** Venting the tank and lines from 300 to 20 kPa gauge releases 5.94 L. A needle valve set for 3.0 min (an effective orifice of about 0.16 mm) gives a peak of 3.50 L/min, or 0.35 % by volume at the duct (8.7 % of LFL), just under H2Guard's 0.4 % warning. At a constant flow, a vent shorter than 89 s would reach the warning. The end-of-day vent after a discharge (70 to 20 kPa gauge) is only 1.06 L. The 3.0 min vent meets the 5 min shutdown part of R16; setup time needs a walk-through with hardware, so **R16 is not verifiable at TRL 3**.

**Interlock (R8).** From H2Guard's TRL 2 figures, the trip reaches a closed valve and a dead supply in about 1.1 s (comparator and relay 0.1 s, solenoid 1.0 s), inside 2 s; the electrolyzer makes only 4.7 mL of hydrogen in that time. But H2Guard is itself at TRL 2, its valve is a 24 V part while H2Bench's tank solenoid is 12 V, and whether its relay can break the 9 A DC supply line is not specified. **At risk.**

**Guard (R15).** The rod guard clears the tank shell by 18 mm, and the relief and vent lines run to the canopy in the model. Met by design review.

## 8. Water, drier and purity (R9, R11)

Gas leaving the separator at 25 °C carries 0.79 to 1.85 % water vapour by mole, depending on tank pressure: about 0.045 g of water per fill. 50 g of silica gel at 10 % uptake lasts about **110 fills** before its color changes. The drier removes water, but PEM stacks also pass some oxygen across the membrane, and there is no deoxidizer. The fuel cell listing asks for 99.995 % or better. **R9 is not met** until the stack supplier states the oxygen content or the fuel cell supplier accepts the gas. Water quality (R11) is met by the mixed-bed resin and conductivity check.

## 9. Envelope and mass (R13)

The model's envelope above the lab table is **900 x 450 x 755 mm**, inside 1,000 x 500 x 800 mm.

*Table 5. Mass estimate.*

| Item | Mass (kg) |
| --- | --- |
| 1 Frame (3.6 m of 20 x 20 mm extrusion) and 12 mm HDPE deck | 1.80 + 4.62 |
| 2 Back panel, 3 mm aluminium composite | 1.95 |
| 3 Canopy, posts and duct collar | 1.89 |
| 4 Bench power supply | 3.00 |
| 5 Reservoir (filled) and deionizer | 0.80 |
| 6 Electrolyzer stack | 3.00 |
| 7 and 8 Separator, drier, check valve and arrestor | 0.70 |
| 9 Tank shell (from the model) and guard | 0.80 + 1.40 |
| 10 and 11 Manifold with cut switch, regulator and solenoid | 1.30 |
| 12 Fuel cell (275 g listed) with stand and controller | 0.50 |
| 13 and 14 Load, lamp, meters, display and cut relay | 0.75 |
| 15 H2Guard parts on the bench | 1.50 |
| 16 and 17 Tubing, wiring and hardware | 1.30 |
| Total | **25.3** (22.3 without the supply) |

The TRL 2 estimate of 18 kg was low; the HDPE deck and the electrolyzer dominate. At 25.3 kg against 25 kg (25.2 kg in v0.1; the cut switch and relay add 0.15 kg), **R13 is at risk**. It is met if the bench supply is carried separately, or with a 10 mm deck (saving about 0.8 kg); no option has been chosen (HBN-DDR-002, open).

## 10. Cost (R14)

The 18-line BOM totals **$885** (H2Guard excluded). Without the bench supply it is $820, and without the supply and the plug-in RCD (where the socket is already protected) $800. `budget_usd` is now $885 with the bench supply included, approved by Amish on 2026-09-26 to cover the priced BOM (HBN-DDR-002; it was $850, and $450 before that, against which the kit is $435 over). The full kit has **no margin**; the kit without the supply is $65 under. The two stacks are $400, 45 % of the total. **Met**, with no margin. The v0.1 total of $865 rises by $20 for the 310 kPa gauge pressure switch (line 10, $45 to $60) and its relay (line 14, $30 to $35).

## 11. Logging (R12)

One cycle is 2,804 s, so a 1 Hz log with 10 channels is 2,804 rows, about 224 kB of CSV. Met by design review.

## 12. Results

*Table 6. Results against HBN-REQ-001 v0.5. Written to `docs/04-calcs/results.csv`.*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R1 | Worst stage 1.8 % (hydrogen per fill 1.5 %, power 1 %) | Each stage within ±5 % relative | Met |
| R2 | 17.7 min fill + 29.0 min discharge = 46.7 min | 60 min or less | Met |
| R3 | 70.2 W (79 W with aged cells) | 100 W or less | Met |
| R4 | 10.8 W net (11.7 W gross); 9.8 W if cells fall to 0.55 V | 10 to 50 W | Met |
| R5 | 8.5 L at 300 kPa gauge; 9.0 L at relief set; 9.9 L at full relief lift and 15 °C | 10 L or less | Met |
| R6 | 300 kPa gauge working, relief 325 kPa gauge; hoop stress 18 MPa at 1 MPa | 300 and 350 kPa gauge or less; vessel 1 MPa or more | Met |
| R7 | 0.030 % by volume (0.8 % LFL); 0.033 % worst case | Below 25 % LFL in 30 m³ | Met |
| R8 | 1.1 s trip to valve closed, from H2Guard TRL 2 figures; 24 V and 12 V valve mismatch | Supply cut and solenoid closed within 2 s; fan runs | **At risk** |
| R9 | Water removed; oxygen crossover unknown; no deoxidizer | 99.995 % or better | **Not met** |
| R10 | Needs 307 kPa in filling, 317 kPa at the supply cut, 332 kPa at relief set; no rating in hand | 332 kPa or more over the O2 side | **At risk** |
| R11 | Mixed-bed resin with conductivity check; 3.4 g water per fill | 1 µS/cm or less | Met |
| R12 | 2,804 rows per cycle, about 224 kB | V, I, P, p and T at 1 Hz to CSV | Met |
| R13 | 900 x 450 x 755 mm; 25.3 kg (22.3 kg without the supply) | 1,000 x 500 mm, 800 mm, 25 kg or less | **At risk** |
| R14 | $885 full; $820 without the supply; $800 minimum (H2Guard excluded) | $885 or less, supply included | Met (no margin) |
| R15 | Guard clearance 18 mm; relief and vent piped to the canopy | Guard, piped relief, no tool-free fitting | Met |
| R16 | Vent 3.0 min; setup needs a walk-through with hardware | Setup 15 min or less; safe in 5 min or less | Not verifiable at TRL 3 |

## 13. Safety

> **Safety:** Hydrogen is flammable from about 4 to 74 % in air and ignites with about 0.02 mJ. These calculations bound the inventory (9.9 L worst case) and the concentration at the duct, but they do not replace H2Guard's detection and interlock, supervision, or a site risk assessment. H2Bench is a research and teaching prototype, not certified laboratory equipment.

> **Safety:** The tank and lines hold up to 710 J of pressure energy at the relief setting. The 310 kPa gauge supply cut keeps the relief valve as a backup; test the cut before each lesson series. Use only vessels and fittings rated 1 MPa or more for hydrogen, keep the guard in place and never open a pressurized fitting.

> **Safety:** Vent slowly. Venting a full tank in under about 90 s can raise the concentration at the duct past H2Guard's warning level; the needle valve is set for 3 min or more.
