# H2Bench

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Hydrogen · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $450 USD · **Difficulty:** 4 of 5

A teaching bench that splits water with a small electrolyzer, stores a few liters of hydrogen at low pressure and runs a fuel cell, with meters so students can measure efficiency at each step. Protected by H2Guard.

![H2Bench concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement HBN-DWG-001 (PDF)](cad/drawings/HBN-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Measuring electricity in, hydrogen made and electricity out gives students an honest sense of where hydrogen fits and where it does not. H2Bench works at tens of watts, large enough that meter and wiring errors do not swamp the result and small enough that the whole hydrogen inventory (about 7.9 L at up to 300 kPa gauge) could be released into a classroom without approaching a flammable mixture. A rigid buffer tank lets students count the hydrogen with the gas law, and the same pressure feeds the fuel cell without a compressor.

It is open and garage-buildable because the barrier for schools is cost and trust. A branded 12 W fuel cell stack alone costs more than the whole $450 bench budget, and a sealed kit cannot be inspected by a safety officer. Every part of H2Bench is off the shelf, the design files are under CERN-OHL-S-2.0, and its safety chain is the portfolio's own open H2Guard detector and interlock.

## Burning platform

Hydrogen is moving from strategy to construction faster than the people who can judge it are trained. Global hydrogen demand was almost 100 Mt in 2024, but low-emissions hydrogen was still less than 1 % of production, and installed water electrolysis capacity was only about 2 GW ([IEA, Global Hydrogen Review 2025](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)). The European Union alone aims to produce 10 Mt of renewable hydrogen a year by 2030 ([European Commission](https://energy.ec.europa.eu/topics/eus-energy-system/hydrogen_en)).

The workforce to build this is short: more than half of 700 energy companies surveyed by the IEA report critical hiring bottlenecks ([IEA, 2025](https://www.iea.org/news/energy-employment-has-surged-but-growing-skills-shortages-threaten-future-momentum)). And the key number every student should leave with is sobering: converting electricity to hydrogen and back with fuel cells returns only 27.4 to 48 % of the energy ([Oxford Institute for Energy Studies, 2025](https://www.oxfordenergy.org/wpcms/wp-content/uploads/2025/07/ET48-Power-to-Hydrogen-to-Power.pdf)). H2Bench lets them measure it.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Secondary and vocational schools | A practical that follows one packet of energy from electricity to hydrogen and back, with students calculating each efficiency |
| Hydrogen technician training | Safe-handling drills on real hardware: purge, leak check, interlock test and shutdown |
| Universities | Electrochemistry and energy labs: polarization curves, Faraday efficiency, gas law and uncertainty analysis |
| Energy utilities and project developers | Induction training for staff moving from gas, power or oil into hydrogen projects |
| Science centers and outreach | Supervised demonstrations of hydrogen production and use, with a visible lamp load |
| Public sector and policy training | Showing decision makers the measured round-trip loss behind hydrogen storage proposals |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| European Union | Targets 10 Mt of domestic renewable hydrogen and 10 Mt of imports a year by 2030 ([European Commission](https://energy.ec.europa.eu/topics/eus-energy-system/hydrogen_en)), which needs technicians across member states. |
| United States | The DOE Hydrogen Program names teachers and students as target audiences and notes "a general lack of awareness of hydrogen as an energy alternative" ([US DOE](https://www.hydrogen.energy.gov/program-areas/education)). |
| India | The National Green Hydrogen Mission targets 5 Mt a year by 2030 and projects over 600,000 jobs; about 5,600 people had been certified in hydrogen skills ([PIB, Government of India](https://www.pib.gov.in/PressNoteDetails.aspx?id=155990&NoteId=155990&ModuleId=3)). |
| China | Holds 65 % of global installed electrolysis capacity ([IEA, 2025](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)), the largest base of electrolyzers that trained operators will run. |
| Chile | Its national strategy aims to produce the world's most cost-competitive green hydrogen by 2030 and to rank among the three leading exporters by 2040 ([IEA policy database](https://www.iea.org/policies/12973-national-strategy-for-green-hydrogen)). |
| Namibia | The Namibia University of Science and Technology has warned of a possible shortfall of 130,000 skilled green hydrogen workers by 2040 ([Ecofin Agency](https://www.ecofinagency.com/news-industry/2309-48927-skills-gap-threatens-namibia-s-green-hydrogen-ambitions-by-2040)). |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. A teaching rig is the second hydrogen project, built on H2Guard. The trigger in the wider world was the gap between announced hydrogen targets and the workforce behind them: the IEA's 2025 employment review found that energy companies face critical hiring bottlenecks and that newly qualified entrants would need to rise by 40 % by 2030 to close the skills gap ([IEA, 2025](https://www.iea.org/news/energy-employment-has-surged-but-growing-skills-shortages-threaten-future-momentum)).

## Problem

Students hear about the hydrogen economy but rarely measure it. Teaching kits are either toys or costly lab systems, and neither shows round-trip losses clearly. Branded 12 W fuel cell stacks alone list at about $480 to $580, and schools need detection and ventilation before they will host any hydrogen rig.

## Concept

A teaching bench that splits water with a small electrolyzer, stores a few liters of hydrogen at low pressure and runs a fuel cell, with meters so students can measure efficiency at each step. Protected by H2Guard.

In one lesson a 70 W PEM electrolyzer fills a 2 L tank from 70 to 300 kPa gauge in 17.7 min; a 12 W class fuel cell then runs a lamp at 10.8 W for 29.0 min. Students log every stage at 1 Hz and find a round trip of about 25 % (HHV basis), each stage measurable to within ±2 %. These are paper figures from the TRL 3 sizing note HBN-CAL-001, not measurements.

At TRL 3 the design meets nine of its sixteen requirements on paper. Cost and hydrogen purity at the fuel cell are not met, and the inventory at full relief lift, the H2Guard interlock, electrolyzer back-pressure and mass are at risk; see [docs/REVIEW.md](docs/REVIEW.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- PEM electrolyzer stack, about 70 W (under 100 W)
- 2 L buffer tank at up to 300 kPa gauge, with relief valve, pressure and temperature sensing (metal hydride and gasbag kept as options)
- PEM fuel cell, 12 W class (under 50 W), with regulator and solenoid valve
- Power meters on each stage, with a logger and display
- Water deionizer cartridge and reservoir
- H2Guard detector and interlock, sensing at the high point of a canopy hood
- Bench frame and canopy hood

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). Parts cost $865 ($800 without the bench power supply, H2Guard excluded), well above the $450 budget; a budget of about $850 is proposed, awaiting Amish. See [docs/REVIEW.md](docs/REVIEW.md).

## Safety

> Hydrogen is flammable from about 4 to 74 % in air and ignites very easily. Keep storage small and at low pressure (about 7.9 L at up to 300 kPa gauge), use only pressure parts rated 1 MPa or more, keep air out of the tank, and operate only with H2Guard active and under supervision. The power supply is mains powered; use an RCD or GFCI. Research and teaching use only; not certified laboratory equipment.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (HBN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `HBN-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
