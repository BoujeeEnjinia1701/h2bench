---
doc_id: HBN-DEC-001
title: H2Bench design decisions register
project: H2Bench
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from REVIEW.md, HBN-DDR-001 to 003 and the build plan work
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for open decisions 1 to 8 (2026-10-02); moved to decisions made (HBN-DDR-003 accepted)"
---

# H2Bench design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

- Letting the school supply the bench power supply (USD 85) would reverse HBN-DDR-002, D10; on 2026-10-02 the supply was kept in the kit, beside the bench, so this is not a saving to take. The "without the bench power supply" figures above do not compare like with like, because the USD 885 target was set with the supply included.
- Ask stack makers for an education bundle of electrolyzer and fuel cell: the two stacks are the largest single cost.
- Build the top frame and posts from plain 20 x 20 mm aluminium square tube with screwed corner plates instead of slotted extrusion and brackets: perhaps USD 20 to 30, at some cost to adjustability.
- Buy fittings, tubing and fasteners as one kit from a single gas-equipment supplier rather than line by line.

## Decisions made

*Table 3. Decisions made, newest first.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit; cost is reported as over or under it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | STANDARDS section 18; this register |
| 2026-09-30 | Make the design buildable while drawing the build plan; keep open decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | HBN-DDR-003 (accepted on 2026-10-02, below) |
| 2026-09-26 | Budget of USD 885 to cover the priced BOM (now the value-engineering target) | Amish: "i approve all the budget items." | HBN-DDR-002, budget section |
| 2026-09-25 | Relief valve at 325 kPa gauge; pressure switch cuts the supply at 310 kPa gauge; vent needle valve 3 min or more; plug-in 30 mA RCD | Amish: "i accept all your recommendations, go with them across all repos." | HBN-DDR-002 D11 to D14 |
| 2026-09-25 | Budget raised to about USD 850 with the bench supply in the kit; H2Guard costed in its own project and shipped with the bench | Amish, same instruction | HBN-DDR-002 D6, D9, D10 |
| 2026-09-25 | Rigid 2 L tank at up to 300 kPa gauge (gasbag with a pump as the fallback if R10 fails); PEM with deionized water; generic 12 W class fuel cell; hydrogen measured by pressure, volume and temperature; bench supply in constant-current mode | Amish, same instruction | HBN-DDR-001 items 1 to 5, HBN-DDR-002 D1 to D5 |
| 2026-09-25 | Tank kept above about 20 kPa gauge, new tank purged by three pressure cycles; canopy hood with a single high point; vocational technician training as the first users | Amish, same instruction | HBN-DDR-001 items 7, 8, 11; HBN-DDR-002 D7, D8 |
| 2026-09-25 | Settle the interlock interface with the H2Guard project | Amish, same instruction | HBN-DDR-002 D15 (the choices to propose were decided on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted as made: the changes P1 to P13 (frame joints, four posts and a top frame, mounts, water lines, guard of threaded rods) and their knock-on changes | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-003, Table 1 |
| 2026-10-02 | Mass (R13): options (a) and (b) together. The bench supply still ships in the kit (HBN-DDR-002, D10) but sits beside the bench, and the deck becomes 10 mm, giving 24.2 kg, which holds as long as the tank is aluminium | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-003, A1 |
| 2026-10-02 | Separator water: option (a) for the prototype. The teacher drains the separator by hand at the 20 kPa gauge holding pressure, under the hood, with H2Guard running | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-003, A2 |
| 2026-10-02 | Hydrogen purity (R9): fit a catalytic deoxidizer between separator and drier now; remove it only if the stack supplier's data show oxygen in the hydrogen within the fuel cell's 99.995 % limit at the bench's lowest operating current | Amish: "i approve your recommendations for all 555 open decisions." | HBN-CAL-001 section 8, HBN-REQ-001 R9 |
| 2026-10-02 | H2Guard interface (R8): propose to H2Guard a 24 V normally closed tank solenoid powered directly from H2Guard so its alarm removes valve power; H2Guard's alarm contact in series with the 310 kPa cut relay so either one breaks the 9 A supply line; 60 m³/h stated as the hood extraction rate, separate from H2Guard's 150 m³/h room exhaust; and vocational technician training as the shared first user | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-002 D15, REVIEW.md |
| 2026-10-02 | Tank: a certified aluminium cylinder (6061-T6 class) of about 2 L with a stamped working pressure of 1 MPa or more and a threaded neck; stainless only if a rated stainless cylinder of about 1.0 kg or less is found | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-002 O3 |
| 2026-10-02 | First worksheets: for post-16 vocational learners on hydrogen or renewable energy technician courses, aligned to the electrochemistry, gas safety and efficiency units of the first partner college's course | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-002 O1 |
| 2026-10-02 | First use: an instructor-run class demonstration; group practicals only after the bench has a recorded run of attended fills with H2Guard tested before each | Amish: "i approve your recommendations for all 555 open decisions." | HBN-DDR-002 O2 |
