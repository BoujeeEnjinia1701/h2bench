---
doc_id: HBN-PRC-001
title: H2Bench design precis
project: H2Bench
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
---

# H2Bench design precis

## Summary

H2Bench is a teaching bench that turns about 21 Wh of electricity into about 4.5 L of usable hydrogen in an 18 min fill, holds it in a 2 L tank at up to 300 kPa gauge, and returns about 5 Wh through a 12 W class fuel cell over about 29 min. Every stage is metered, so students measure a round-trip efficiency of about 25 % (estimate, HHV basis) from their own data and see where the other 75 % goes. The bench sits on an existing lab table under a canopy hood and runs only while the portfolio's H2Guard detector, extraction fan and interlock are active. All figures in this document are first-order estimates to be checked at TRL 3.

![Hero render](../media/hero.png)

*Figure 1. H2Bench on an existing lab table with a 1.75 m person for scale. Energy flows left to right: power supply, water, electrolyzer, gas treatment, buffer tank, regulator, fuel cell and lamp. Massing model.*

## How it works

A lesson runs in two halves.

1. **Fill (about 18 min).** The bench power supply (4) drives the PEM electrolyzer stack (6) in constant-current mode at about 9 A and 7.8 V. Deionized water from the reservoir (5) is split: oxygen vents into the hood, and hydrogen passes through the separator and drier (7), the check valve and flame arrestor (8), and into the buffer tank (9). The electrolyzer pushes the tank from 70 to 300 kPa gauge on its own; there is no compressor. Students log current, voltage, tank pressure and temperature, and compute the hydrogen made from the gas law and from Faraday's law. The difference is the Faraday efficiency.
2. **Discharge (about 29 min).** The solenoid valve and regulator (11) feed the fuel cell (12) at about 50 kPa gauge. The fuel cell runs the electronic load and lamp (13) at about 1.5 A. Students log power out and tank pressure fall, and plot the fuel cell's polarization curve by stepping the load.

The meters and logger (14) record every quantity at 1 Hz to a CSV file. The H2Guard sensor at the high point of the canopy hood (15) watches for hydrogen; on alarm it cuts the power supply output, closes the tank solenoid and runs the extraction fan at full speed.

![Energy flow](../media/flow.png)

*Figure 2. Energy per lesson cycle, HHV basis. All values are estimates: electrolyzer 72 % (voltage efficiency 76 %, Faraday efficiency 95 %), 2 % lost to leaks and venting in storage, fuel cell about 35 % net (0.60 V per cell, 95 % fuel utilization, 0.9 W fan and controls).*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 3.

| No. | Component | Function | Key figure (estimate) |
| --- | --- | --- | --- |
| 1 | Bench deck and extrusion frame | Carries everything, sits on the lab table | 900 x 450 mm |
| 2 | Instrument back panel | Printed energy-chain schematic; carries the meters | 570 mm tall |
| 3 | Canopy hood, duct and posts | Collects rising hydrogen at one point for sensing and extraction | 100 mm duct |
| 4 | Bench DC power supply | Constant-current drive for the electrolyzer | 0 to 30 V, 0 to 10 A |
| 5 | DI water reservoir and deionizer | Feed water at 1 µS/cm or less | About 3.4 g water used per fill |
| 6 | PEM electrolyzer stack | Splits water; pressurizes the tank | 4 cells, about 70 W, about 250 mL/min H2 |
| 7 | Gas and water separator, drier | Returns water; dries the hydrogen | Silica gel with indicator |
| 8 | Check valve and flame arrestor | Stops backflow and flame propagation into the stack | 7 kPa cracking pressure |
| 9 | Hydrogen buffer tank with guard | Stores the lesson's hydrogen | 2 L, 300 kPa gauge working, rated 1 MPa or more |
| 10 | Tank manifold | Pressure and temperature for the gas law; relief; gauge; manual vent | Relief at 350 kPa gauge |
| 11 | Regulator and solenoid valve | Feeds the fuel cell; closes on alarm or power loss | About 50 kPa gauge out |
| 12 | PEM fuel cell | Converts hydrogen back to electricity | 12 W class, 13 cells, about 146 mL/min H2 |
| 13 | Electronic load and lamp | Steps the load for polarization curves; shows the output | 0 to 3 A |
| 14 | Meters, logger and display | Three power monitors, pressure and temperature, CSV at 1 Hz | ±1 % power |
| 15 | H2Guard sensor, controller and fan | Detection, extraction and interlock (H2Guard project) | See H2Guard |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section looking from the front. The electrolyzer (6) shows its four membrane electrode assemblies between titanium plates; the buffer tank (9) is a thin-walled vessel with a domed top inside its rod guard. The power supply (4) is at the left and the fuel cell (12) at the right.*

