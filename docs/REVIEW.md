# Review note: H2Bench

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (HBN-DDR-001 v0.1): the eight TRL 2 recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review, and the items that stay open.
- `docs/04-calcs/01-sizing.md` (HBN-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: electrolyzer and fill, inventory and pressure, fuel cell, energy balance, measurement uncertainty, hood and venting, interlock, water and drier, envelope and mass, cost and logging, with a results table for R1 to R16. The script reads the tank and bench dimensions from the model and the prices from the BOM.
- `cad/src/model.py`: parametric build123d model (frame, deck, back panel, canopy with duct, supply, reservoir, 4-cell electrolyzer with membranes and ports, separator and drier, arrestor, 2.000 L tank sized from its volume parameter with guard, manifold with relief and vent needle valve, regulator and solenoid, 75 x 47 x 70 mm fuel cell, load, meters, H2Guard stand-in, 6 mm gas lines). Exports `cad/step/` and `cad/stl/` (assembly, frame and hood, tank module, electrolyzer); clash check finds no overlaps.
- `cad/src/sheets.py` and `cad/drawings/HBN-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". HBN-DWG-001 was free because the concept blueprint uses HBN-DWG-010.
- `bom/bom.csv` (18 lines, all priced with a supplier type) and `bom/bom-notes.md`. Line 18 (plug-in 30 mA RCD, $20) is new; lines 6, 10, 12 and 16 were updated.
- `cad/src/concept_media.py` now builds from `model.py`; all media regenerated (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`), checked by eye, and the temporary `media/_views*` folders deleted. The kit's cutaway cuts at the mean Y of all parts, which missed the gas train, so the script renders its own cutaway on the gas train centreline.
- `docs/01-problem.md`, `docs/02-concept.md` and `docs/03-requirements.md` moved to v0.3 with the adopted choices, HBN-CAL-001 numbers and a status column from the CAL.
- `project.yaml`: trl 3, trl_target 3, trl_evidence updated; `budget_usd`, pitch and problem unchanged. `README.md`: TRL badge, links, Concept numbers and cost line.

### Requirements (HBN-CAL-001)

Nine met, two not met, four at risk, one not verifiable at TRL 3.

| ID | Result | Status |
| --- | --- | --- |
| R9 | Oxygen crossover unknown, no deoxidizer; fuel cell listing asks for 99.995 % | **Not met** |
| R14 | $865 full, $800 without the bench supply, $780 minimum; against $450 (and $850 proposed) | **Not met** |
| R5 | 9.6 L at the relief setting, but 10.5 L at full relief lift on a 15 °C day | At risk |
| R8 | 1.1 s trip to valve closed from H2Guard's TRL 2 figures; 24 V and 12 V valve mismatch | At risk |
| R10 | Stack must hold 357 kPa over the O2 side at the relief setting; no rating in hand | At risk |
| R13 | 900 x 450 x 755 mm, but 25.2 kg against 25 kg (22.2 kg without the supply) | At risk |
| R16 | Vent 3.0 min; setup needs hardware | Not verifiable at TRL 3 |
| R1, R2, R3, R4, R7 | ±1.8 % worst stage; 46.7 min cycle; 70.2 W; 10.8 W net; 0.8 % LFL in 30 m³ | Met |
| R6, R11, R12, R15 | Pressure ratings, water quality, logging, guard | Met (design review) |

Corrections to TRL 2 numbers: the 7.9 L "at the relief setting" was the tank alone at 300 kPa gauge; with the lines it is 9.6 L at the relief setting and 10.5 L at full lift. Mass rises from about 18 to 25.2 kg. Cost rises from $845 to $865 with the RCD line. The fuel cell's 146 mL/min was the reacted flow; it draws 154 mL/min. Bench height is 755 mm, not about 770 mm. R10's 300 kPa target does not cover a relief lift (357 kPa needed). R4 has only a 0.8 W margin.

Key numbers: 70.2 W electrolyzer, 256 mL/min, 17.7 min fill of 0.189 mol (4.5 L); 10.8 W net fuel cell for 29.0 min, 5.2 Wh; round trip 25.1 % (HHV); 646 J stored pressure energy at 300 kPa gauge; hydrogen per fill measured to ±1.5 %; drier lasts about 110 fills.

### Decisions recorded (HBN-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: rigid 2 L tank at up to 300 kPa gauge (gasbag with pump as the fallback if R10 fails); PEM, not alkaline; generic 12 W class fuel cell with a polarization curve as a purchase condition; hydrogen measured by pressure, volume and temperature; bench supply in constant-current mode as the source; H2Guard costed in its own project and shipped with the bench (applied to the R14 scope); tank kept above 20 kPa gauge with pressure-cycle purging; vocational technician training as the first users. No pitch or problem rewording was recommended, so none was applied.

