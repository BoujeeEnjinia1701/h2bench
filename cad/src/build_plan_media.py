"""H2Bench prototype build plan pictures (HBN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|diagrams ...]
With no argument it draws everything. A sheet, joint or step can be drawn alone by number, for
example `python cad/src/build_plan_media.py sheet:105 joint:3 step:7` (one picture per process
keeps memory low). Every picture is drawn from cad/src/model.py (build_components), so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/HBN-DWG-101 to 114        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/piping.png          gas and water lines, block level (matplotlib)
    docs/05-build-plan/wiring.png          power, cut relay and interlock wiring, block level
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = build_components(P)
GY, DT, TOP = P["gas_y"], D["deck_top"], D["top"]


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*keys):
    return _fuse([C[k].shape for k in keys])


def part(name, keys, color=None, explode=(0, 0, 0), alpha=1.0):
    keys = [keys] if isinstance(keys, str) else keys
    return Part(name, S(*keys), color or C[keys[0]].color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


# ----------------------------------------------------------------- named components, in build order
ORDER = [
    ("frame", "Frame: six rails and corner brackets", ["rail_front", "rail_back", "end_l", "end_r", "cross_l", "cross_r", "frame_brackets"], "#9CA3AF"),
    ("deck", "Deck and water post", ["deck", "water_post"], "#D6D3D1"),
    ("lip", "Drip lip angles", ["lip"], "#6B7280"),
    ("posts", "Posts and foot brackets", ["posts", "post_brackets"], "#64748B"),
    ("panel", "Instrument back panel", ["panel"], "#CBD5E1"),
    ("top", "Top frame and brackets", ["top_rails", "top_brackets"], "#475569"),
    ("canopy", "Canopy, duct collar, outlet hanger", ["canopy", "collar", "hanger"], "#93C5FD"),
    ("stand", "Reservoir stand", ["res_stand"], "#A8A29E"),
    ("water", "Reservoir, cartridge, band clips", ["reservoir", "di", "water_bands"], "#38BDF8"),
    ("feet", "Electrolyzer feet", ["ely_feet"], "#B45309"),
    ("ely", "Electrolyzer stack", ["ely", "ely_cells", "ely_meas"], "#0F766E"),
    ("colbr", "Column bracket", ["col_bracket"], "#78716C"),
    ("columns", "Separator, drier, pipe clips", ["sep", "drier", "col_clips"], "#6B7280"),
    ("deox", "Catalytic deoxidizer and clip", ["deox", "deox_clip"], "#7C3AED"),
    ("arr", "Arrestor saddle, arrestor, clip", ["arr_saddle", "arrestor", "arr_clip"], "#C2410C"),
    ("cradle", "Tank cradle", ["cradle"], "#E7E5E4"),
    ("rods", "Guard rods and lower nuts", ["guard_rods", "guard_nuts"], "#57534E"),
    ("tank", "Hydrogen buffer tank", ["tank"], "#E5E7EB"),
    ("manifold", "Tank manifold", ["manifold"], "#EA580C"),
    ("gplate", "Guard top plate", ["guard_plate"], "#78716C"),
    ("reg", "Regulator and solenoid valve", ["reg"], "#D4A017"),
    ("fc", "Fuel cell on its bridge", ["fc_bridge", "fc"], "#1F2937"),
    ("load", "Electronic load and lamp", ["load"], "#FACC15"),
    ("lines", "Gas and water lines", ["gas_lines", "water_lines"], "#0EA5E9"),
    ("psu", "Bench power supply", ["psu"], "#374151"),
    ("meters", "Meters, logger and display", ["meters"], "#15803D"),
    ("h2g", "H2Guard sensor, fan, controller", ["h2guard"], "#DC2626"),
]
M = {k: part(n, keys, col) for k, n, keys, col in ORDER}


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- overview
def overview():
    off = {"frame": (0, 0, -520), "deck": (0, 0, -380), "lip": (0, -120, -300),
           "posts": (0, 380, 120), "panel": (0, 560, 120), "top": (0, 380, 300), "canopy": (0, 380, 460),
           "stand": (-60, -260, -120), "water": (-60, -260, 40), "feet": (0, -60, -120), "ely": (0, -60, 0),
           "colbr": (0, 110, -90), "columns": (0, -230, 40), "deox": (0, 40, 190), "arr": (40, -300, -60), "cradle": (0, -60, -160),
           "rods": (70, 40, -30), "tank": (150, -260, 250), "manifold": (150, -260, 470), "gplate": (70, 40, 170),
           "reg": (60, -220, -60), "fc": (120, -120, 60), "load": (140, -160, -160), "lines": (0, -380, 470),
           "psu": (-220, 40, 120), "meters": (0, 520, 150), "h2g": (0, 380, 700)}
    parts = [mv(M[k], off[k]) for k, *_ in ORDER]
    return bv.overview(parts, OUT / "overview.png", "H2Bench prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the hood frame is pulled back, the bench parts forward",
                       elev=20, azim=-60, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
BASE = dict(project="H2Bench", date=DATE)


def _sheet(dwg, keys, name, title, material, notes, neighbours, view_shape=None, inset_view=(24, -58), color=None):
    pt = part(name, keys, color)
    return bv.component_sheet(pt, neighbours, dwg_no=dwg, title=title, material=material, notes=notes,
                              view_shape=view_shape, inset_view=inset_view, **BASE)


def sheet(n):
    import build123d as b
    g = lambda *k: [M[x] for x in k]  # noqa: E731
    s = P["post"]
    if n == 101:
        return _sheet("HBN-DWG-101", ["rail_front", "rail_back", "end_l", "end_r", "cross_l", "cross_r", "frame_brackets"],
                      "Frame", "H2Bench frame: making sketch", "Aluminium extrusion 20 x 20 mm, 6 mm slot (20 series)", [
            "Cut two rails 900 mm long (front and back).",
            "Cut four rails 410 mm long: two end rails and two cross rails.",
            "Saw square, within 0.3 mm; deburr every end.",
            "Lay the frame upside down on a flat bench: the long rails run the",
            "  full 900, the short rails fit between them.",
            "Cross rails centred 150 mm each side of the middle (300 apart).",
            "Join each meeting with one inside corner bracket on the inside",
            "  faces, two M5 x 10 screws and two drop-in T-nuts.",
            "Before closing the frame, slide drop-in T-nuts into the top slots:",
            "  3 per long rail and 2 per short rail, for the deck screws.",
            "Fits: the deck sits on the top faces; the posts stand on the",
            "  end rails and on the ends of the back rail.",
            "Check: diagonals equal within 2 mm; frame flat on the bench.",
        ], [part("Posts", ["posts", "post_brackets"])], inset_view=(30, -55))
    if n == 102:
        return _sheet("HBN-DWG-102", ["deck"], "Deck", "H2Bench deck: making sketch", "HDPE sheet 10 mm, natural or white", [
            "Cut the sheet to 900 x 450 mm; round the corners lightly.",
            "Front notches, one at each end: 20 mm in from the end edge and",
            "  60 mm long, from 85 to 145 mm back from the front edge.",
            "Rear notches: 40 x 20 mm at each back corner.",
            "Frame screws: 5.5 mm, countersunk from the top, over the T-nuts",
            "  in the frame's top slots (mark through from the frame).",
            "Guard rods: four 10.5 mm holes on a 156 mm square centred 175",
            "  right of the middle and 40 in front of the centre line. Press an",
            "  M10 tee nut into each from below before the deck goes on.",
            "Water post: one 5.5 mm countersunk hole from below, 146 right of",
            "  the left end and 80 back from the front edge; fit the post now.",
            "Mounts (stand, feet, brackets, cradle, saddle, regulator, bridge):",
            "  set each in place later, mark through its holes, drill 4 mm",
            "  pilots 10 deep, fix with 5 mm stainless self-tapping screws.",
            "Drip lip: 10 x 10 x 1.5 angle, front 900 and four end pieces;",
            "  screw every 100 mm on a bead of silicone.",
            "Check: the deck lies flat on the frame with every notch clear.",
        ], g("frame", "posts", "lip"), inset_view=(35, -60))
    if n == 103:
        one = C["posts"].shape.solids()[0]
        return _sheet("HBN-DWG-103", ["posts"], "Post", "H2Bench post (make 4) and water post: making sketch",
                      "Aluminium extrusion 20 x 20 mm, 6 mm slot (20 series)", [
            "Posts: cut four lengths of 582 mm, square, and deburr.",
            "Water post: cut one length of 200 mm from the same bar.",
            "Tap the centre hole M5, 12 deep, at both ends of every piece",
            "  (the water post needs the bottom end only).",
            "Each post stands on the frame through a notch in the deck,",
            "  held by inside corner brackets: a front post by two (front and",
            "  back), a rear post by one on its inner side.",
            "The water post is screwed to the deck from below, into its",
            "  tapped end, before the deck goes on the frame.",
            "Before standing a post up, slide in T-nuts: four in the front",
            "  slot of each rear post for the panel screws.",
            "Check: every post upright within 1 mm over its length.",
        ], g("frame", "deck", "top"), view_shape=one, inset_view=(25, -60))
    if n == 104:
        return _sheet("HBN-DWG-104", ["top_rails", "top_brackets"], "Top frame", "H2Bench top frame: making sketch",
                      "Aluminium extrusion 20 x 20 mm and 20-series inside corner brackets", [
            "Cut two rails 860 mm (front and back) and two rails 305 mm (sides).",
            "The front and back rails fit between the post tops; the side",
            "  rails fit between the front and rear posts.",
            "Hold each with inside corner brackets under the rail end",
            "  (front and back rails) or on the inner face (side rails):",
            "  M5 x 10 screws into drop-in T-nuts.",
            "All rail tops flush with the post tops, 570 mm above the deck.",
            "Slide T-nuts into the top slots for the canopy screws before",
            "  closing the frame: 4 per long rail, 2 per side rail.",
            "Check: diagonals across the top equal within 2 mm; the panel's",
            "  top edge just meets the side rails.",
        ], g("posts", "panel"), inset_view=(30, -55))
    if n == 105:
        return _sheet("HBN-DWG-105", ["panel"], "Instrument back panel", "H2Bench instrument back panel: making sketch",
                      "Aluminium composite panel 3 mm, printed face", [
            "Cut the panel to 900 wide x 550 tall.",
            "Have the energy-chain schematic printed on the front before",
            "  drilling, or apply it as a printed vinyl.",
            "Four 5.5 mm holes 10 mm in from each side edge, at 60, 220,",
            "  380 and 530 mm up from the bottom edge, for M5 button heads",
            "  into T-nuts in the rear posts.",
            "Display cut-out 230 x 100 mm, centred, 355 to 455 mm up.",
            "Three stage meter cut-outs 80 x 50 mm, 225 to 275 mm up, with",
            "  left edges 75, 205 and 705 mm from the left side (the meter",
            "  bezels are 10 mm larger and cover the cut edges).",
            "Fit: the back face sits flat on the rear posts; the bottom edge",
            "  rests on the deck with a silicone bead (the panel is the back",
            "  of the drip tray); the top edge meets the side rails.",
            "Check: the panel is flat and square to the deck.",
        ], g("posts", "deck", "meters"), inset_view=(25, -60))
    if n == 106:
        return _sheet("HBN-DWG-106", ["canopy"], "Canopy sheet", "H2Bench canopy sheet: making sketch",
                      "Polycarbonate sheet 3 mm, clear", [
            "Cut the sheet to 900 x 345 mm; keep the film on while working.",
            "Duct hole 106 mm diameter, centre on the middle line, 240 mm",
            "  back from the front edge. Cut with a hole saw at low speed.",
            "Screw holes 6 mm (oversize for heat movement), 10 mm in from the",
            "  edges: front and back at 110 and 330 mm each side of the middle;",
            "  each side 120 and 220 mm back from the front edge.",
            "Hanger holes: two 4.5 mm, 93 mm back from the front edge,",
            "  150 and 200 mm right of the middle.",
            "Fit: lies on the top frame; M5 screws with large washers.",
            "Duct collar: bought 100 mm flanged spigot through the hole,",
            "  flange on top, four M4 screws and a silicone bead.",
            "Check: no cracks from any hole; the sheet lies flat.",
        ], g("top", "posts", "h2g") + [part("Duct collar", ["collar"])], inset_view=(35, -60))
    if n == 107:
        return _sheet("HBN-DWG-107", ["res_stand"], "Reservoir stand", "H2Bench reservoir stand: making sketch",
                      "Aluminium sheet 2 mm, 5052 class", [
            "Cut a blank 114 wide x about 260 long (top 120, legs 58, feet 15;",
            "  check the bend allowance on a scrap first).",
            "Fold the legs down 90 degrees along the two long-side lines, then",
            "  fold the feet outward 90 degrees at the bottom of each leg.",
            "Top 114 x 120 mm, 60 mm above the deck.",
            "Drill two 5.5 mm holes in each foot, 30 and 85 mm from the left",
            "  edge, for 5 mm deck screws.",
            "Fit: feet flat on the deck, left edge against the left front",
            "  post, front foot against the drip lip.",
            "The reservoir stands on the top, held by a band clip to the",
            "  water post (sheet HBN-DWG-103).",
            "Check: the top is level; the stand does not rock.",
        ], g("water") + [part("Water post", ["water_post"])], inset_view=(25, -50))
    if n == 108:
        return _sheet("HBN-DWG-108", ["ely_feet"], "Electrolyzer feet", "H2Bench electrolyzer feet (make 2): making sketch",
                      "Aluminium unequal angle 40 x 20 x 3 mm", [
            "Cut two 70 mm lengths of 40 x 20 x 3 angle; deburr.",
            "Upright 40 mm leg: two 6.5 mm holes 30 mm up from the deck,",
            "  25 mm each side of the middle, for M6 screws into the stack's",
            "  end-plate mounting holes (confirm the holes on the part).",
            "Flat 20 mm leg: two 5.5 mm holes 11.5 mm out from the end plate",
            "  face, 25 mm each side of the middle, for 5 mm deck screws.",
            "Fit: the upright leg bolts flat to the outside face of an end",
            "  plate, below the lower tie rods; the flat leg points outward",
            "  and screws to the deck. The stack's base is 20 mm above the deck.",
            "Check: the stack stands level and does not rock.",
        ], g("ely"), view_shape=C["ely_feet"].shape.solids()[0], inset_view=(25, -40))
    if n == 109:
        return _sheet("HBN-DWG-109", ["col_bracket"], "Column bracket", "H2Bench column bracket: making sketch",
                      "Aluminium sheet 3 mm, 5052 class", [
            "Cut a blank 100 wide x 170 long.",
            "Fold the bottom 23 mm back 90 degrees to make a foot.",
            "Upright face 100 wide x 150 tall.",
            "Drill two 5.5 mm holes in the foot, 14 mm behind the face, at",
            "  20 and 78 mm from the left edge, for 5 mm deck screws.",
            "Drill two 4 mm clip holes 115 mm above the deck, at 20 and",
            "  78 mm from the left edge (the separator and drier centres).",
            "Drill a third 4 mm clip hole 78 mm above the deck, 49 mm from",
            "  the left edge, for the deoxidizer clip.",
            "Fit: stands 5 mm behind the separator; the foot points back.",
            "The separator and drier clips screw to it; the deoxidizer",
            "  stands on the foot and is clipped to it.",
            "Check: upright square to the deck; the clips line up with",
            "  the column centres.",
        ], g("columns", "deox", "arr"), inset_view=(25, 125))
    if n == 110:
        return _sheet("HBN-DWG-110", ["arr_saddle"], "Arrestor saddle", "H2Bench arrestor saddle: making sketch",
                      "HDPE block 16 x 32 x 24 mm", [
            "Cut a block 16 long x 32 wide x 24 tall from 16 mm HDPE.",
            "Bore a 31 mm half-round seat across the top, its centre",
            "  28 mm above the deck (60 mm above the table).",
            "Drill a 4.2 mm hole 10 mm up the middle from below for a",
            "  5 mm self-tapping screw put up through the deck.",
            "Drill two 3 mm pilot holes in the sides for the band clip ends.",
            "Fit: the arrestor lies in the seat, centred on the gas line,",
            "  and the band clip wraps over it into the side holes.",
            "Check: the arrestor sits level with the drier outlet.",
        ], [part("Arrestor", ["arrestor"]), part("Drier", ["drier"])], inset_view=(30, -40))
    if n == 111:
        return _sheet("HBN-DWG-111", ["cradle"], "Tank cradle", "H2Bench tank cradle: making sketch",
                      "HDPE sheet 20 mm", [
            "Cut a 130 x 130 mm square from 20 mm HDPE.",
            "Bore a pocket 112 mm diameter, 10 mm deep, centred, with a",
            "  router and circle jig or a hole saw and chisel.",
            "Four 5.5 mm holes 12 mm in from each corner, for 5 mm",
            "  self-tapping deck screws.",
            "Fit: the cradle sits on the deck inside the four guard rods",
            "  (8 mm clear of their nuts); the tank stands in the pocket,",
            "  1 mm clear all round.",
            "Check: the tank drops in and stands upright without rocking.",
        ], g("tank", "rods"), inset_view=(30, -50))
    if n == 112:
        return _sheet("HBN-DWG-112", ["guard_plate"], "Guard top plate", "H2Bench guard rods and top plate: making sketch",
                      "Aluminium plate 4 mm; M10 stainless threaded rod", [
            "Plate: cut 176 x 176 mm from 4 mm aluminium; cut a 130 x 130",
            "  mm opening in the middle (drill the corners, jigsaw, file).",
            "Four 10.5 mm holes on a 156 mm square (78 mm from the centre).",
            "Rods: cut four M10 stainless threaded rods 363 mm long; file",
            "  the ends and run a nut over each end to clean the thread.",
            "Each rod screws into the tee nut under the deck and is locked by",
            "  a nut and washer on top; the plate is clamped between two nuts",
            "  at the top, 60 mm above the tank top.",
            "The manifold, gauge and lines pass up through the opening.",
            "Check: plate level within 1 mm; the tank lifts out only",
            "  after the plate comes off.",
        ], g("tank", "manifold", "rods"), inset_view=(30, -50))
    if n == 113:
        return _sheet("HBN-DWG-113", ["fc_bridge"], "Fuel cell bridge", "H2Bench fuel cell bridge: making sketch",
                      "Aluminium sheet 2 mm, 5052 class", [
            "Cut a blank 57 wide x about 190 long (top 85, legs 38, feet 15;",
            "  check the bend allowance on a scrap first).",
            "Fold the legs down 90 degrees, then the feet outward 90 degrees.",
            "Top 85 x 57 mm, 40 mm above the deck; front and back left open",
            "  so the stack's fan can draw and blow air through.",
            "Drill the top to the stack's mounting holes (confirm on the part).",
            "Two 5.5 mm holes in each foot, 15 mm each side of the middle,",
            "  for 5 mm deck screws.",
            "Fit: the stack sits on the top, its hydrogen inlet on the left",
            "  side, 5 mm above the bridge top, facing the regulator.",
            "Check: the stack is level; the fan face is clear of the bridge.",
        ], [part("Fuel cell", ["fc"]), part("Regulator", ["reg"])], inset_view=(25, -50))
    if n == 114:
        return _sheet("HBN-DWG-114", ["hanger"], "Outlet hanger", "H2Bench outlet hanger: making sketch",
                      "Aluminium equal angle 20 x 20 x 2 mm", [
            "Cut a 70 mm length of 20 x 20 x 2 angle; deburr.",
            "Flat leg: two 4.5 mm holes, 10 mm from the bend, 10 mm in from",
            "  each end, for M4 screws up through the canopy.",
            "Hanging leg: two 6.5 mm holes for tube clips, 15 mm and 55 mm",
            "  from the left end, 10 mm below the canopy.",
            "Fit: screwed under the canopy above the tank manifold. The",
            "  relief and vent lines are clipped to the hanging leg and end",
            "  7 mm below the canopy, so the gas leaves into the hood.",
            "Check: both line ends open and pointing up.",
        ], [Part("Canopy", win(C["canopy"].shape, 60, 290, -120, 60, 0, 700), "#D1D5DB", None, (0, 0, 0), 1.0),
            Part("Relief and vent lines", win(C["gas_lines"].shape, 140, 210, -60, -20, D["tank_top"], 700), "#D1D5DB", None, (0, 0, 0), 1.0),
            part("Manifold", ["manifold"])], inset_view=(15, -60))
    raise KeyError(n)


SHEETS = list(range(101, 115))


# ----------------------------------------------------------------- joints
def joint(n):
    L, Dd = P["bench_l"], P["bench_d"]
    fy0, fy1 = D["front_post_y"]
    ry0, ry1 = D["rear_post_y"]
    if n == 1:
        bx = (-455, -385, -230, -160, -5, 25)
        return _joint(n, [
            ("Front rail", ["rail_front"], None), ("Left end rail", ["end_l"], "#CBD5E1"),
            ("Inside corner bracket", ["frame_brackets"], "#111827")], bx,
            "Joint 1: frame corner (front left, seen from inside the frame, deck off)",
            "The end rail fits between the long rails; one inside bracket with two M5 screws into T-nuts",
            elev=35, azim=50)
    if n == 2:
        bx = (395, 455, fy0 - 45, fy1 + 45, -2, 75)
        return _joint(n, [("Right end rail", ["end_r"], None), ("Deck (notched)", ["deck"], None),
                          ("Front post", ["posts"], None), ("Foot brackets, front and back", ["post_brackets"], "#111827"),
                          ("Drip lip angle", ["lip"], None)], bx,
                      "Joint 2: front post foot (right side)",
                      "The post stands on the end rail through a notch in the deck; a bracket in front and one behind",
                      elev=28, azim=-150)
    if n == 3:
        bx = (380, 455, fy0 - 5, fy1 + 60, TOP - 60, TOP + 5)
        return _joint(n, [("Front post", ["posts"], "#CBD5E1", (380, 455, fy0 - 5, fy1 + 60, TOP - 110, TOP + 5)),
                          ("Front and side top rails", ["top_rails"], "#94A3B8", (380, 455, fy0 - 5, fy1 + 60, TOP - 60, TOP + 5)),
                          ("Top brackets", ["top_brackets"], "#C2410C")], bx,
                      "Joint 3: top frame corner (front right, seen from inside the hood, canopy off)",
                      "Rails butt against the post; a bracket under the front rail and one inside the side rail; the canopy lies on top",
                      elev=22, azim=145)
    if n == 4:
        bx = (385, 455, ry0 - 30, ry1 + 2, 10, 90)
        return _joint(n, [("Back rail", ["rail_back"], "#6B7280", (385, 428, ry0 - 30, ry1 + 2, 10, 90)),
                          ("Deck", ["deck"], "#E7E5E4", (385, 408, ry0 - 3, ry1 + 2, 10, 90)), ("Rear post", ["posts"], "#64748B"),
                          ("Foot bracket (inner side)", ["post_brackets"], "#C2410C"), ("Instrument panel", ["panel"], "#CBD5E1")], bx,
                      "Joint 4: panel foot and rear post (right side, seen from behind)",
                      "The panel screws to the post's front face and stands on the deck on a silicone bead; the foot bracket sits inside the post",
                      elev=50, azim=140)
    if n == 5:
        ex1 = D["ex1"]
        bx = (ex1 - 45, ex1 + 25, GY - 60, GY + 40, DT - 12, DT + 75)
        return _joint(n, [("Deck", ["deck"], None), ("Right end plate", ["ely"], None),
                          ("Cell plates", ["ely_cells"], None), ("Foot, 40 x 20 x 3 angle", ["ely_feet"], None)], bx,
                      "Joint 5: electrolyzer foot (right end)",
                      "The upright leg bolts to the end plate (two M6); the flat leg screws to the deck (two M5)",
                      elev=22, azim=-35)
    if n == 6:
        TX = P["tank_x"]
        bx = (TX - 100, TX + 100, GY - 100, GY, -2, DT + 70)
        return _joint(n, [("Deck", ["deck"], None), ("Tank cradle", ["cradle"], None), ("Tank base", ["tank"], None),
                          ("Guard rods", ["guard_rods"], None), ("Nuts above and below the deck", ["guard_nuts"], "#111827")], bx,
                      "Joint 6: tank in its cradle, guard rods through the deck (cut open)",
                      "Cut through the tank axis. The tank stands 10 mm deep in the pocket; each rod has a nut each side of the deck",
                      elev=18, azim=-70)
    if n == 7:
        sx_, dx7 = P["sep_x"], P["drier_x"]
        bx = (sx_ - 45, dx7 + 30, GY - 40, GY + 85, DT + 60, DT + 121)
        return _joint(n, [("Separator", ["sep"], None), ("Drier", ["drier"], None), ("Column bracket", ["col_bracket"], None),
                          ("Pipe clips", ["col_clips", "deox_clip"], "#111827"), ("Catalytic deoxidizer", ["deox"], "#7C3AED")], bx,
                      "Joint 7: separator, drier and deoxidizer clipped to the column bracket",
                      "Seen from above the front, columns cut above the clips; the deoxidizer stands on the foot behind",
                      elev=55, azim=-70)
    if n == 8:
        ax0, ax1 = P["arr_x"]
        bx = (ax0 - 15, ax1 + 10, GY - 30, GY + 25, DT - 2, P["arr_z"] + 25)
        return _joint(n, [("Deck", ["deck"], None), ("Arrestor saddle", ["arr_saddle"], None),
                          ("Check valve and arrestor", ["arrestor"], None), ("Band clip", ["arr_clip"], "#111827"),
                          ("Drier outlet", ["drier"], None)], bx,
                      "Joint 8: arrestor on its saddle",
                      "The arrestor screws straight onto the drier outlet and rests in the saddle seat",
                      elev=25, azim=-60)
    if n == 9:
        dx_, dy_ = P["duct_x"], P["duct_y"]
        bx = (dx_ - 90, dx_ + 90, dy_ - 90, dy_, TOP - 30, D["duct_top"] + 55)
        return _joint(n, [("Canopy sheet", ["canopy"], "#93C5FD"), ("Duct collar and flange", ["collar"], None),
                          ("H2Guard fan and sensor", ["h2guard"], "#DC2626")], bx,
                      "Joint 9: duct collar through the canopy (cut open)",
                      "Seen from behind the cut. The spigot passes through a 106 mm hole; the flange sits on a silicone bead; the fan sits on the spigot",
                      elev=15, azim=115)
    raise KeyError(n)


def _joint(n, items, bx, title, sub, elev=24, azim=-58):
    ps = []
    for it in items:
        name, keys, col = it[:3]
        sh = win(S(*keys), *(it[3] if len(it) > 3 else bx))
        ps.append(Part(name, sh, col or C[keys[0]].color, None, (0, 0, 0), 1.0))
    return bv.joint(ps, OUT / f"joint-{n:02d}.png", title, subtitle=sub, elev=elev, azim=azim, size=(8, 6))


JOINTS = list(range(1, 10))


# ----------------------------------------------------------------- assembly steps
def _done(upto):
    keys = [k for k, *_ in ORDER]
    return [M[k] for k in keys[:keys.index(upto)]] if upto else []


STEPS = [
    (1, None, [("frame", (0, 0, 0))], "frame rails and corner brackets",
     "Rails upside down on a flat bench; one inside bracket at each meeting; T-nuts in the top slots", dict(elev=35, azim=-55)),
    (2, "deck", [("deck", (0, 0, 120)), ("lip", (0, -60, 200))], "deck and drip lip onto the frame",
     "Countersunk M5 screws into the T-nuts; lip angles screwed every 100 mm on a silicone bead", dict(elev=30, azim=-55)),
    (3, "posts", [("posts", (0, 0, 200))], "posts onto the frame",
     "Each post through its deck notch onto the frame; front posts two brackets, rear posts one", dict(elev=22, azim=-55)),
    (4, "panel", [("panel", (0, 200, 0)), ("top", (0, 0, 180))], "instrument panel and top frame",
     "Panel on the rear posts, four M5 each side, silicone at its foot; then the four top rails and brackets", dict(elev=22, azim=-55)),
    (5, "canopy", [("canopy", (0, 0, 180))], "canopy, duct collar and outlet hanger",
     "Sheet on the top frame with M5 screws and large washers; collar flange on silicone; hanger under the sheet", dict(elev=25, azim=-55)),
    (6, "stand", [("stand", (0, -160, 0)), ("water", (0, -160, 160))], "reservoir stand, water post, reservoir and cartridge",
     "Stand and post screwed to the deck; reservoir on the stand; band clips round both vessels to the post", dict(elev=22, azim=-40)),
    (7, "feet", [("feet", (0, -120, 0)), ("ely", (0, -120, 180))], "electrolyzer on its feet",
     "Feet bolted to the end plates first (two M6 each), then the stack set down and the feet screwed to the deck", dict(elev=22, azim=-40)),
    (8, "colbr", [("colbr", (0, 120, 0)), ("columns", (0, -140, 120)), ("deox", (0, 40, 220)), ("arr", (0, -140, 60))],
     "column bracket, separator, deoxidizer, drier and arrestor",
     "Bracket and saddle down; separator, drier and deoxidizer clipped on; arrestor on the drier outlet", dict(elev=22, azim=-40)),
    (9, "cradle", [("cradle", (0, -120, 0)), ("rods", (0, 0, 160)), ("tank", (0, 0, 300))], "cradle, guard rods and tank",
     "Cradle screwed down; rods through the deck with a nut each side; tank lowered into the pocket", dict(elev=22, azim=-40)),
    (10, "manifold", [("manifold", (0, 0, 180)), ("gplate", (0, 0, 320))], "tank manifold and guard top plate",
     "Manifold into the tank neck on hydrogen thread sealant; plate onto the rods, nut below and above", dict(elev=22, azim=-40)),
    (11, "reg", [("reg", (0, 0, 170)), ("fc", (0, 0, 280)), ("load", (0, -150, 0))], "regulator, fuel cell and load",
     "Regulator and bridge screwed down; stack screwed to the bridge; load case screwed to the deck", dict(elev=25, azim=-25)),
    (12, "lines", [("lines", (0, -120, 120))], "gas and water lines",
     "Cut each line square, deburr, compression fittings; relief and vent lines clipped to the hanger. Hold point: leak check", dict(elev=22, azim=-50)),
    (13, "psu", [("psu", (-120, 0, 0)), ("meters", (0, -160, 0))], "power supply, meters and wiring",
     "Meters into the panel cut-outs; supply stood on the lab table beside the bench; wire as the wiring diagram. Hold point: wiring checks", dict(elev=22, azim=-50)),
    (14, "h2g", [("h2g", (0, 0, 200))], "H2Guard sensor, fan and controller",
     "Sensor under the canopy beside the duct, fan on the collar, controller on the canopy; interlock wired to the supply cut", dict(elev=25, azim=-55)),
]


def step(n):
    for num, upto, new, title, sub, kw in STEPS:
        if num != n:
            continue
        done = _done(upto or new[0][0])
        news = [mv(M[k], e) for k, e in new]
        return bv.step(done, news, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, label_done=False, **kw)
    raise KeyError(n)


# ----------------------------------------------------------------- block diagrams
def _fig(title, sub, size=(12, 7.2)):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=size, dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    ax.text(2, 70, title, fontsize=13, fontweight="bold", color="#111827", va="top")
    ax.text(2, 66.6, sub, fontsize=8.5, color="#4B5563", va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/h2bench", fontsize=7, color="#0F766E", ha="right", family="monospace")
    return fig, ax, plt


def _blk(ax, x, y, w, h, title, sub, color):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8, zorder=2))
    ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color="#111827", zorder=3)
    if sub:
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7, color="#4B5563", linespacing=1.3, zorder=3)


def _wire(ax, pts, color, lw=2.0, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=1)


def _lab(ax, x, y, text, color, ha="left"):
    ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=4,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def piping():
    fig, ax, plt = _fig("H2Bench prototype: gas and water lines",
                        "Every line is 6 mm tubing with compression fittings rated for hydrogen. Flow runs left to right. Pressures are kPa gauge.")
    H2, W, O2, V = "#0F766E", "#0284C7", "#B91C1C", "#6B7280"
    _blk(ax, 3, 40, 14, 12, "Reservoir", "on its stand,\nvented lid", W)
    _blk(ax, 3, 18, 14, 12, "Deionizer", "mixed-bed\ncartridge", W)
    _blk(ax, 24, 30, 15, 16, "Electrolyzer", "water and oxygen\nside on the left\nend plate; hydrogen\nout on the right", H2)
    _blk(ax, 44, 34, 9.5, 12, "Separator", "drain valve\nat the foot", H2)
    _blk(ax, 55, 34, 9.5, 12, "Deoxidizer", "catalyst\ncartridge", "#7C3AED")
    _blk(ax, 66, 34, 8.5, 12, "Drier", "silica gel", H2)
    _blk(ax, 64, 13, 11, 13, "Check valve,\narrestor", "\n\n7 kPa check", H2)
    _blk(ax, 78, 30, 14, 16, "Tank, 2 L", "manifold: pressure,\ntemperature, gauge,\nrelief, vent, cut\nswitch", H2)
    _blk(ax, 97, 34, 10, 12, "Solenoid,\nregulator", "", H2)
    _blk(ax, 107, 15, 11, 11, "Fuel cell", "about 50 kPa", H2)
    _blk(ax, 76, 55, 30, 6, "Outlet hanger under the canopy", "", V)
    # water
    _wire(ax, [(10, 40), (10, 30)], W); _lab(ax, 10.6, 35, "side outlet to\ncartridge inlet", W)
    _wire(ax, [(17, 24), (21, 24), (21, 34), (24, 34)], W); _lab(ax, 17.2, 21.6, "cartridge out to stack\nwater inlet (low)", W)
    _wire(ax, [(24, 43), (20, 43), (20, 48), (17, 48)], O2); _lab(ax, 18, 50.6, "oxygen and water back\nto the reservoir top", O2)
    ax.text(10, 54, "oxygen leaves through the vented lid\ninto the hood", fontsize=7, color=O2, ha="center")
    # hydrogen
    _wire(ax, [(39, 40), (44, 40)], H2); _lab(ax, 41.5, 42, "H2", H2, "center")
    _wire(ax, [(53.5, 44), (55, 44)], H2)
    _wire(ax, [(64.5, 44), (66, 44)], H2)
    _wire(ax, [(70.2, 34), (70.2, 26)], H2); _lab(ax, 70.8, 30, "drier out", H2)
    _wire(ax, [(75, 20), (76.5, 20), (76.5, 36), (78, 36)], H2)
    _wire(ax, [(92, 40), (97, 40)], H2); ax.text(94.5, 41.2, "0 to\n300", fontsize=6.6, color=H2, ha="center", va="bottom")
    _wire(ax, [(102, 34), (102, 22), (107, 22)], H2); _lab(ax, 102.6, 28, "about 50", H2)
    _wire(ax, [(82, 46), (82, 55)], V, ls="--"); _lab(ax, 82.6, 50.5, "relief, 325", V)
    _wire(ax, [(88, 46), (88, 55)], V, ls="--"); _lab(ax, 88.6, 50.5, "vent valve", V)
    _wire(ax, [(48.7, 34), (48.7, 28)], W, lw=1.2, ls=":"); _lab(ax, 49.2, 26.5, "drained by hand\nat 20 kPa", W)
    ax.text(3, 8.6, "Never open a fitting under pressure. The relief and vent lines end 7 mm below the canopy, so gas they release rises to the H2Guard sensor and the duct.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 5.4, "Blue: water. Red: oxygen with water. Teal: hydrogen. Grey dashed: relief and vent into the hood.", fontsize=7.2, color="#4B5563")
    out = OUT / "piping.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def wiring():
    fig, ax, plt = _fig("H2Bench prototype: power, cut and interlock wiring",
                        "Block level. The supply cut and the H2Guard interlock are hardwired and work without the logger firmware.")
    RED, BLU, GRY, AMB = "#B91C1C", "#1D4ED8", "#6B7280", "#B45309"
    _blk(ax, 3, 44, 14, 12, "Mains socket", "with plug-in\n30 mA RCD", AMB)
    _blk(ax, 22, 44, 15, 12, "Bench supply", "0 to 30 V, 10 A,\nconstant current", "#374151")
    _blk(ax, 43, 44, 15, 12, "Cut relay", "10 A DC or more,\nopens the + line", RED)
    _blk(ax, 64, 44, 15, 12, "Stage 1 meter", "power monitor\nand shunt", "#15803D")
    _blk(ax, 85, 44, 15, 12, "Electrolyzer", "about 7.8 V, 9 A", "#0F766E")
    _blk(ax, 43, 24, 15, 11, "Cut switch", "on the manifold,\nopens at 310 kPa", RED)
    _blk(ax, 22, 24, 15, 11, "H2Guard", "relay output\nin series", "#DC2626")
    _blk(ax, 64, 24, 15, 11, "Logger", "display, 1 Hz CSV,\npressure, temperature", "#15803D")
    _blk(ax, 85, 24, 15, 11, "Fuel cell", "stage 3 meter,\nload and lamp", "#1F2937")
    _blk(ax, 103, 44, 15, 12, "Tank solenoid", "12 V, normally\nclosed", "#D4A017")
    _wire(ax, [(17, 50), (22, 50)], AMB); _lab(ax, 19.5, 52, "mains", AMB, "center")
    _wire(ax, [(37, 50), (43, 50)], RED); ax.text(40, 51, "+ line\n2.5 mm²", fontsize=6.6, color=RED, ha="center", va="bottom")
    _wire(ax, [(58, 50), (64, 50)], RED); _wire(ax, [(79, 50), (85, 50)], RED); ax.text(82, 51, "2.5 mm²", fontsize=6.6, color=RED, ha="center", va="bottom")
    _wire(ax, [(50.5, 35), (50.5, 44)], GRY, 1.4); _lab(ax, 51, 39.5, "coil, 12 V,\nthrough the switch", GRY)
    _wire(ax, [(37, 29), (43, 29)], GRY, 1.4); _lab(ax, 40, 31, "in series", GRY, "center")
    _wire(ax, [(29.5, 24), (29.5, 18), (110, 18), (110, 44)], GRY, 1.4); _lab(ax, 70, 16.3, "H2Guard also cuts the solenoid's 12 V (closes the tank)", GRY, "center")
    _wire(ax, [(71.5, 44), (71.5, 35)], BLU, 1.2); _lab(ax, 72, 39.5, "I2C", BLU)
    _wire(ax, [(85, 29.5), (79, 29.5)], BLU, 1.2); _lab(ax, 82, 31.4, "I2C", BLU, "center")
    ax.text(3, 10.2, "Safety: the supply is mains powered. Use an earthed supply on the RCD, keep the mains lead off the wet deck, and do not power up until",
            fontsize=7.6, color=AMB, fontweight="bold")
    ax.text(3, 7.6, "the safety stops in section 6 of the plan are passed. Fuse the 12 V control supply at 1 A.",
            fontsize=7.6, color=AMB, fontweight="bold")
    ax.text(3, 4.6, "Red: electrolyzer power. Grey: cut and interlock circuit (any open contact stops the electrolyzer). Blue: measurement.", fontsize=7.2, color="#4B5563")
    out = OUT / "wiring.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "diagrams"]
    OUT.mkdir(parents=True, exist_ok=True)
    for a in args:
        if a == "overview":
            print(overview())
        elif a == "sheets":
            for n in SHEETS:
                print(sheet(n))
        elif a == "joints":
            for n in JOINTS:
                print(joint(n))
        elif a == "steps":
            for num, *_ in STEPS:
                print(step(num))
        elif a == "diagrams":
            print(piping()); print(wiring())
        elif ":" in a:
            kind, n = a.split(":")
            print({"sheet": sheet, "joint": joint, "step": step}[kind](int(n)))
        else:
            raise SystemExit(f"unknown: {a}")
