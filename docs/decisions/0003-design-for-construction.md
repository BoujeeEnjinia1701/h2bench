---
doc_id: HBN-DDR-003
title: H2Bench design for construction
project: H2Bench
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 change what the bench weighs or how it is operated and are **Proposed, awaiting Amish**; they are also listed in the design decisions register (`docs/06-design-decisions.md`).

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The H2Bench model of HBN-DDR-002 showed what the bench does (the gas train, the tank, the hood and the meters) but was a massing model: several parts were fused shapes that cannot be cut or joined as drawn, several had no fixing, and the water side of the electrolyzer was not modelled at all.

Checking the concept model with build123d found: the tie rods of the electrolyzer cut 2 mm into its cell plates; the gas lines were seven separate pieces that did not join up; the front posts stood on the 6 mm drip lip; the canopy, the back panel and every component on the deck touched their neighbours but had nothing holding them. The rest of Table 1 comes from asking, for each part, how it is made and how it fastens to the next.

The changes keep what H2Bench does: the same 900 x 450 x 755 mm envelope, the same electrolyzer, 2 L tank, pressures, fuel cell, meters, hood and H2Guard positions, and the same gas path from stack to fuel cell. No energy, gas, pressure or venting figure in HBN-CAL-001 changes. Every change is in `cad/src/model.py`, which now builds each part separately and runs 135 constructability checks (`python cad/src/model.py --check`): no part overlaps another except where intended (a line pushed into its fitting, a rod through its nuts, the manifold in the tank neck), 70 pairs that must bear on or fasten to each other touch, 16 clearances hold, and every part is supported. All 135 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The frame was one fused shape: six bars overlapping at every corner, with no joints. | Six cut lengths of 20 x 20 mm slotted aluminium extrusion: two rails of 900 mm, two end rails and two cross rails of 410 mm between them, joined by eight inside corner brackets with M5 screws into drop-in T-nuts. | Standard 20-series parts, cut with a hacksaw; no welding (R14). |
| P2 | The drip lip was moulded into the HDPE deck. HDPE cannot be glued, and a lip cannot be cut from a 12 mm sheet. | A 10 x 10 x 1.5 mm aluminium angle screwed along the front and end edges on a bead of silicone, standing 10 mm above the deck (was 8 mm). The instrument panel closes the back edge. | Bought section, screwed, sealed. |
| P3 | Two front posts stood on the 6 mm lip with no fixing; the 3 mm polycarbonate canopy was cantilevered 345 mm behind them with nothing at the back; the back panel stood on the lip and touched nothing else. | Four posts of the same extrusion, each standing on the frame through a notch in the deck and held by inside corner brackets (two on a front post, one on a rear post). A top frame of the same extrusion joins the post tops (two rails of 860 mm, two of 305 mm, eight brackets). The canopy lies on the top frame on 12 screws. The panel screws to the front faces of the rear posts and stands on the deck on a silicone bead; it is 550 mm tall (was 570) so its top meets the side rails. | A closed frame carries the canopy and the H2Guard fan without sagging, and every joint is a standard bracket. |
| P4 | The 100 mm duct collar was fused into the canopy sheet. | A bought flanged 100 mm spigot through a 106 mm hole, flange on top on a silicone bead, four M4 screws. | Bought part; the H2Guard fan sits on the spigot as before. |
| P5 | The relief line ended flush against the underside of the canopy, which would block it; it was 300 mm long with no support; the vent valve had no line at all. | Both the relief line and a new vent line rise to an outlet hanger (20 x 20 x 2 mm angle) screwed under the canopy, are clipped to it, and end 7 mm below the sheet. | Gas leaves freely into the hood, where it rises to the H2Guard sensor and the duct, as the safety case assumes. |
| P6 | The water side of the electrolyzer was missing: no line from the reservoir or cartridge to the stack, and the oxygen port floated 10 mm off the cell block. A gravity-fed stack needs its reservoir above it. | Water ports moved to the back face of the left end plate (water in low, oxygen and water out high). The reservoir stands on a folded 60 mm aluminium stand; the deionizer cartridge (now 150 mm tall) stands beside it; three 6 mm water lines run reservoir to cartridge, cartridge to stack, and stack back to the reservoir top. Oxygen leaves through the reservoir's vented lid into the hood. | A sealed, primed line from a reservoir above the stack feeds it by gravity, with no pump, as small PEM stacks are run. |
| P7 | The electrolyzer's tie rods cut 2 mm into its cell plates, and its feet were two bars under the stack that could not be screwed down once the stack was on them. | Tie rods placed 6 mm outside the plates. Two feet of 40 x 20 x 3 mm aluminium angle, each bolted to an end plate by two M6 screws and to the deck by two 5 mm screws reachable beside the stack; the stack's base is 20 mm above the deck (was 13). | Every screw can be reached; the stack's own end plates carry it. |
| P8 | The separator and drier stood loose; the tube between them was 3 mm long, with no room for a fitting; the separator's water return to the reservoir came from a column at tank pressure with no valve. | A folded 3 mm aluminium column bracket behind both columns with a pipe clip round each. Gas leaves the top of the separator and loops over into the top of the drier; the drier's bottom outlet screws straight into the check valve and arrestor. The separator gets a manual drain valve at its foot. | Room for every fitting; nothing at tank pressure drains without a valve. (Draining by hand is Table 3, A2.) |
| P9 | The check valve and arrestor sat 150 mm up on a 15 mm post block, which put its outlet line into the tank. | The arrestor lies 60 mm above the table in an HDPE saddle with a band clip, straight off the drier outlet; the line to the tank rises at 108 mm, 9 mm clear of the tank and between the guard rods. | Short, supported run; every line clears the tank by 5 mm or more. |
| P10 | The tank stood on top of a solid block; the four guard rods stood on the deck with nothing holding them; the top of the guard was a 10 mm square ring that would have to be welded. | A 20 mm HDPE cradle with a 112 mm pocket 10 mm deep (the tank stands 8 mm lower than before). Four M10 stainless threaded rods screw into tee nuts pressed into the deck and are locked by nuts above it; a 4 mm aluminium top plate with a 130 mm opening is clamped between two nuts on each rod, 60 mm above the tank top. | No welding (R14); the tank cannot tip out of the pocket or lift past the plate. |
| P11 | The fuel cell stood on a solid block that would block the air its fan moves. | A folded 2 mm aluminium bridge, 40 mm tall, open at front and back. | Same height; the fan's air path stays clear. |
| P12 | The reservoir and cartridge stood loose. | A 200 mm length of the frame extrusion (the water post) stands between them, screwed to the deck from below before the deck goes on; a band clip holds each vessel to it. | Light vessels held at mid height by one standard part. |
| P13 | Nothing fixed the components to the deck. | Every mount (stand, feet, brackets, cradle, saddle, regulator, bridge, load case) is marked through its own holes onto the deck and fixed with 5 mm stainless self-tapping screws into 4 mm pilot holes. | HDPE holds self-tapping screws well; no access from below is needed after the deck is on. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 28.0 kg with the bench supply (was 25.3 kg), 25.0 kg without it (was 22.3 kg) [HBN-CAL-001 section 9]. R13 stays at risk, now by 3.0 kg. Made parts are now weighed from their model volumes. | The rear posts, top frame and brackets add about 2.4 kg. |
| Cost | BOM lines 1, 3, 5, 6, 7, 8, 9, 12, 16 and 17 repriced for the parts added: USD 999 with the bench supply (was USD 885), USD 934 without it. Value-engineering target: USD 885. Estimated cost of the constructable design: USD 999 (USD 114 over the target). `budget_usd` unchanged. | Parts added for construction. |
| Guard clearance | Corrected from 18 mm to 50 mm. The concept note measured from the tank to a rod as if the rods stood on the axes; they stand at the corners of a 156 mm square. R15 stays met. | Calculation correction; no geometry change. |
| Drawing | HBN-DWG-001 Rev P3; making sketches HBN-DWG-101 to 114 added. | Follows the model. |
| Documents | HBN-CAL-001 v0.4, HBN-REQ-001 v0.6, HBN-PRC-001 v0.6: mass, cost, guard clearance and the constructable parts. No requirement changed status; cost (R14) is now reported against the value-engineering target rather than as met. | Follows the model. |
| Energy, gas and pressure | Unchanged: the tank volume, pressures, stack and fuel cell are the same, so every figure of HBN-CAL-001 sections 2 to 8 and 11 stands. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Mass (R13, 25 kg or less) is now 28.0 kg with the bench supply. This replaces open item O4 of HBN-DDR-002. | (a) carry the bench supply separately (25.0 kg, exactly on the limit); (b) also use a 10 mm deck (24.2 kg); (c) raise R13 to 30 kg, since the bench is assembled on its table and moved in two parts; (d) look for lighter hood parts (a lighter canopy frame of 15 x 15 mm extrusion saves about 0.6 kg). | (a) and (b) together, which meets 25 kg with 0.8 kg to spare and changes nothing a student sees. |
| A2 | The separator's water now returns to the reservoir by hand: the teacher opens the drain valve at the 20 kPa gauge holding pressure, catches the water and pours it back. The concept had a plumbed return. | (a) by hand, as modelled; (b) a plumbed return with a needle valve and a float trap. | (a) for the prototype: a few grams of water per fill, and nothing at tank pressure can drain on its own. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan HBN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 10 met, 1 not met (R9 purity), 3 at risk (R8, R10, R13), 1 not verifiable at TRL 3 (R16); cost (R14) is reported against the value-engineering target, USD 114 over it (it was counted as met at USD 885 before the construction changes).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: no rear posts, no top frame, the tank higher and the old mounts. They need updating on Amish's Mac, where Blender is.
- The stack's end-plate mounting holes, the tank neck thread, the fuel cell's mounting holes, the meters' bezel sizes and the reservoir's outlet are confirmed when the parts are bought (register, "To confirm when parts are bought").