## First-order numbers

Table 2. Energy and gas per lesson cycle (estimates).

| Quantity | Value | Assumption |
| --- | --- | --- |
| Electrolyzer input | 70 W for 17.7 min, 20.8 Wh | 4 cells, 1.95 V per cell, 9 A |
| Hydrogen produced | 0.189 mol, 4.5 L at 20 °C, 15.0 Wh (HHV) | Faraday efficiency 95 %; HHV 285.8 kJ/mol |
| Electrolyzer efficiency | About 72 % (HHV) | Voltage efficiency 1.48 V / 1.95 V = 76 % |
| Compression penalty | About 18 mV per cell, under 1 % | Electrochemical, 1 to 4 bar absolute on the H2 side |
| Tank content at 300 kPa gauge | 0.33 mol, 7.9 L at 20 °C, 0.66 g | 2.0 L at 401 kPa absolute, 20 °C |
| Usable swing | 300 down to 70 kPa gauge, 0.189 mol | Regulator needs about 20 kPa headroom above the fuel cell supply |
| Storage loss | About 2 %, 0.3 Wh | Leaks, purge of the lines; to be measured |
| Fuel cell output | 11.7 W gross, 10.8 W net, for about 29 min, 5.2 Wh | 13 cells at 0.60 V and 1.5 A; 95 % utilization; 0.9 W fan and controls |
| Fuel cell efficiency | About 35 % net (HHV), about 42 % (LHV) | Consistent with the 40 % system efficiency listed for the 12 W class ([Fuel Cell Store](https://www.fuelcellstore.com/horizon-12-watt-pem-fuel-cell)) |
| Round trip | About 25 % (HHV) | Near the low end of the 27.4 to 48 % range in [OIES (2025)](https://www.oxfordenergy.org/wpcms/wp-content/uploads/2025/07/ET48-Power-to-Hydrogen-to-Power.pdf), as expected at 12 W scale with a dead-end fuel cell |
| Heat released | About 20 W at the electrolyzer, about 20 W at the fuel cell | Losses in Figure 2 divided by run time |
| Oxygen vented | About 2.3 L per fill | Half the hydrogen moles |
| Total release into a 30 m³ room | About 0.03 % by volume, under 1 % of the 4 % lower flammable limit | Full 7.9 L, well mixed |
| Stored pressure energy | About 0.65 kJ | Isentropic expansion of 2 L from 401 to 101 kPa absolute |
| Stored chemical energy | About 94 kJ (HHV), 80 kJ (LHV) | 0.33 mol |
| Hydrogen measurement | About ±2 % | 0.25 % FS transducer on 600 kPa, ±1 K, tank volume calibrated by water fill to ±1 % |
| Parts cost | About $845, or $780 without the bench supply | `bom/bom.csv`; H2Guard excluded |

The numbers show that one 90 min lesson can hold a full cycle (R2), the inventory stays under 10 L (R5) and the round trip lands where published studies say it should, so the bench teaches the right lesson. They also show that cost (R14) is far from the $450 target.

## Key design choices

Each choice below is **proposed, awaiting Amish**. Decision records will go in [decisions/](decisions/) once decided.

1. **Storage: rigid 2 L buffer tank at up to 300 kPa gauge.** Options: (a) rigid tank, pressurized by the electrolyzer; (b) metal hydride canister (stores more at lower pressure, but slow, costly and hides the gas law); (c) near-atmospheric gasbag or water-displacement gas holder with a small pump to feed the fuel cell. Recommendation: (a), because the fuel cell needs about 45 to 55 kPa gauge supply ([Fuel Cell Store](https://www.fuelcellstore.com/horizon-12-watt-pem-fuel-cell)) and pressure and temperature give students a direct measurement of the hydrogen. Condition: the electrolyzer must be rated for the back-pressure (R10); if not, fall back to (c).
2. **PEM electrolysis with deionized water, not alkaline.** Alkaline cells are cheaper but need potassium hydroxide, a caustic electrolyte. Recommendation: PEM for student safety.
3. **Generic 12 W class fuel cell rather than a branded stack.** A branded 12 W stack costs $482 to $576; a generic stack is estimated at about $250 but its purity tolerance and polarization data must be obtained. Recommendation: generic, with a published polarization curve as a purchase condition; branded as the fallback.
4. **Measure hydrogen by pressure, volume and temperature, not by a mass flow meter.** It is cheaper, and the gas law is itself a lesson. A mass flow meter could be an upgrade for university labs.
5. **Bench power supply in constant-current mode as the source.** A small solar panel could be added later to show renewable-to-hydrogen; not in the first version.
6. **H2Guard as a hard dependency, costed in its own project.** The bench cannot run without it. Whether a school kit should include it in the price is a pitch-level choice.
7. **Tank kept above about 20 kPa gauge between lessons** so air cannot enter; a new or opened tank is purged with hydrogen by pressure cycling before first use (three fill and vent cycles to 300 kPa gauge reduce the air fraction to about 1.6 %).
8. **Canopy hood with a single high point** so the sensor sees any leak first and the fan extracts it.
9. **Budget.** See `docs/REVIEW.md`: the parts cost is about $845 against $450.

## Safety

> **Safety:** Hydrogen is flammable in air from about 4 to 74 % by volume and ignites with about 0.02 mJ, far less than most fuels; its flame is hard to see in daylight ([US DOE](https://www1.eere.energy.gov/hydrogenandfuelcells/pdfs/h2_safety_fsheet.pdf)). H2Bench is a research and teaching prototype, not certified laboratory equipment. Run it only under supervision, only with the H2Guard detector, fan and interlock active and tested, and never near open flames, heaters or sparking tools.

> **Safety:** The tank and lines are under pressure (up to 300 kPa gauge, relief at 350 kPa gauge). Use only vessels and fittings rated 1 MPa or more and rated for hydrogen; never use plastic bottles. Keep the tank inside its guard, pipe the relief valve and manual vent into the hood, and never open a fitting while the system is pressurized.

> **Safety:** Keep air out of the tank. A hydrogen and air mixture inside a closed vessel can burn or detonate. Purge a new or opened tank with hydrogen by pressure cycling, and never vent it below about 20 kPa gauge.

> **Safety:** The oxygen outlet of the electrolyzer must vent to the hood, away from the hydrogen outlet, so oxygen and hydrogen can never mix in a line.

> **Safety:** The bench power supply is mains powered. Use a supply with a protective earth, keep the mains lead off the wet deck, and fit a residual-current device (RCD or GFCI) on the bench socket. Water and electricity share the deck; keep the reservoir below and away from the supply.

> **Safety:** The electrolyzer and fuel cell stacks run warm (about 20 W of heat each) and the fuel cell's maximum stack temperature is about 55 °C. Allow cooling before handling.

## Open questions

- [ ] Can a generic electrolyzer stack at this size hold 300 kPa gauge on the hydrogen side with the oxygen side at atmospheric pressure (R10)?
- [ ] What hydrogen purity reaches the fuel cell after the separator and drier, and does the chosen fuel cell tolerate it (R9)?
- [ ] H2Guard alarm set point and response time; how the interlock reaches the power supply output and the solenoid (R8).
- [ ] Tank: aluminium or stainless; which certified vessel type is easiest for schools to approve?
- [ ] Is a 300 kPa gauge tank acceptable to school safety officers, or is option (c) (near-atmospheric storage with a pump) needed?
- [ ] Which curriculum and age group to align the first worksheets with?
- [ ] How to bring the cost toward $450 (see REVIEW.md).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
