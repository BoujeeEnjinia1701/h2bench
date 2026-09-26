---
doc_id: HBN-DDR-002
title: H2Bench recommendations accepted
project: H2Bench
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($885)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item in Table 1 is "Decided by Amish, 2026-09-25: go with recommendation"; items without a recommendation (Table 2) remain open.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists every item in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in HBN-DDR-001 that carried a recommendation, now decided, and what changed in the repo. Items without a recommendation stay "Proposed, awaiting Amish". Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, and `trl` and `trl_target` stay at 3.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3), HBN-DDR-001 and HBN-CAL-001 v0.1.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Storage (DDR-001 item 1) | Rigid 2 L tank at up to 300 kPa gauge; gasbag with pump as the fallback if R10 fails | Wording only (HBN-PRC-001 v0.4, HBN-DDR-001 v0.2) |
| D2 | Electrolysis type (item 2) | PEM with deionized water, not alkaline | Wording only |
| D3 | Fuel cell source (item 3) | Generic 12 W class stack with a published polarization curve as a purchase condition; branded stack as the fallback | Wording only |
| D4 | Hydrogen measurement (item 4) | Pressure, volume and temperature, not a mass flow meter | Wording only |
| D5 | Source (item 5) | Bench power supply in constant-current mode; solar later | Wording only |
| D6 | H2Guard cost scope (item 6) | Costed in its own project, shipped with the bench | Wording only (already in R14 scope) |
| D7 | Tank minimum pressure (item 7) | Kept above about 20 kPa gauge; new tank purged by three pressure cycles | Wording only |
| D8 | Canopy hood (item 11), proposed as the working design | Canopy hood with a single high point for sensing and extraction | Wording only (already in the model) |
| D9 | Budget (item 9) | Recommendation (a): raise `budget_usd` to about $850, bench supply included, H2Guard costed separately | `project.yaml` `budget_usd` $450 to $850; R14 restated as $850 including the supply (HBN-REQ-001 v0.4); README, HBN-PRB-001 v0.4, HBN-PRC-001 v0.4, BOM notes and HBN-CAL-001 v0.2 updated. The kit is $885, so R14 is still not met, by $35 |
| D10 | Bench power supply in the kit (item 10) | In the kit, as D9 states | BOM line 4 note; R14 scope |
| D11 | Relief valve setting (item 13) | 325 kPa gauge (was 350) | `bom/bom.csv` line 10; HBN-CAL-001 v0.2: inventory at full relief lift and 15 °C 10.5 L to 9.9 L, R5 at risk to met; at the relief setting 9.6 L to 9.0 L; stored pressure energy at the relief setting 776 J to 710 J; room release 0.032 % to 0.030 % by volume. HBN-DWG-001 Rev P1 to P2 notes |
| D12 | High-pressure supply cut (item 13) | Pressure switch opens at 310 kPa gauge and a relay breaks the electrolyzer supply; the relief valve is a backup only | `cad/src/model.py`: cut switch added to the manifold (item 10); STEP and STL re-exported; HBN-DWG-001 Rev P2; media regenerated. BOM line 10 $45 to $60 (switch), line 14 $30 to $35 (relay): total $865 to $885. Mass 25.2 to 25.3 kg. R10 restated from 300 kPa to 332 kPa (relief setting plus check valve); membrane load at the relief setting 357 to 332 kPa, 317 kPa at the cut. The cut is hardwired; no firmware rule is needed |
| D13 | Vent needle valve (item 13) | Set so venting 300 to 20 kPa gauge takes 3 min or more | Wording only (already in the design) |
| D14 | Plug-in 30 mA RCD (item 13) | Keep as BOM line 18 | Wording only (already in the BOM) |
| D15 | H2Guard interface (item 14) | Settle the valve voltage, the output that breaks the 9 A supply line, the hood extraction rate and the first user with the H2Guard project | Listed under cross-repo actions in `docs/REVIEW.md`; H2Guard not edited. R8 stays at risk |

No pitch or problem rewording was recommended, so the pitch and problem lines in `project.yaml` and `README.md` are unchanged; the README cost line now states the $850 budget.

### Items still open

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Curriculum and age group for the first worksheets. No recommendation was made | Proposed, awaiting Amish |
| O2 | Class demonstration or group practical first. No recommendation was made | Proposed, awaiting Amish |
| O3 | Aluminium or stainless tank. No recommendation was made | Proposed, awaiting Amish |
| O4 | Mass (R13, 25.3 kg against 25 kg): accept, carry the supply separately, or use a 10 mm deck (saves 0.77 kg). No recommendation was made | Proposed, awaiting Amish |
| O5 | Cost (R14, $885 against $850): where to find $35. No recommendation was made | Decided by Amish, 2026-09-26: budget set to $885 (see below) |

## Consequences

- Requirement status (HBN-CAL-001 v0.2): met 10 (was 9), not met 2 (R9 purity, R14 cost), at risk 3 (was 4: R8, R10, R13), not verifiable at TRL 3 1 (R16).
- Documents bumped: HBN-PRB-001 v0.4, HBN-PRC-001 v0.4, HBN-REQ-001 v0.4, HBN-CAL-001 v0.2, HBN-DDR-001 v0.2; drawing HBN-DWG-001 Rev P2.
- Cross-repo action: settle the interlock interface with H2Guard (D15). Not edited here.
- TRL 4 work (building the bench, supplier confirmation of back-pressure and purity, purchasing, lab tests, firmware beyond a sketch) remains on hold.

## Budget approved, 2026-09-26

On 2026-09-26 Amish wrote, in chat: "i approve all the budget items."

- Budget set to $885 to cover the priced BOM: decided by Amish, 2026-09-26. This settles O5. The 18-line BOM is $885 with the bench supply (H2Guard excluded), so R14 moves from not met to met, with no margin.
- Requirement status (HBN-CAL-001 v0.3): met 11, not met 1 (R9 purity), at risk 3 (R8, R10, R13), not verifiable at TRL 3 1 (R16).
- Files changed: `project.yaml` (`budget_usd` 850 to 885); HBN-REQ-001 v0.5; HBN-CAL-001 v0.3, `docs/04-calcs/sizing.py` (hard-coded budget 850 to 885) and `results.csv`; HBN-PRB-001 v0.5 and HBN-PRC-001 v0.5 (budget figure); `README.md`; `bom/bom-notes.md`; `docs/REVIEW.md`.