### Still awaiting Amish

- **Budget:** about $850 recommended at TRL 2; `budget_usd` stays $450. The full kit is $865, $15 over even the recommended figure; without the bench supply it is $800.
- Whether the bench power supply is in the kit (BOM line 4).
- Canopy hood with a single high point (not in the TRL 2 review list, so not adopted; kept as the working design).
- Curriculum alignment, class demonstration or group practical first, and aluminium or stainless tank (no recommendation made).
- Engineering proposals from this session: relief at 325 kPa gauge (329 kPa gauge or less keeps R5 at full lift); a 310 kPa gauge cut of the supply so the relief valve is a backup; vent needle valve set for 3 min or more; plug-in RCD line.
- Mass (R13): accept 25.2 kg, carry the supply separately, or use a 10 mm deck (saves 0.77 kg).

### Cross-repo notes (H2Guard, not edited)

H2Guard is not one of the batch's shared components, but H2Bench depends on it, so its REVIEW.md and documents were read. Consistent: H2Guard's trip to valve closed within 2 s (HGD-REQ-001 R4) matches R8, and its inventory rule (300 L for 30 m³) is met thirtyfold. Conflicts to resolve with H2Guard: (1) its valve is a 24 V normally closed part, while H2Bench's tank solenoid is 12 V; (2) it is not stated which H2Guard output breaks H2Bench's 9 A DC supply line; (3) H2Guard models its fan as a 150 m³/h room exhaust, while H2Bench assumes 60 m³/h through its canopy duct; (4) H2Guard recommends a university teaching lab as first user, H2Bench vocational training.

### Safety concerns

- Hydrogen is flammable from 4 to 74 % with a 0.02 mJ ignition energy and a nearly invisible flame; the bench must never run without H2Guard detection, extraction and interlock.
- Venting a full tank faster than about 90 s can raise the duct concentration past H2Guard's warning; the needle valve is set for 3 min or more.
- At the relief setting the tank holds 776 J of pressure energy; only 1 MPa rated metal parts, guard in place.
- The relief lift loads the electrolyzer membrane to 357 to 392 kPa; an unrated stack could fail and mix hydrogen into the oxygen side. The 310 kPa gauge supply cut is proposed.
- Oxygen crossover also puts some oxygen into the stored hydrogen; far below a flammable mixture, but unquantified.
- Mains supply near water: RCD (line 18) and earthed supply. Warm stacks: about 20 W of heat each. Users under 18 only under supervision.
- Research and teaching prototype, not certified laboratory equipment.

### Other notes

