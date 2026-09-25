# Review note: H2Bench

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
