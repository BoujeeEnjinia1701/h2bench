---
doc_id: HBN-BLD-001
title: H2Bench prototype build plan
project: H2Bench
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (HBN-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "HBN-DDR-003 accepted (2026-10-02); separator drain rule"
---

# H2Bench prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order.*

The prototype is one H2Bench: a 900 x 450 mm aluminium-framed deck that sits on an existing lab table, with a clear canopy hood 570 mm above it on four posts and a printed instrument panel across the back. On the deck, from left to right in the order the energy flows, stand a bench power supply, a water reservoir and deionizer, a small electrolyzer stack, a separator and drier, a check valve and flame arrestor, a 2 L hydrogen tank in a rod guard with its manifold, a regulator, a fuel cell and a lamp load. The H2Guard detector, fan and controller sit at the high point of the hood. Figure 1 shows the 26 components in the order you make or fit them. The frame, deck, lip, posts, top frame, panel, canopy and eight small mounts are made in a workshop; the rest are bought and fitted. The work is sawing and drilling aluminium extrusion, folding thin aluminium sheet, cutting HDPE and polycarbonate sheet, fitting compression fittings to 6 mm tubing and wiring bought modules. The parts cost about USD 999 from the bill of materials.

> **Safety:** This bench makes, stores and uses hydrogen, which burns in air from about 4 to 74 % and ignites very easily, and holds it at up to 300 kPa gauge. Nothing in sections 3 and 4 uses hydrogen: the build is dry until the safety stops of section 6. Never connect the electrolyzer, pressurize the tank or open the hydrogen line until those stops say so, and never run the bench without H2Guard active. The bench supply is mains powered: use it only on an earthed socket with a 30 mA RCD. Cut aluminium and polycarbonate edges are sharp; deburr everything.

## 2. What changed to make it buildable

The concept showed what the bench does; some of its parts could not be made or fixed as drawn. Each change below keeps what the bench does, and all of them are recorded in decision record HBN-DDR-003, made under Amish's 2026-09-30 instruction to make the design physically buildable and accepted by him on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Frame | One fused shape, bars overlapping at every corner | Six cut lengths of slotted extrusion joined by inside corner brackets (Figure 3) | Standard parts, no welding |
| Drip lip | Moulded into the HDPE deck | Aluminium angle screwed on a silicone bead; the panel closes the back (Figure 8) | HDPE cannot be glued or moulded in a workshop |
| Posts and canopy | Two front posts standing on the lip; the canopy held only at the front; the panel held by nothing | Four posts on the frame, a top frame, the canopy screwed to it, the panel screwed to the rear posts (Figures 6, 8, 10) | A closed frame carries the canopy and fan |
| Duct collar | Fused into the canopy | Bought flanged spigot through a 106 mm hole (Figure 13) | Bought part |
| Relief and vent lines | Relief line pressed against the canopy, unsupported; no vent line | Both lines clipped to a hanger, ending 7 mm below the canopy (Figure 12) | The gas must get out into the hood |
| Water side | Not drawn | Reservoir on a 60 mm stand, three water lines to and from the stack (Figures 14, 25) | The stack is fed by gravity |
| Electrolyzer | Tie rods through its cell plates; feet that could not be screwed down | Rods clear of the plates; two angle feet bolted to the end plates (Figure 16) | Every screw can be reached |
| Separator and drier | Loose, 3 mm apart in line with no room for fittings | On a column bracket with pipe clips; gas loops over from one top to the other (Figure 18) | Room for every fitting |
| Arrestor | 150 mm up on a post block | 60 mm up in an HDPE saddle straight off the drier outlet (Figure 20) | Short, supported run clear of the tank |
| Tank guard | Rods standing loose; a top ring that would need welding | Threaded rods in tee nuts, a bolted top plate, the tank in a pocketed cradle (Figure 22) | No welding; the tank cannot tip or lift |
| Fuel cell stand | A solid block in the fan's air path | A folded bridge, open front and back (Figure 24) | Air flows through the stack |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing at the front of the bench (the student side); "front" is the student side and "back" the instrument panel. Heights are above the lab table unless a step says otherwise; the deck top is 32 mm above the table. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

All extrusion, brackets and T-nuts are one 20-series system (20 x 20 mm profile, 6 mm slot). Mounts are fixed to the deck with 5 mm stainless self-tapping screws in 4 mm pilot holes, 10 mm deep, marked through the mount's own holes with the mount in place (Table 2).

*Table 2. Where each mount goes on the deck, measured from the left end and from the front edge of the deck.*

| Mount | From the left end | From the front edge |
| --- | --- | --- |
| Reservoir stand (top) | 20 to 134 | 25 to 145 |
| Water post (centre) | 146 | 80 |
| Electrolyzer end plates | 235 to 365, feet 215 to 385 | centred 185 |
| Separator and drier (centres) | 422 and 480 | 185 |
| Column bracket (face) | 402 to 502 | 220 |
| Arrestor saddle (centre) | 530 | 185 |
| Tank cradle and guard (centre) | 625 | 185 |
| Regulator (centre) | 730 | 185 |
| Fuel cell bridge | 790 to 875 | centred 185 |
| Load and lamp | 750 to 890 | 10 to 65 |
| Bench supply (on its feet) | 10 to 160 | 201 to 415 |

### 3.1 Frame

![Figure 2. Making sketch of the frame](../cad/drawings/HBN-DWG-101.png)

*Figure 2. Frame making sketch (HBN-DWG-101).*

**What it is and what it is made from.** The rectangle the deck sits on and the posts stand on. 20 x 20 mm slotted aluminium extrusion, 3.44 m in all.

**How to make it.**

1. Cut two rails 900 long (front and back) and four rails 410 long (two end rails and two cross rails). Saw square within 0.3 mm and deburr every end.
2. Lay the rails upside down on a flat bench: the long rails run the full 900; the short rails fit between them, the end rails flush with the ends and the cross rails centred 150 each side of the middle.
3. Before closing the frame, slide drop-in T-nuts into the top slots: three in each long rail and two in each short rail, for the deck screws.
4. Join each meeting with one inside corner bracket on the inside faces, two M5 x 10 screws into T-nuts.

**How it fits the parts next to it.**

![Figure 3. Joint 1: frame corner](05-build-plan/joint-01.png)

*Figure 3. The end rail butts between the long rails; one inside bracket holds each meeting.*

The deck lies on the top faces. The front posts stand on the end rails and the rear posts on the ends of the back rail (Figure 6).

**Check before moving on.** The diagonals are equal within 2 mm and the frame lies flat on the bench without rocking.

### 3.2 Deck, water post and drip lip

![Figure 4. Making sketch of the deck](../cad/drawings/HBN-DWG-102.png)

*Figure 4. Deck making sketch (HBN-DWG-102), with the drip lip and the holes that must be made before the deck goes on.*

**What it is and what it is made from.** The wet tray everything stands on. HDPE sheet 12 mm, 900 x 450; aluminium angle 10 x 10 x 1.5 mm for the lip; a 200 mm length of the frame extrusion for the water post.

**How to make it.**

1. Cut the sheet to 900 x 450 and round the corners lightly.
2. Cut the front notches, one at each end: 20 in from the end edge, from 85 to 145 back from the front edge. Cut the rear notches 40 x 20 at each back corner.
3. Set the deck on the frame, mark through from the T-nuts, and drill 5.5 mm, countersunk from the top, for the frame screws.
4. Drill four 10.5 mm holes for the guard rods on a 156 mm square centred 625 from the left end and 185 from the front edge. Press an M10 tee nut into each from below.
5. Drill one 5.5 mm hole, countersunk from below, 146 from the left end and 80 from the front edge, and screw the water post (Figure 5) to the deck through it, into its tapped end.
6. Cut the lip angle: one piece 900 for the front, and two pieces 75 and two pieces 282 for the ends (they stop at the post notches and at the panel).

**How it fits the parts next to it.** The deck lies on the frame on countersunk M5 screws into the T-nuts. The lip angles go on in step 2 with one leg flat on the deck at its edge and the other standing 10 up, screwed every 100 mm on a bead of silicone; the panel closes the back edge (Figure 8).

**Check before moving on.** The deck lies flat on the frame with every notch clear of the brackets; the tee nuts are flush underneath; the water post stands upright.

### 3.3 Posts

![Figure 5. Making sketch of the post and the water post](../cad/drawings/HBN-DWG-103.png)

*Figure 5. Post and water post making sketch (HBN-DWG-103).*

**What it is and what it is made from.** Four uprights that carry the top frame, canopy and panel. 20 x 20 mm extrusion.

**How to make it.**

1. Cut four lengths of 582, square, and deburr. (Cut the 200 mm water post from the same bar.)
2. Tap the centre hole M5, 12 deep, at both ends of every post; the water post needs its bottom end only.
3. Slide four T-nuts into the front slot of each rear post for the panel screws.

**How it fits the parts next to it.**

![Figure 6. Joint 2: front post foot](05-build-plan/joint-02.png)

*Figure 6. A front post stands on the end rail through a notch in the deck, held by an inside bracket in front and one behind. A rear post has one bracket, on its inner side (Figure 8).*

**Check before moving on.** Every post is upright within 1 mm over its length.

### 3.4 Instrument back panel

![Figure 7. Making sketch of the instrument panel](../cad/drawings/HBN-DWG-105.png)

*Figure 7. Instrument back panel making sketch (HBN-DWG-105).*

**What it is and what it is made from.** The back wall of the bench, printed with the energy-chain schematic, carrying the display and the three stage meters. Aluminium composite panel 3 mm.

**How to make it.**

1. Cut the panel 900 wide x 550 tall. Have the schematic printed on the front first, or apply it as printed vinyl.
2. Drill four 5.5 mm holes 10 in from each side edge, at 60, 220, 380 and 530 up from the bottom edge.
3. Cut the display opening 230 x 100, centred, 355 to 455 up from the bottom edge.
4. Cut three meter openings 80 x 50, 225 to 275 up, with their left edges 75, 205 and 705 from the left side. Check each opening against the meter you bought before cutting; the bezels cover the cut edges.

**How it fits the parts next to it.**

![Figure 8. Joint 4: panel foot and rear post](05-build-plan/joint-04.png)

*Figure 8. Seen from behind. The panel screws to the front face of the rear post and stands on the deck; the post's foot bracket sits on its inner side.*

The back face sits flat on the rear posts on M5 button-head screws into the T-nuts; the bottom edge stands on the deck on a bead of silicone, which closes the back of the drip tray; the top edge meets the underside of the side top rails.

**Check before moving on.** The panel is flat and square to the deck.

### 3.5 Top frame

![Figure 9. Making sketch of the top frame](../cad/drawings/HBN-DWG-104.png)

*Figure 9. Top frame making sketch (HBN-DWG-104).*

**What it is and what it is made from.** The rectangle at the top of the posts that the canopy lies on. 20 x 20 mm extrusion and eight inside corner brackets.

**How to make it.**

1. Cut two rails 860 (front and back) and two rails 305 (sides).
2. Slide T-nuts into the top slots for the canopy screws: four in each long rail and two in each side rail.

**How it fits the parts next to it.**

![Figure 10. Joint 3: top frame corner](05-build-plan/joint-03.png)

*Figure 10. Seen from inside the hood with the canopy off. The rails butt against the post; a bracket under each long rail and one inside each side rail; the canopy lies on top.*

All rail tops are flush with the post tops, 570 above the deck.

**Check before moving on.** The diagonals across the top are equal within 2 mm.

### 3.6 Canopy, duct collar and outlet hanger

![Figure 11. Making sketch of the canopy](../cad/drawings/HBN-DWG-106.png)

*Figure 11. Canopy making sketch (HBN-DWG-106).*

**What it is and what it is made from.** The clear hood that gathers any hydrogen at one high point, the duct, for the H2Guard sensor and fan. Polycarbonate sheet 3 mm, a bought 100 mm flanged duct collar, and a 70 mm length of 20 x 20 x 2 mm aluminium angle for the outlet hanger.

**How to make it.**

1. Cut the sheet 900 x 345, keeping the film on while working.
2. Cut the duct hole 106 across, centred on the middle line, 240 back from the front edge, with a hole saw at low speed.
3. Drill 6 mm screw holes (oversize, so the sheet can move with heat) 10 in from the edges: front and back at 110 and 330 each side of the middle; each side 120 and 220 back from the front edge.
4. Drill two 4.5 mm hanger holes 93 back from the front edge, 150 and 200 right of the middle.
5. Make the outlet hanger (Figure 12): two 4.5 mm holes in the flat leg 10 from each end, two 6.5 mm clip holes in the hanging leg 15 and 55 from the left end, 10 below the canopy.

![Figure 12. Making sketch of the outlet hanger](../cad/drawings/HBN-DWG-114.png)

*Figure 12. Outlet hanger making sketch (HBN-DWG-114).*

**How it fits the parts next to it.**

![Figure 13. Joint 9: duct collar through the canopy](05-build-plan/joint-09.png)

*Figure 13. Cut open. The spigot passes through the hole and its flange sits on the sheet on a silicone bead with four M4 screws; the H2Guard fan sits on the spigot.*

The sheet lies on the top frame on M5 screws with large washers. The hanger is screwed under the sheet above the tank manifold with two M4 screws, nuts on top.

**Check before moving on.** No cracks run from any hole; the sheet lies flat.

### 3.7 Reservoir stand

![Figure 14. Making sketch of the reservoir stand](../cad/drawings/HBN-DWG-107.png)

*Figure 14. Reservoir stand making sketch (HBN-DWG-107).*

**What it is and what it is made from.** A folded stand that lifts the water reservoir 60 mm, so its water stands above the electrolyzer's water inlet and feeds it by gravity. Aluminium sheet 2 mm.

**How to make it.**

1. Cut a blank 114 wide x about 260 long (top 120, legs 58, feet 15); check the bend allowance on a scrap first.
2. Fold the legs down 90 degrees along the two long-side lines, then the feet outward 90 degrees.
3. Drill two 5.5 mm holes in each foot, 30 and 85 from the left edge.

**How it fits the parts next to it.** The feet lie flat on the deck, the left edge against the left front post and the front foot against the drip lip. The reservoir stands on the top; a band clip holds it to the water post at mid height, and a second band clip holds the deionizer cartridge to the other side of the post.

**Check before moving on.** The top is level and the stand does not rock.

### 3.8 Electrolyzer feet

![Figure 15. Making sketch of the electrolyzer feet](../cad/drawings/HBN-DWG-108.png)

*Figure 15. Electrolyzer feet making sketch (HBN-DWG-108).*

**What it is and what it is made from.** Two feet that carry the bought electrolyzer by its end plates. Aluminium unequal angle 40 x 20 x 3 mm.

**How to make it.**

1. Cut two 70 lengths and deburr.
2. Upright 40 leg: two 6.5 mm holes 30 up from the deck, 25 each side of the middle, to suit the stack's end-plate mounting holes (check them on the stack before drilling).
3. Flat 20 leg: two 5.5 mm holes 11.5 out from the end-plate face, 25 each side of the middle.

**How it fits the parts next to it.**

![Figure 16. Joint 5: electrolyzer foot](05-build-plan/joint-05.png)

*Figure 16. The upright leg bolts flat to the outside face of an end plate, below the lower tie rods; the flat leg points outward and screws to the deck.*

The stack's base sits 20 above the deck.

**Check before moving on.** With the feet on, the stack stands level and does not rock.

### 3.9 Column bracket

![Figure 17. Making sketch of the column bracket](../cad/drawings/HBN-DWG-109.png)

*Figure 17. Column bracket making sketch (HBN-DWG-109).*

**What it is and what it is made from.** An upright plate behind the separator and drier that their pipe clips screw to. Aluminium sheet 3 mm.

**How to make it.**

1. Cut a blank 100 wide x 170 long and fold the bottom 23 back 90 degrees to make a foot; the face is 150 tall.
2. Drill two 5.5 mm holes in the foot, 14 behind the face, at 20 and 78 from the left edge.
3. Drill two 4 mm clip holes 115 above the deck at 20 and 78 from the left edge, in line with the separator and drier centres.

**How it fits the parts next to it.**

![Figure 18. Joint 7: separator and drier on the column bracket](05-build-plan/joint-07.png)

*Figure 18. A 60 mm pipe clip round the separator and a 40 mm clip round the drier, each screwed through the bracket.*

The bracket stands 5 behind the separator, its foot pointing back.

**Check before moving on.** The face is square to the deck and the clips line up with the column centres.

### 3.10 Arrestor saddle

![Figure 19. Making sketch of the arrestor saddle](../cad/drawings/HBN-DWG-110.png)

*Figure 19. Arrestor saddle making sketch (HBN-DWG-110).*

**What it is and what it is made from.** A small block that the check valve and flame arrestor rest in. HDPE 16 mm, 16 x 32 x 24.

**How to make it.**

1. Cut the block 16 long x 32 wide x 24 tall.
2. Bore a 31 mm half-round seat across the top, its centre 28 above the deck.
3. Drill a 4.2 mm hole 10 up the middle from below for a 5 mm self-tapping screw put up through the deck, and two 3 mm pilot holes in the sides for the band clip ends.

**How it fits the parts next to it.**

![Figure 20. Joint 8: arrestor on its saddle](05-build-plan/joint-08.png)

*Figure 20. The arrestor screws straight onto the drier outlet and rests in the seat under a band clip.*

**Check before moving on.** The arrestor sits level with the drier outlet and is not strained by its fittings.

### 3.11 Tank cradle

![Figure 21. Making sketch of the tank cradle](../cad/drawings/HBN-DWG-111.png)

*Figure 21. Tank cradle making sketch (HBN-DWG-111).*

**What it is and what it is made from.** A pocketed block the tank stands in. HDPE 20 mm, 130 x 130.

**How to make it.**

1. Cut a 130 square.
2. Bore a pocket 112 across and 10 deep, centred, with a router and circle jig (or a hole saw and chisel).
3. Drill four 5.5 mm holes 12 in from each corner.

**How it fits the parts next to it.**

![Figure 22. Joint 6: tank in its cradle and guard rods through the deck](05-build-plan/joint-06.png)

*Figure 22. Cut through the tank axis. The tank stands 10 deep in the pocket, 1 clear all round; each guard rod screws into a tee nut under the deck and is locked by a nut above it.*

The cradle sits inside the four guard rods, 8 clear of their nuts.

**Check before moving on.** The tank drops in and stands upright without rocking.

### 3.12 Guard rods and top plate

![Figure 23. Making sketch of the guard rods and top plate](../cad/drawings/HBN-DWG-112.png)

*Figure 23. Guard rods and top plate making sketch (HBN-DWG-112).*

**What it is and what it is made from.** The guard round the tank: four rods and a top plate. M10 stainless threaded rod; aluminium plate 4 mm.

**How to make it.**

1. Plate: cut 176 x 176; cut a 130 x 130 opening in the middle (drill the corners, cut with a jigsaw, file straight). Drill four 10.5 mm holes on a 156 square.
2. Rods: cut four lengths of 363. File the ends and run a nut over each end to clean the thread.

**How it fits the parts next to it.** Each rod screws into its tee nut and is locked with a nut and washer on the deck (Figure 22). The plate is clamped between two nuts on each rod, 60 above the top of the tank; the manifold, gauge and lines pass up through the opening.

**Check before moving on.** The plate is level within 1 mm, and the tank can be lifted out only once the plate is off.

### 3.13 Fuel cell bridge

![Figure 24. Making sketch of the fuel cell bridge](../cad/drawings/HBN-DWG-113.png)

*Figure 24. Fuel cell bridge making sketch (HBN-DWG-113).*

**What it is and what it is made from.** A folded stand that lifts the fuel cell 40 mm, open at front and back so its fan can move air through the stack. Aluminium sheet 2 mm.

**How to make it.**

1. Cut a blank 57 wide x about 190 long (top 85, legs 38, feet 15); check the bend allowance on a scrap first.
2. Fold the legs down 90 degrees, then the feet outward 90 degrees.
3. Drill the top to the stack's mounting holes, and two 5.5 mm holes in each foot, 15 each side of the middle.

**How it fits the parts next to it.** The stack sits on the top with its hydrogen inlet on the left side, facing the regulator, 5 above the bridge top.

**Check before moving on.** The stack is level and its fan face is clear of the bridge.

### 3.14 Bought components, lines and wiring

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Bench power supply (line 4).** Lab supply 0 to 30 V, 0 to 10 A, constant-current mode, earthed, with a plug-in 30 mA RCD (line 18).
- **Reservoir and deionizer (line 5).** 500 mL HDPE reservoir about 110 across and 170 tall with a low side outlet and a vented lid; mixed-bed resin cartridge with color change, about 50 across and 150 tall, with 6 mm fittings; conductivity check to 1 µS/cm.
- **Electrolyzer (line 6).** 4-cell PEM stack, about 7.8 V at 9 A, end plates about 110 square, hydrogen side rated to 332 kPa or more over the oxygen side, two mounting holes in each end plate, water in and oxygen out on one end plate.
- **Separator and drier (line 7).** Separator column about 60 across and 160 tall with a drain valve at its foot, drained by hand only at the 20 kPa gauge holding pressure, under the hood, with H2Guard running; 50 g indicating silica gel drier about 40 across and 130 tall; both rated 1 MPa or more.
- **Check valve and flame arrestor (line 8).** Stainless check valve, 7 kPa cracking, and a sintered flame arrestor rated for hydrogen, joined in line, about 28 across and 50 long.
- **Tank (line 9).** 2 L aluminium or stainless vessel, 110 across or less, flat base, working pressure 1 MPa or more.
- **Tank manifold (line 10).** Neck adapter carrying a 0 to 600 kPa absolute transducer, a 10 kΩ thermistor bonded to the shell, a relief valve set to 325 kPa gauge, a 0 to 600 kPa gauge, a needle valve set so venting 300 to 20 kPa gauge takes 3 min or more, and a pressure switch set to open at 310 kPa gauge.
- **Regulator and solenoid (line 11).** Regulator 0 to 100 kPa out, set near 50 kPa gauge; 12 V normally closed solenoid on the tank outlet.
- **Fuel cell (line 12).** Air-cooled PEM stack, 12 W class, 13 cells, about 75 x 47 x 70, with fan and purge valve.
- **Load and lamp (line 13), meters and logger (line 14).** Constant-current load 0 to 3 A with a 5 W LED lamp; logger board with three power monitors and shunts, pressure and temperature inputs, a 3.5 in display, and a 12 V relay rated 10 A DC or more.
- **Lines and fixings (lines 16 and 17).** PTFE or polyamide tubing 6 mm and compression fittings rated for hydrogen; 2.5 mm² wire for the electrolyzer supply; stainless M4, M5 and M6 fasteners, M10 tee nuts and nuts, drop-in T-nuts, 5 mm self-tapping screws, silicone sealant, hazard and flow-direction labels.

![Figure 25. Gas and water lines](05-build-plan/piping.png)

*Figure 25. Gas and water lines, block level.*

![Figure 26. Power, cut and interlock wiring](05-build-plan/wiring.png)

*Figure 26. Power, cut and interlock wiring, block level. No circuit board is laid out at this stage; bought modules stand in for it.*

The pressure switch on the manifold and the H2Guard relay output are wired in series in the coil circuit of the cut relay, which breaks the positive line from the bench supply to the electrolyzer: any open contact stops the electrolyzer, with no software in the path. H2Guard also breaks the 12 V supply to the normally closed tank solenoid, which closes the tank.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in.

### Step 1: frame rails and corner brackets

![Step 1](05-build-plan/step-01.png)

Rails upside down on a flat bench; one inside bracket at each meeting; T-nuts in the top slots before each joint closes. Turn the frame right way up.

### Step 2: deck, water post and drip lip

![Step 2](05-build-plan/step-02.png)

Fit the guard-rod tee nuts and the water post to the deck first (section 3.2). Then lay the deck on the frame and fix it with countersunk M5 screws into the T-nuts. Screw the lip angles down every 100 mm on a bead of silicone.

### Step 3: posts onto the frame

![Step 3](05-build-plan/step-03.png)

Each post stands through its deck notch onto the frame. Front posts: one bracket in front and one behind, on the end rail. Rear posts: one bracket on the inner side, on the back rail. Square each post before tightening.

### Step 4: instrument panel and top frame

![Step 4](05-build-plan/step-04.png)

Run a bead of silicone along the deck where the panel stands, set the panel against the rear posts and fit four M5 button-head screws each side. Then fit the four top rails and their eight brackets, flush with the post tops.

### Step 5: canopy, duct collar and outlet hanger

![Step 5](05-build-plan/step-05.png)

Screw the hanger under the sheet, then lay the sheet on the top frame and fit twelve M5 screws with large washers, snug, not tight. Fit the duct collar through its hole, flange on a bead of silicone, four M4 screws.

### Step 6: reservoir stand, reservoir and cartridge

![Step 6](05-build-plan/step-06.png)

Screw the stand down (Table 2). Stand the reservoir on it and the cartridge on the deck beside the water post; fit a band clip round each to the post.

### Step 7: electrolyzer on its feet

![Step 7](05-build-plan/step-07.png)

Bolt the feet to the end plates first, two M6 each. Set the stack down with its hydrogen outlet to the right and its water ports to the back, and screw the feet to the deck.

### Step 8: column bracket, separator, drier and arrestor

![Step 8](05-build-plan/step-08.png)

Screw the column bracket and the arrestor saddle down. Clip the separator and drier to the bracket. Screw the check valve and arrestor onto the drier's outlet, arrow toward the tank, and close the band clip over it.

### Step 9: cradle, guard rods and tank

![Step 9](05-build-plan/step-09.png)

Screw the cradle down. Screw each rod into its tee nut and lock it with a nut and washer on the deck. Lower the tank into the pocket, neck up.

### Step 10: tank manifold and guard top plate

![Step 10](05-build-plan/step-10.png)

Screw the manifold into the tank neck on thread sealant rated for hydrogen, gauge to the front, cut switch to the back. Run a nut down each rod to 56 above the tank top, drop the plate on, and fit a nut above it.

### Step 11: regulator, fuel cell and load

![Step 11](05-build-plan/step-11.png)

Screw the regulator and the fuel cell bridge down, then the fuel cell to the bridge, hydrogen inlet to the left. Screw the load case to the deck at the front right.

### Step 12: gas and water lines

![Step 12](05-build-plan/step-12.png)

Fit every line as Figure 25 shows: cut each tube square, deburr it, fit the inserts and compression nuts, and keep every gas line at least 5 clear of the tank. Clip the relief and vent lines to the hanger, ends 7 below the canopy. Label each line with its flow direction. **Hold point:** the leak checks of safety stop S3.

### Step 13: power supply, meters and wiring

![Step 13](05-build-plan/step-13.png)

Fit the meters and display into the panel openings and the logger behind the panel. Stand the supply on the deck at the left, mains lead routed off the deck. Wire as Figure 26 with the supply switched off and unplugged. **Hold point:** the wiring checks of safety stop S2.

### Step 14: H2Guard sensor, fan and controller

![Step 14](05-build-plan/step-14.png)

Fit the H2Guard sensor under the canopy beside the duct, the fan on the collar and the controller on the canopy, as the H2Guard project describes. Wire its relay output in series with the cut switch and in the solenoid supply (Figure 26). **Hold point:** safety stop S4.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of HBN-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Size and mass | R13 | Measure the envelope; weigh the bench with and without the supply | Within 1,000 x 500 x 800 mm; mass recorded against 25 kg |
| Guard and lines | R15 | Look at the guard and every line end | Tank inside the guard, top plate on; relief and vent lines end under the canopy; no fitting opens without a tool |
| Water quality | R11 | Conductivity at the stack inlet after the cartridge | 1 µS/cm or less |
| Leak tightness | R5, R7 | Nitrogen at 300 kPa gauge for 30 min, soapy water on every fitting (S3) | No bubbles; pressure fall within the transducer's resolution after temperature correction |
| Supply cut | R6 | Raise the manifold pressure with nitrogen to the switch point while watching the relay (S3) | The relay opens at 310 kPa gauge, give or take 5 |
| Relief valve | R6 | Bench test of the relief valve before fitting | Lifts at 325 kPa gauge, give or take 10 |
| Interlock | R8 | H2Guard test input or test gas at the sensor with the supply on a dummy load (S4) | Supply cut and solenoid closed within 2 s; fan runs |
| Electrolyzer power | R3 | Constant current 9 A, first fill (S5) | 100 W or less at the stack |
| Fill and cycle time | R2 | Time one fill from 70 to 300 kPa gauge and one discharge | Fill plus discharge within 60 min |
| Fuel cell output | R4 | Lamp load at 1.5 A (S6) | 10 W or more net |
| Logging | R12 | Log one cycle | Voltage, current, power, pressure and temperature at 1 Hz in a CSV file |
| Measurement | R1 | Hydrogen counted by gas law and by charge for three fills | Stage efficiencies repeat within 5 % relative |
| Vent and shutdown | R16 | Vent 300 to 20 kPa gauge through the needle valve; time a full setup and shutdown | Vent 3 min or more; bench safe within 5 min; setup within 15 min |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any work with the parts.** The workspace has a fire extinguisher for electrical fires, a clear route out, and no open flames, heaters or sparking tools near the bench. Safety glasses and gloves for cutting and drilling.
- **S2. Before the bench supply is plugged in.** The supply is earthed and plugged into the 30 mA RCD, which trips on its test button. The mains lead runs off the deck. With the supply off, the cut relay is open whenever the cut switch or the H2Guard contact is open (meter check). Wire sizes and polarity are checked against Figure 26.
- **S3. Before any gas pressure.** Every fitting is tight and labelled. Leak test with nitrogen, not air or hydrogen: 50 kPa gauge first, then 300 kPa gauge, soapy water on every fitting, 30 min hold. Check the cut switch at 310 kPa gauge with nitrogen. Vent the nitrogen through the needle valve, never by opening a fitting.
- **S4. Before any hydrogen is made.** H2Guard is fitted and tested: its alarm, its cut of the electrolyzer supply and its close of the tank solenoid all work within 2 s, and the fan extracts through the duct to outdoors. The relief valve has been bench tested. A trained supervisor is present.
- **S5. First fill.** Purge the tank of nitrogen and air by three fill and vent cycles to 300 kPa gauge, venting slowly through the needle valve each time (3 min or more). Attended the whole time, hood fan running. Stop at any H2Guard warning, any smell of burning, or any pressure above 300 kPa gauge that the cut does not stop. Keep the tank above 20 kPa gauge from then on so air cannot enter.
- **S6. Before the fuel cell runs.** The fuel cell supplier has accepted the gas the bench makes, or the deoxidizer is fitted (see the register). The regulator is set to about 50 kPa gauge with the solenoid closed and the fuel cell disconnected.
- **S7. Before students use the bench.** All first checks of section 5 are recorded; the supervisor knows the vent, purge and shutdown sequence; the room meets the site's hydrogen risk assessment.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade, or a mitre saw with a non-ferrous blade; bench vice with soft jaws; drill in a stand; drills 3 to 10.5 mm; countersink; M5 tap; hole saws 106 and 112 mm, or a router with a circle jig; jigsaw with metal and plastic blades; files and deburring tool; scriber, engineer's square, steel rule and calipers; hand sheet folder (or hardwood angle in the vice) for 2 and 3 mm aluminium up to 120 mm wide; tube cutter for 6 mm tubing; spanners for compression fittings; torque screwdriver; caulking gun; multimeter; conductivity meter; stopwatch; scale to 30 kg; nitrogen cylinder with a regulator to 0 to 400 kPa gauge for leak testing; leak detection fluid.

**Skills.** No certified trade is needed for the build. Basic metalwork (marking out, sawing, drilling, tapping, folding thin sheet), plastic sheet work, making compression fittings on small tubing, and low-voltage wiring. The mains side is a bought, earthed supply plugged into an RCD; no mains wiring is part of this build. Running the bench with hydrogen needs a supervisor trained in hydrogen handling.

**Workspace.** A bench about 1.5 x 0.8 m in a ventilated room; a metalwork corner kept apart from the electronics; for the first fill, a lab with an extraction route outdoors for the H2Guard duct.

**Personal protective equipment.** Safety glasses for cutting, drilling and all gas work; cut-resistant gloves for aluminium and polycarbonate; hearing protection when sawing; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 135 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/HBN-DWG-101` to `HBN-DWG-114`.
- General arrangement: `cad/drawings/HBN-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (HBN-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; mass in section 9, cost in section 10.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (HBN-DDR-003), with HBN-DDR-001 and HBN-DDR-002; the register `docs/06-design-decisions.md` (HBN-DEC-001).
- Requirements: `docs/03-requirements.md` (HBN-REQ-001 v0.6).