- No TRL 4 material exists (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created.
- Citations checked with WebFetch on 2026-09-25: the Fuel Cell Store 12 W listing (7.8 V at 1.5 A, 13 cells, 0.45 to 0.55 bar, 99.995 %, 0.18 L/min, 40 %, 55 °C, 5 to 30 °C, 275 g, $576) and the Ecofin Namibia report (130,000 workers by 2040, attributed to the NUST vice-chancellor; still a news report of a statement, not a study). The MSE listing confirms a single-cell 300 mL/min stack at $1,396.95 but states no output pressure, so the TRL 2 claim "up to about 0.4 MPa" was removed from HBN-PRB-001. Generic stack prices (BOM lines 6 and 12) remain unverified estimates.
- The `model.py` assemblies copy each shape, because a build123d shape can have only one parent compound; without this the STEP export and drawing silently lost parts.

### Recommended next step

TRL 4 is on hold by Amish's instruction, so the next step is a review, not a build: Amish to decide the budget (and whether the supply is in the kit), confirm or reject the relief, supply-cut and RCD proposals, and settle the H2Guard interface points with that project. For the record only, TRL 4 would need a named electrolyzer with a back-pressure rating of at least 357 kPa and an oxygen-in-hydrogen figure, fuel cell supplier acceptance of the gas, an H2Guard design at TRL 3 with a defined interlock output, a lab test report (TST, environment: lab) and build log entries.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (HBN-PRB-001 v0.2): problem with cited sources, users, operating environment, constraints, out of scope, prior work and open questions. No co-design checklist existed, so none was kept.
- `docs/03-requirements.md` (HBN-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, estimated status and assumptions.
- `docs/02-concept.md` (HBN-PRC-001 v0.2): lesson sequence, 15 numbered components, energy and gas balance, nine proposed design choices, safety section and open questions.
- `cad/src/concept_media.py`: massing model of the bench (15 BOM parts, plus the electrolyzer cell block shown as unnumbered parts) on an existing lab table, with a 1.75 m person placed on the floor as a context part.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` with callouts 1 to 15, `cutaway.png` (electrolyzer membranes and hollow tank), and `flow.png` (energy per lesson, all values labeled estimates).
- `bom/bom.csv`: 17 rows, numbered to match the exploded view (rows 16 and 17 are not modeled), with indicative USD prices; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, both "Where it could be used" tables and "What sparked the idea" expanded with cited figures; Problem, Concept, Key components and Safety brought in line with the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` is unchanged. The pitch ("a few liters of hydrogen at low pressure") and problem remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Electrolyzer input | About 70 W (4 cells, 9 A) | R3 met |
| Fill time, 70 to 300 kPa gauge | About 18 min, 20.8 Wh in | R2 met |
| Hydrogen made per fill | 0.189 mol, about 4.5 L, 15.0 Wh (HHV) | |
| Electrolyzer efficiency | About 72 % (HHV) | |
| Tank inventory at 300 kPa gauge | About 7.9 L, 0.66 g | R5 met |
| Fuel cell | About 10.8 W net for about 29 min, 5.2 Wh | R4 met |
| Round trip | About 25 % (HHV basis) | Near the low end of the published 27.4 to 48 % range |
| Full release into a 30 m³ room | About 0.03 % by volume, under 1 % of LFL | R7 met |
| Hydrogen measurement uncertainty | About ±2 % | R1 expected met |
| Bench size and mass | 900 x 450 mm, about 770 mm tall, about 18 kg | R13 met |
| Parts cost (H2Guard excluded) | About $845, or about $780 without the bench supply | **R14 not met** |

Requirements not met or at risk:

- **R14 (cost) not met:** about $845 against $450. The two stacks (about $400 together) and the pressure parts drive the cost.
- **R9 (hydrogen purity) not met on paper:** the 12 W class fuel cell specifies 99.995 % or better; the purity after the separator and drier is unknown.
- **R10 (electrolyzer back-pressure) at risk:** a generic stack must be confirmed to hold 300 kPa gauge on the hydrogen side.
- **R8 (interlock) at risk:** depends on H2Guard, whose README is still at scaffold stage; set point and response time are not yet defined.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to about $850 (bench power supply included, H2Guard costed separately); (b) keep $450 as the bench-only cost with both stacks bought separately by the school; (c) shrink to a 5 W class fuel cell and a smaller electrolyzer, which cuts cost but weakens the measurements. Recommendation: (a). `project.yaml` is unchanged.
2. **Storage method.** Rigid 2 L tank at up to 300 kPa gauge (recommended), metal hydride canister, or near-atmospheric gasbag with a pump.
3. **PEM rather than alkaline electrolysis** (recommended, for student safety).
4. **Fuel cell source.** Generic 12 W class stack with a published polarization curve (recommended) or a branded stack at $482 to $576.
5. **Hydrogen measured by pressure, volume and temperature** rather than a mass flow meter (recommended).
6. **Bench power supply as the source**, with solar as a later option (recommended).
7. **H2Guard included in the kit price or not.** Recommendation: cost it separately but ship the two together.
8. **Tank kept above about 20 kPa gauge between lessons** with pressure-cycle purging of a new tank (recommended).
9. **First users.** Vocational technician training or secondary school practical first; recommendation: vocational training, where supervision and safety culture are stronger.

### Safety concerns

- Flammable gas with a very low ignition energy and a nearly invisible flame; the bench must never run without H2Guard detection, extraction and interlock.
- Pressure: 2 L at up to 300 kPa gauge (about 0.65 kJ of stored pressure energy); only rated metal vessels and fittings, relief at 350 kPa gauge piped into the hood, tank guard.
- Air ingress into the tank could form a flammable mixture inside a closed vessel; purge and minimum-pressure rules are part of the design.
- Oxygen and hydrogen outlets must stay separate.
- Mains-powered supply near water: earthed supply, RCD or GFCI, reservoir kept away from the supply.
- Warm stacks (about 20 W of heat each, fuel cell stack limit about 55 °C).
- Users include students under 18: supervised use only, with teacher-held control of the power supply.

### Problems and notes

- H2Guard's README is still the scaffold. H2Bench cites only what it states (sensor, relay controller, spark-free fan, normally closed supply valve, alarm). The interlock outputs H2Bench needs (power supply cut, tank solenoid close) should be confirmed with that project.
- Generic stack prices (items 6 and 12) could not be verified from a primary source; they are marked as estimates in the BOM.
- The Namibia figure in the README comes from a news report of a university statement, not a published study.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1, 2 and 9. If approved, run `/advance-trl3` to check the energy, gas law, uncertainty and release calculations in a CAL note, confirm electrolyzer back-pressure and purity with suppliers, and produce the parametric model and drawing sheet. The design is not ready for TRL 4.
