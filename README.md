# H2Bench

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Hydrogen · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $450 USD · **Difficulty:** 4 of 5

A teaching bench that splits water with a small electrolyzer, stores a few liters of hydrogen at low pressure and runs a fuel cell, with meters so students can measure efficiency at each step. Protected by H2Guard.

## Concept rationale

Measuring electricity in, hydrogen made and electricity out gives students an honest sense of where hydrogen fits and where it does not.

## Burning platform

Countries are investing heavily in hydrogen and need technicians and engineers who understand it from first principles.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. A teaching rig is the second hydrogen project, built on H2Guard.

## Problem

Students hear about the hydrogen economy but rarely measure it. Teaching kits are either toys or costly lab systems, and neither shows round-trip losses clearly.

## Concept

A teaching bench that splits water with a small electrolyzer, stores a few liters of hydrogen at low pressure and runs a fuel cell, with meters so students can measure efficiency at each step. Protected by H2Guard.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- PEM electrolyzer stack, under 100 W
- Low-pressure metal hydride or gasbag storage
- PEM fuel cell, under 50 W
- Power meters on each stage
- Water deionizer cartridge
- H2Guard detector and interlock
- Bench frame and shield

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Hydrogen is flammable. Keep storage small and at low pressure, operate only with H2Guard active and under supervision. Research and teaching use only.

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
