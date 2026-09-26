---
doc_id: HBN-DDR-001
title: H2Bench TRL 2 review decisions
project: H2Bench
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations for items 1 to 8 in Table 1 are adopted for TRL 3 work pending Amish's review; the items in Table 2 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed nine H2Bench design choices as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the H2Bench items one by one. This record therefore lists each recommendation as adopted for TRL 3 work, open for his review, and lists separately what stays open. Nothing here is recorded as approved. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and HBN-PRC-001. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| 1 | Storage: rigid 2 L buffer tank at up to 300 kPa gauge, pressurized by the electrolyzer; near-atmospheric gasbag with a pump stays the fallback if R10 cannot be met | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3, `cad/src/model.py`, HBN-CAL-001 section 3 |
| 2 | PEM electrolysis with deionized water, not alkaline | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3 |
| 3 | Generic 12 W class fuel cell with a published polarization curve as a purchase condition; branded stack as the fallback | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3, `bom/bom.csv` line 12 |
| 4 | Hydrogen measured by pressure, volume and temperature, not by a mass flow meter | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3, HBN-CAL-001 section 6 |
| 5 | Bench power supply in constant-current mode as the source; solar as a later option | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3 |
| 6 | H2Guard costed in its own project but shipped with H2Bench; the bench cannot run without it | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-REQ-001 v0.3 R14, `bom/bom.csv` line 15 |
| 7 | Tank kept above about 20 kPa gauge between lessons; a new or opened tank purged by three pressure cycles | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRC-001 v0.3, HBN-PRB-001 v0.3 |
| 8 | First users: vocational hydrogen technician training, ahead of secondary school practicals | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | HBN-PRB-001 v0.3 |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and `README.md` keep their pitch and problem lines.

### Items that remain open

*Table 2. Open items.*

| # | Item | Status |
| --- | --- | --- |
| 9 | Budget. The TRL 2 review recommended raising `budget_usd` from $450 to about $850 (bench power supply included, H2Guard costed separately). `budget_usd` stays at $450 in `project.yaml`. HBN-CAL-001 prices the kit at $865 in full, $800 without the bench supply and $780 without the supply and the plug-in RCD | Proposed, awaiting Amish. The $850 figure is a recommendation only |
| 10 | Whether the bench power supply is part of the kit or supplied by the school (BOM line 4) | Proposed, awaiting Amish (tied to item 9) |
| 11 | Canopy hood with a single high point for sensing and extraction (HBN-PRC-001 choice 8). It was not in the TRL 2 review list | Proposed, awaiting Amish. Kept in the model as the working design |
| 12 | Curriculum to align the first worksheets with; class demonstration or group practical first; aluminium or stainless tank | Proposed, awaiting Amish. No recommendation was made |
| 13 | Engineering proposals from HBN-CAL-001: relief set at 325 kPa gauge (329 kPa gauge or less keeps R5 at full relief lift); a 310 kPa gauge high-pressure cut of the supply so the relief valve is only a backup; vent needle valve set for 3 min or more; plug-in 30 mA RCD as BOM line 18 | Engineering proposals, awaiting Amish |
| 14 | H2Guard interface: H2Guard's valve is 24 V, normally closed; H2Bench's tank solenoid is 12 V. H2Guard's first-user recommendation (university teaching lab) differs from item 8 here | Raised in `docs/REVIEW.md`; H2Guard not edited |

## Consequences

- The design at TRL 3 is the rigid-tank, PEM, generic-stack bench measured by the gas law, as modeled in `cad/src/model.py` and drawn on HBN-DWG-001.
- Cost stays **not met** against the $450 in `project.yaml`, and the full kit is $15 over the recommended $850 until item 9 or 10 is decided.
- R10 (electrolyzer back-pressure) remains the condition for item 1; if no generic stack can be shown to hold 357 kPa over its oxygen side, the fallback in item 1 applies.
- The first-user choice (item 8) makes supervision by trained instructors the planning assumption; the worksheets for school use wait for item 12.
