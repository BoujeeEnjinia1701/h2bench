---
doc_id: HBN-DEC-001
title: H2Bench design decisions register
project: H2Bench
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from REVIEW.md, HBN-DDR-001 to 003 and the build plan work
---

# H2Bench design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Decisions still to be made.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction: accept the changes that make the bench buildable (frame joints, four posts and a top frame, mounts, water lines, guard of threaded rods) | Accept as made; ask for changes | Accept | The whole build plan | HBN-DDR-003, Table 1 |
| 2 | Mass (R13, 25 kg or less): the constructable bench is 28.0 kg with the bench supply. Replaces HBN-DDR-002 O4 | (a) carry the supply separately (25.0 kg); (b) also a 10 mm deck (24.2 kg); (c) raise R13 to 30 kg; (d) a lighter top frame of 15 x 15 mm extrusion (saves about 0.6 kg) | (a) and (b) together | Deck thickness (build plan section 3.2); what ships with the bench | HBN-DDR-003, A1 |
| 3 | Separator water returned by hand (drain valve opened at 20 kPa gauge, water poured back) instead of a plumbed return | (a) by hand; (b) plumbed return with a needle valve and float trap | (a) for the prototype | Separator fittings (section 3.10) | HBN-DDR-003, A2 |
| 4 | Hydrogen purity at the fuel cell (R9, not met): oxygen crossover from the stack is unknown and there is no deoxidizer | (a) ask the stack supplier for the oxygen content and the fuel cell supplier to accept it; (b) add a catalytic deoxidizer before the drier; (c) run with the purge set high and accept faster fuel cell ageing | (a) first, (b) if the figures do not close | A deoxidizer would add one line part between separator and drier | HBN-CAL-001 section 8, HBN-REQ-001 R9 |
| 5 | H2Guard interface (R8, at risk): valve voltage (H2Guard 24 V, the H2Bench tank solenoid 12 V), which H2Guard output breaks the 9 A supply line, hood extraction (60 m³/h here, 150 m³/h room exhaust in H2Guard), first user | Settle with the H2Guard project; or fit a 24 V solenoid here | Settle with H2Guard (decided as an action in HBN-DDR-002 D15; the choices themselves are still open) | Solenoid coil voltage; interlock wiring (build plan wiring diagram) | HBN-DDR-002 D15, REVIEW.md |
| 6 | Tank material | Aluminium; stainless steel | No recommendation made | Tank part and mass | HBN-DDR-002 O3 |
| 7 | Curriculum and age group for the first worksheets | Open | No recommendation made | Not part of the build | HBN-DDR-002 O1 |
| 8 | Class demonstration or group practical first | Open | No recommendation made | Not part of the build | HBN-DDR-002 O2 |

## To confirm when parts are bought

*Table 2. Things to check on the real parts.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The electrolyzer's hydrogen side is rated to 332 kPa or more over its oxygen side | R10; if not, the decided fallback (a gasbag with a pump) applies | HBN-DDR-002 D1, HBN-CAL-001 section 2 |
| 2 | The electrolyzer's end plates have two tapped mounting holes on each end face, about 50 mm apart and about 10 mm above the base, or the maker's own feet | The feet bolt there; otherwise the feet change | HBN-DDR-003 P7 |
| 3 | The electrolyzer's water inlet and oxygen outlet are on one end plate, inlet low and outlet high | The water lines are routed for that | HBN-DDR-003 P6 |
| 4 | The separator and drier are rated 1 MPa or more | They sit at tank pressure | HBN-PRC-001 safety notes |
| 5 | The tank is 110 mm across or less, stands on a flat base, and its neck thread suits the manifold adapter | The cradle pocket is 112 mm; the manifold screws into the neck | HBN-DDR-003 P10 |
| 6 | The fuel cell's mounting holes, and its hydrogen inlet on the side facing the regulator | The bridge top is drilled to suit | HBN-DDR-003 P11 |
| 7 | The panel meters' and display's cut-out sizes | The panel cut-outs are 80 x 50 mm and 230 x 100 mm | Build plan section 3.5 |
| 8 | The reservoir has a low side outlet and a vented lid; the deionizer cartridge takes 6 mm push-in or compression fittings | The water lines connect there | HBN-DDR-003 P6 |
| 9 | The 100 mm flanged duct collar fits the H2Guard fan | The fan sits on the spigot | HBN-DDR-003 P4 |
| 10 | The extrusion, brackets and T-nuts are all one 20-series system (6 mm slot) | Mixed systems do not fit | HBN-DDR-003 P1 |

## Value engineering

Value-engineering target: USD 885 (a hypothetical control target, not a limit; `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 999 (USD 114 over the target). Without the bench power supply it is USD 934 (USD 49 over), and USD 914 where the bench socket is already RCD protected (USD 29 over). H2Guard is costed in its own project.

Main cost drivers:

- The two stacks: electrolyzer USD 155 and fuel cell USD 253 with their mounts, 41 % of the total.
- The frame, deck, hood and panel (BOM lines 1 to 3): USD 140, of which the construction changes added USD 45.
- The pressure parts: tank and guard USD 70, manifold USD 60, regulator and solenoid USD 40.

Savings worth trying:

- Let the school supply the bench power supply and use an RCD-protected socket: USD 85.
- Ask stack makers for an education bundle of electrolyzer and fuel cell: the two stacks are the largest single cost.
- Build the top frame and posts from plain 20 x 20 mm aluminium square tube with screwed corner plates instead of slotted extrusion and brackets: perhaps USD 20 to 30, at some cost to adjustability.
- Buy fittings, tubing and fasteners as one kit from a single gas-equipment supplier rather than line by line.

## Decisions made

*Table 3. Decisions made, newest first.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit; cost is reported as over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | STANDARDS section 18; this register |
| 2026-09-30 | Make the design buildable while drawing the build plan; keep open decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | HBN-DDR-003 (open for review, item 1 above) |
| 2026-09-26 | Budget of USD 885 to cover the priced BOM (now the value-engineering target) | Amish: "i approve all the budget items." | HBN-DDR-002, budget section |
| 2026-09-25 | Relief valve at 325 kPa gauge; pressure switch cuts the supply at 310 kPa gauge; vent needle valve 3 min or more; plug-in 30 mA RCD | Amish: "i accept all your recommendations, go with them across all repos." | HBN-DDR-002 D11 to D14 |
| 2026-09-25 | Budget raised to about USD 850 with the bench supply in the kit; H2Guard costed in its own project and shipped with the bench | Amish, same instruction | HBN-DDR-002 D6, D9, D10 |
| 2026-09-25 | Rigid 2 L tank at up to 300 kPa gauge (gasbag with a pump as the fallback if R10 fails); PEM with deionized water; generic 12 W class fuel cell; hydrogen measured by pressure, volume and temperature; bench supply in constant-current mode | Amish, same instruction | HBN-DDR-001 items 1 to 5, HBN-DDR-002 D1 to D5 |
| 2026-09-25 | Tank kept above about 20 kPa gauge, new tank purged by three pressure cycles; canopy hood with a single high point; vocational technician training as the first users | Amish, same instruction | HBN-DDR-001 items 7, 8, 11; HBN-DDR-002 D7, D8 |
| 2026-09-25 | Settle the interlock interface with the H2Guard project | Amish, same instruction | HBN-DDR-002 D15 (the choices are open item 5 above) |
