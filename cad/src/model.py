"""H2Bench parametric model (build123d), TRL 3, constructable design (HBN-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    runs the constructability checks only

Every part is modelled as it is made or bought: cut extrusion, folded sheet, drilled plate,
threaded rod, bought vessel. build_components() returns each part separately (used by the build
plan pictures and the checks); build_parts() groups them into the 15 numbered BOM items used by
the concept media, the general arrangement drawing and the appearance model.

Axes: X along the bench, left to right in the order the energy flows (water and power in,
electrolyzer, gas treatment, buffer tank, regulator, fuel cell, load). Y front (-Y, student
side) to back (+Y, instrument panel). Z up; Z = 0 is the top of the existing lab table.
Units mm.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Bench (HBN-REQ-001 R13)
    "bench_l": 900.0, "bench_d": 450.0,
    "frame_h": 20.0,            # 20 x 20 mm aluminium extrusion, 6 mm slot
    "deck_t": 10.0,             # HDPE deck (10 mm, decided 2026-10-02)
    "lip_h": 10.0,              # drip lip: 10 x 10 x 1.5 mm aluminium angle on the deck edge
    "lip_t": 1.5,
    "panel_t": 3.0, "panel_y": 202.0,   # instrument panel front face... back face on the rear posts
    "panel_standoff": 0.0,      # kept for older scripts; the panel now sits flat on the rear posts
    "canopy_clear": 570.0,      # deck top to canopy underside
    "canopy_t": 3.0, "canopy_front_y": -120.0,
    "post": 20.0,
    "bracket": (20.0, 4.0),     # 20-series inside corner bracket: leg length, thickness
    "duct_d": 100.0, "duct_h": 100.0, "duct_x": 0.0, "duct_y": 120.0, "collar_flange_d": 140.0,
    # Gas train centreline
    "gas_y": -40.0, "tube_od": 6.0,
    # 4 Bench power supply (L x D x H)
    "psu": (150.0, 210.0, 140.0), "psu_x0": -630.0, "psu_y0": -105.0,   # beside the bench on the lab table (2026-10-02)
    # 5 Reservoir (on a folded stand) and deionizer cartridge, held to a short post
    "res_d": 110.0, "res_h": 170.0, "res_x": -370.0, "res_y": -140.0, "res_stand_h": 60.0,
    "di_d": 50.0, "di_h": 150.0, "di_x": -268.0, "di_y": -150.0,
    # 6 PEM electrolyzer: 4 cells, 56 cm2 active area class, 25 mm cell pitch, on two angle feet
    "ely_cells": 4, "ely_pitch": 25.0, "ely_plate": 90.0, "ely_end_t": 15.0,
    "ely_x0": -215.0, "ely_lift": 20.0,
    # 7 Separator and drier on a folded column bracket
    "sep_d": 60.0, "sep_h": 160.0, "sep_x": -28.0, "drier_d": 40.0, "drier_h": 130.0, "drier_x": 30.0,
    # 19 Catalytic deoxidizer between separator and drier (decided 2026-10-02): a vertical cartridge
    #    standing on the column bracket's foot, clipped to its plate, two ports on top
    "deox_d": 32.0, "deox_h": 120.0, "deox_x": 1.0,
    # 8 Check valve and flame arrestor, on a saddle block
    "arr_x": (55.0, 105.0), "arr_d": 28.0, "arr_z": 60.0,
    # 9 Buffer tank: internal volume is the design input, cylinder length follows from it
    "tank_v_l": 2.0, "tank_od": 110.0, "tank_wall": 3.0, "tank_x": 175.0,
    "cradle": (130.0, 20.0), "cradle_pocket": (112.0, 10.0),
    "guard_offset": 78.0, "guard_rod_d": 10.0, "guard_top_gap": 60.0, "guard_plate": (176.0, 130.0, 4.0),
    # 11 Regulator and solenoid
    "reg_x": 280.0,
    # 12 Fuel cell stack: 75 x 47 x 70 mm with fan (Fuel Cell Store listing for the 12 W class)
    "fc": (75.0, 47.0, 70.0), "fc_x0": 345.0, "fc_stand_h": 40.0,
    # 13 Load and lamp
    "load": (140.0, 55.0, 50.0), "load_x0": 300.0, "load_y0": -215.0,
}


def tank_cyl_len(p=PARAMS):
    """Internal straight length of the tank (mm) for the set internal volume: flat base,
    cylindrical body and a hemispherical top."""
    r = p["tank_od"] / 2 - p["tank_wall"]
    v = p["tank_v_l"] * 1e6
    return (v - 2 / 3 * math.pi * r ** 3) / (math.pi * r ** 2)


def tank_internal_volume_l(p=PARAMS):
    r = p["tank_od"] / 2 - p["tank_wall"]
    return (math.pi * r ** 2 * tank_cyl_len(p) + 2 / 3 * math.pi * r ** 3) / 1e6


def levels(p=PARAMS):
    deck_top = p["frame_h"] + p["deck_t"]
    top = deck_top + p["canopy_clear"]            # canopy underside
    return deck_top, top


def derived(p=PARAMS):
    """Positions that several parts share (mm)."""
    deck_top, top = levels(p)
    L, D, s = p["bench_l"], p["bench_d"], p["post"]
    tz0 = deck_top + p["cradle"][1] - p["cradle_pocket"][1]          # tank base sits in the cradle pocket
    tz1 = tz0 + p["tank_wall"] + tank_cyl_len(p)
    tank_top = tz1 + p["tank_od"] / 2
    ez0 = deck_top + p["ely_lift"]
    n, pitch, et = p["ely_cells"], p["ely_pitch"], p["ely_end_t"]
    ex1 = p["ely_x0"] + 2 * et + n * pitch
    return {
        "deck_top": deck_top, "top": top, "rail_top": top - s,
        "front_post_y": (p["canopy_front_y"], p["canopy_front_y"] + s),
        "rear_post_y": (D / 2 - s, D / 2),
        "panel_y": (p["panel_y"], p["panel_y"] + p["panel_t"]),
        "tz0": tz0, "tz1": tz1, "tank_top": tank_top, "g_top": tank_top + p["guard_top_gap"],
        "ez0": ez0, "ex1": ex1, "ezc": ez0 + (p["ely_plate"] + 20) / 2,
        "res_z0": deck_top + p["res_stand_h"],
        "fz0": deck_top + p["fc_stand_h"],
        "duct_top": top + p["canopy_t"] + p["duct_h"],
    }


def envelope(p=PARAMS):
    """Overall bench envelope above the lab table (mm): length, depth, height."""
    d = derived(p)
    height = d["duct_top"] + 50.0          # H2Guard fan housing is 50 mm on the duct
    return p["bench_l"], p["bench_d"], height


# ----------------------------------------------------------------- geometry helpers
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _vcyl(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, abs(z1 - z0))


def _xcyl(x0, x1, y, z, r):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def _ycyl(x, y0, y1, z, r):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, abs(y1 - y0))


def _ring(x, y, z0, z1, r0, r1):
    return _vcyl(x, y, z0, z1, r1) - _vcyl(x, y, z0 - 1, z1 + 1, r0)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _corner(c, a, b, w, p=PARAMS):
    """20-series inside corner bracket. c: a point on the inside corner line; a and b: unit axis
    vectors along the two faces it sits on (leg A lies on the face whose normal is b, leg B on the
    face whose normal is a); w: the axis the bracket's width runs along from c."""
    L, t = p["bracket"]
    W = 20.0

    def pt(*terms):
        return tuple(c[i] + sum(k * v[i] for k, v in terms) for i in range(3))
    a0, a1 = c, pt((L, a), (t, b), (W, w))
    b0, b1 = c, pt((L, b), (t, a), (W, w))
    return (_box(a0[0], a1[0], a0[1], a1[1], a0[2], a1[2])
            + _box(b0[0], b1[0], b0[1], b1[1], b0[2], b1[2]))


def _tube(points, r):
    """A tube along a path of axis-aligned straight runs, with a ball at each bend."""
    from build123d import Pos, Sphere
    segs = []
    for (x0, y0, z0), (x1, y1, z1) in zip(points[:-1], points[1:]):
        if abs(x1 - x0) > 1e-6:
            segs.append(_xcyl(x0, x1, y0, z0, r))
        elif abs(y1 - y0) > 1e-6:
            segs.append(_ycyl(x0, y0, y1, z0, r))
        else:
            segs.append(_vcyl(x0, y0, z0, z1, r))
    for q in points[1:-1]:
        segs.append(Pos(*q) * Sphere(r))
    return _union(segs)


def _hat(x0, x1, y0, y1, z_top, z_base, t, legs="x", foot=15.0):
    """A folded sheet stand: a flat top, two legs folded down along two opposite edges and a foot
    folded outward at the bottom of each leg. legs='x': legs at the x0 and x1 edges."""
    top = _box(x0, x1, y0, y1, z_top - t, z_top)
    if legs == "x":
        return (top + _box(x0, x0 + t, y0, y1, z_base, z_top) + _box(x1 - t, x1, y0, y1, z_base, z_top)
                + _box(x0 - foot, x0 + t, y0, y1, z_base, z_base + t) + _box(x1 - t, x1 + foot, y0, y1, z_base, z_base + t))
    return (top + _box(x0, x1, y0, y0 + t, z_base, z_top) + _box(x0, x1, y1 - t, y1, z_base, z_top)
            + _box(x0, x1, y0 - foot, y0 + t, z_base, z_base + t) + _box(x0, x1, y1 - t, y1 + foot, z_base, z_base + t))


# ----------------------------------------------------------------- components
class C:
    """One component: what it is, its shape, colour, BOM line and the group it belongs to."""
    def __init__(self, name, shape, color, bom, group, made=False):
        self.name, self.shape, self.color, self.bom, self.group, self.made = name, shape, color, bom, group, made


def build_components(p=PARAMS):
    """Every part separately, keyed by a short id, in build order."""
    from build123d import Pos, Sphere
    b, vc, xc, yc = _box, _vcyl, _xcyl, _ycyl
    d = derived(p)
    L, D, s = p["bench_l"], p["bench_d"], p["post"]
    fh, DT, TOP, RT = p["frame_h"], d["deck_top"], d["top"], d["rail_top"]
    GY, tr = p["gas_y"], p["tube_od"] / 2
    fy0, fy1 = d["front_post_y"]
    ry0, ry1 = d["rear_post_y"]
    py0, py1 = d["panel_y"]
    out = {}

    def add(key, *a, **k):
        out[key] = C(*a, **k)

    # 1 Frame: two long rails 900, two end rails and two cross rails 410 between them, inside brackets
    add("rail_front", "Front rail", b(-L / 2, L / 2, -D / 2, -D / 2 + s, 0, fh), "#9CA3AF", 1, "frame", True)
    add("rail_back", "Back rail", b(-L / 2, L / 2, D / 2 - s, D / 2, 0, fh), "#9CA3AF", 1, "frame", True)
    xc_ = L / 6
    for k, x0 in (("end_l", -L / 2), ("cross_l", -xc_ - s / 2), ("cross_r", xc_ - s / 2), ("end_r", L / 2 - s)):
        add(k, {"end_l": "Left end rail", "end_r": "Right end rail", "cross_l": "Left cross rail",
                "cross_r": "Right cross rail"}[k], b(x0, x0 + s, -D / 2 + s, D / 2 - s, 0, fh), "#9CA3AF", 1, "frame", True)
    fb = []
    for sy in (-1, 1):
        yy = sy * (D / 2 - s)
        fb.append(_corner((-L / 2 + s, yy, 0), (1, 0, 0), (0, -sy, 0), (0, 0, 1)))
        fb.append(_corner((L / 2 - s, yy, 0), (-1, 0, 0), (0, -sy, 0), (0, 0, 1)))
        for xx in (-xc_ + s / 2, xc_ + s / 2):
            fb.append(_corner((xx, yy, 0), (1, 0, 0), (0, -sy, 0), (0, 0, 1)))
    add("frame_brackets", "Frame corner brackets (8)", _union(fb), "#4B5563", 1, "frame")

    # 1 Deck: HDPE 900 x 450 x 12, notched round the four posts and their foot brackets
    deck = b(-L / 2, L / 2, -D / 2, D / 2, fh, DT)
    for sx in (-1, 1):
        deck = deck - b(sx * (L / 2 - s), sx * L / 2, fy0 - 20, fy1 + 20, fh - 1, DT + 1)
        deck = deck - b(sx * (L / 2 - 2 * s), sx * L / 2, ry0, ry1, fh - 1, DT + 1)
    add("deck", "Deck", deck, "#E5E7EB", 1, "frame", True)

    # 1 Drip lip: 10 x 10 x 1.5 aluminium angle on the front and end edges (the panel closes the back)
    lh, lt = p["lip_h"], p["lip_t"]

    def lip_x(x0, x1):          # along the front edge
        y0 = -D / 2
        return b(x0, x1, y0, y0 + lh, DT, DT + lt) + b(x0, x1, y0, y0 + lt, DT, DT + lh)

    def lip_y(sx, y0, y1):      # along an end edge
        x0 = sx * L / 2
        return b(x0, x0 - sx * lh, y0, y1, DT, DT + lt) + b(x0, x0 - sx * lt, y0, y1, DT, DT + lh)
    lip = lip_x(-L / 2, L / 2)
    for sx in (-1, 1):
        lip = lip + lip_y(sx, -D / 2 + lh, fy0 - 20) + lip_y(sx, fy1 + 20, py0)
    add("lip", "Drip lip angles (5)", lip, "#6B7280", 1, "frame", True)

    # 3 Posts: four 20 x 20 extrusions from the frame top to the canopy underside, each held by
    #   inside corner brackets on the frame (deck notched round them)
    posts, pb = [], []
    for sx in (-1, 1):
        xo, xi = sx * L / 2, sx * (L / 2 - s)
        posts.append(b(xi, xo, fy0, fy1, fh, TOP))
        posts.append(b(xi, xo, ry0, ry1, fh, TOP))
        pb.append(_corner((min(xi, xo), fy0, fh), (0, -1, 0), (0, 0, 1), (1, 0, 0)))
        pb.append(_corner((min(xi, xo), fy1, fh), (0, 1, 0), (0, 0, 1), (1, 0, 0)))
        pb.append(_corner((xi, ry0, fh), (-sx, 0, 0), (0, 0, 1), (0, 1, 0)))
    add("posts", "Posts (4)", _union(posts), "#64748B", 3, "hood", True)
    add("post_brackets", "Post foot brackets (6)", _union(pb), "#4B5563", 3, "hood")

    # 2 Instrument panel: 3 mm aluminium composite on the front faces of the rear posts
    panel = b(-L / 2, L / 2, py0, py1, DT, RT) - b(-115, 115, py0 - 1, py1 + 1, DT + 355, DT + 455)
    for mx in (-380, -250, 250):
        panel = panel - b(mx + 5, mx + 85, py0 - 1, py1 + 1, DT + 225, DT + 275)
    for sx in (-1, 1):
        for zz in (60, 220, 380, 530):
            panel = panel - yc(sx * (L / 2 - 10), py0 - 1, py1 + 1, DT + zz, 2.75)
    add("panel", "Instrument back panel", panel, "#D1D5DB", 2, "panel", True)

    # 3 Top frame: front and back rails between the posts, side rails between front and rear posts
    tf = (b(-L / 2 + s, L / 2 - s, fy0, fy1, RT, TOP) + b(-L / 2 + s, L / 2 - s, ry0, ry1, RT, TOP))
    tb = []
    for sx in (-1, 1):
        xo, xi = sx * L / 2, sx * (L / 2 - s)
        tf = tf + b(xi, xo, fy1, ry0, RT, TOP)
        for yy in (fy0, ry0):
            tb.append(_corner((xi, yy, RT), (-sx, 0, 0), (0, 0, -1), (0, 1, 0)))
        tb.append(_corner((xi, fy1, RT), (0, 1, 0), (-sx, 0, 0), (0, 0, 1)))
        tb.append(_corner((xi, ry0, RT), (0, -1, 0), (-sx, 0, 0), (0, 0, 1)))
    add("top_rails", "Top frame rails (4)", tf, "#64748B", 3, "hood", True)
    add("top_brackets", "Top frame brackets (8)", _union(tb), "#4B5563", 3, "hood")

    # 3 Canopy: 3 mm polycarbonate on the top frame, 106 mm hole for a bought flanged duct collar
    cy0, dr, ct = p["canopy_front_y"], p["duct_d"] / 2, p["canopy_t"]
    dxy = (p["duct_x"], p["duct_y"])
    canopy = b(-L / 2, L / 2, cy0, D / 2, TOP, TOP + ct) - vc(*dxy, TOP - 1, TOP + ct + 1, dr + 3)
    for xx in (-330, -110, 110, 330):
        for yy in ((fy0 + fy1) / 2, (ry0 + ry1) / 2):
            canopy = canopy - vc(xx, yy, TOP - 1, TOP + ct + 1, 3)
    for sx in (-1, 1):
        for yy in (0, 100):
            canopy = canopy - vc(sx * (L / 2 - s / 2), yy, TOP - 1, TOP + ct + 1, 3)
    for xx in (p["tank_x"] - 25, p["tank_x"] + 25):
        canopy = canopy - vc(xx, GY + 13, TOP - 1, TOP + ct + 1, 2.25)
    add("canopy", "Canopy sheet", canopy, "#BFDBFE", 3, "hood", True)
    collar = (_ring(*dxy, TOP, d["duct_top"], dr, dr + 3)
              + _ring(*dxy, TOP + ct, TOP + ct + 2, dr, p["collar_flange_d"] / 2))
    add("collar", "Duct collar, flanged", collar, "#93C5FD", 3, "hood")

    # 4 Bench DC power supply (bought; stands on its own feet on the lab table beside the bench)
    pl, pd, ph = p["psu"]
    x0, y0 = p["psu_x0"], p["psu_y0"]
    psu = b(x0, x0 + pl, y0, y0 + pd, 0, ph) + b(x0 + 10, x0 + pl - 10, y0 - 4, y0, 30, ph - 20)
    add("psu", "Bench DC power supply", psu, "#374151", 4, "psu")

    # 5 Reservoir on a folded 2 mm aluminium stand; deionizer cartridge; both banded to a short post
    rx, ry, rr = p["res_x"], p["res_y"], p["res_d"] / 2
    rz0 = d["res_z0"]
    stand = _hat(rx - 60, rx + 54, ry - 60, ry + 60, rz0, DT, 2.0, legs="y")
    for xx in (rx - 30, rx + 25):
        for yy in (ry - 67.5, ry + 67.5):
            stand = stand - vc(xx, yy, DT - 1, DT + 3, 2.75)
    add("res_stand", "Reservoir stand", stand,
        "#A8A29E", 5, "water", True)
    res = vc(rx, ry, rz0, rz0 + p["res_h"], rr) + yc(rx, ry + rr - 1, ry + rr + 12, rz0 + 18, 5)
    add("reservoir", "DI water reservoir", res, "#38BDF8", 5, "water")
    dx_, dy_, drr = p["di_x"], p["di_y"], p["di_d"] / 2
    di = (vc(dx_, dy_, DT, DT + p["di_h"], drr) + vc(dx_, dy_, DT + p["di_h"], DT + p["di_h"] + 12, 5)
          + yc(dx_, dy_ + drr - 1, dy_ + drr + 12, DT + 18, 5))
    add("di", "Deionizer cartridge", di, "#7DD3FC", 5, "water")
    wpx = rx + rr + 1                                   # the post's left face touches the reservoir band
    add("water_post", "Water post", b(wpx, wpx + s, -155, -135, DT, DT + 200), "#64748B", 5, "water", True)
    bands = (_ring(rx, ry, rz0 + 120, rz0 + 130, rr, rr + 1) + _ring(dx_, dy_, DT + 95, DT + 105, drr, dx_ - (wpx + s)))
    add("water_bands", "Band clips (2)", bands, "#111827", 5, "water")

    # 6 PEM electrolyzer (bought) on two 40 x 20 x 3 angle feet bolted to its end plates
    ex0, n, pitch, pp, et = p["ely_x0"], p["ely_cells"], p["ely_pitch"], p["ely_plate"], p["ely_end_t"]
    ez0, ex1, ezc = d["ez0"], d["ex1"], d["ezc"]
    hp = (pp + 20) / 2
    ely = (b(ex0, ex0 + et, GY - hp, GY + hp, ez0, ez0 + pp + 20)
           + b(ex1 - et, ex1, GY - hp, GY + hp, ez0, ez0 + pp + 20))
    for dy in (-(pp / 2 + 6), pp / 2 + 6):
        for z in (ez0 + 9, ez0 + pp + 11):
            ely = ely + xc(ex0 - 10, ex1 + 10, GY + dy, z, 4)
    ely = ely + xc(ex1, ex1 + 12, GY, ezc + 25, 5)                     # hydrogen out, right end plate
    for z in (ez0 + 20, ez0 + 90):                                       # water in (low), oxygen and water out (high)
        ely = ely + yc(ex0 + et / 2, GY + hp, GY + hp + 12, z, 5)
    plates = b(ex0 + et, ex1 - et, GY - pp / 2, GY + pp / 2, ez0 + 10, ez0 + pp + 10)
    meas = _union([b(ex0 + et + i * pitch + 10, ex0 + et + i * pitch + 16, GY - pp / 2 + 3, GY + pp / 2 - 3,
                     ez0 + 13, ez0 + pp + 7) for i in range(n)])
    plates = plates - meas
    add("ely", "PEM electrolyzer stack", ely, "#0F766E", 6, "ely")
    add("ely_cells", "Electrolyzer cells", plates, "#9CA3AF", None, "ely")
    add("ely_meas", "Electrolyzer membranes", meas, "#111827", None, "ely")
    feet = []
    for xe, sx in ((ex0, -1), (ex1, 1)):
        xv = xe + sx * 3
        feet.append(b(xe, xv, GY - 35, GY + 35, DT, DT + 40)
                    + b(xv - sx * 3, xv + sx * 17, GY - 35, GY + 35, DT, DT + 3))
    fe = _union(feet)
    for xe, sx in ((ex0, -1), (ex1, 1)):
        for yy in (GY - 25, GY + 25):
            fe = fe - xc(xe - 1 * sx, xe + 4 * sx, yy, DT + 30, 3.25) - vc(xe + sx * 11.5, yy, DT - 1, DT + 4, 2.75)
    add("ely_feet", "Electrolyzer feet (2)", fe, "#B45309", 6, "ely", True)

    # 7 Separator (with drain valve) and drier on a folded 3 mm column bracket behind them
    sx_, sr, dx7, dr7 = p["sep_x"], p["sep_d"] / 2, p["drier_x"], p["drier_d"] / 2
    sep = (vc(sx_, GY, DT, DT + p["sep_h"], sr) + vc(sx_, GY, DT + p["sep_h"], DT + p["sep_h"] + 12, 5)
           + yc(sx_, GY - sr - 14, GY - sr + 1, DT + 14, 6) + vc(sx_, GY - sr - 10, DT + 14, DT + 30, 4))
    add("sep", "Gas and water separator", sep, "#6B7280", 7, "gas")
    drier = (vc(dx7, GY, DT, DT + p["drier_h"], dr7) + vc(dx7, GY, DT + p["drier_h"], DT + p["drier_h"] + 12, 5)
             + xc(dx7 + dr7 - 1, p["arr_x"][0], GY, p["arr_z"], 5))
    add("drier", "Silica gel drier", drier, "#9CA3AF", 7, "gas")
    cb_y = GY + sr + 5                                                   # bracket face, 5 mm behind the separator
    cbr = (b(sx_ - 20, dx7 + 22, cb_y, cb_y + 3, DT, DT + 150)
           + b(sx_ - 20, dx7 + 22, cb_y, cb_y + 23, DT, DT + 3))
    cz = DT + 110
    for xx in (sx_, dx7):
        cbr = cbr - yc(xx, cb_y - 1, cb_y + 4, cz + 5, 2.0) - vc(xx, cb_y + 14, DT - 1, DT + 4, 2.75)
    cbr = cbr - yc(p["deox_x"], cb_y - 1, cb_y + 4, DT + 3 + 70 + 5, 2.0)      # clip hole for the deoxidizer (2026-10-02)
    add("col_bracket", "Column bracket", cbr, "#A8A29E", 7, "gas", True)
    clips = (_ring(sx_, GY, cz, cz + 10, sr, sr + 1.5) + b(sx_ - 6, sx_ + 6, GY + sr + 0.5, cb_y, cz, cz + 10)
             + _ring(dx7, GY, cz, cz + 10, dr7, dr7 + 1.5) + b(dx7 - 6, dx7 + 6, GY + dr7 + 0.5, cb_y, cz, cz + 10))
    add("col_clips", "Pipe clips (2)", clips, "#111827", 7, "gas")

    # 19 Catalytic deoxidizer: stands on the column bracket's foot, its back 5 mm from the plate, one clip
    #    round it to the plate; inlet and outlet ports on top
    dxo, dro, dho = p["deox_x"], p["deox_d"] / 2, p["deox_h"]
    dyo = cb_y + 3 + 5 + dro
    zd0, zd1 = DT + 3, DT + 3 + dho
    deox = (vc(dxo, dyo, zd0, zd1, dro) + vc(dxo - 8, dyo, zd1, zd1 + 12, 4) + vc(dxo + 8, dyo, zd1, zd1 + 12, 4))
    add("deox", "Catalytic deoxidizer", deox, "#7C3AED", 19, "gas")
    zc = zd0 + 70
    add("deox_clip", "Deoxidizer clip", _ring(dxo, dyo, zc, zc + 10, dro, dro + 1.5)
        + b(dxo - 6, dxo + 6, cb_y + 3, dyo - dro - 0.5, zc, zc + 10), "#111827", 19, "gas")

    # 8 Check valve and flame arrestor on an HDPE saddle with a band clip
    ax0, ax1 = p["arr_x"]
    ar, az = p["arr_d"] / 2, p["arr_z"]
    add("arrestor", "Check valve and flame arrestor", xc(ax0, ax1, GY, az, ar), "#B45309", 8, "gas")
    am = (ax0 + ax1) / 2
    saddle = (b(am - 8, am + 8, GY - 16, GY + 16, DT, az - 4) - xc(am - 9, am + 9, GY, az, ar + 1.5)
              - vc(am, GY, DT - 1, DT + 10, 2.1))
    add("arr_saddle", "Arrestor saddle", saddle, "#E7E5E4", 8, "gas", True)
    add("arr_clip", "Arrestor band clip", xc(am - 3, am + 3, GY, az, ar + 1.5) - xc(am - 4, am + 4, GY, az, ar), "#111827", 8, "gas")

    # 9 Tank in a pocketed HDPE cradle, inside a guard of four M10 rods and a 4 mm top plate
    TX, TR, tw = p["tank_x"], p["tank_od"] / 2, p["tank_wall"]
    tz0, tz1, ttop = d["tz0"], d["tz1"], d["tank_top"]
    shell_out = vc(TX, GY, tz0, tz1, TR) + Pos(TX, GY, tz1) * Sphere(TR)
    shell_in = vc(TX, GY, tz0 + tw, tz1, TR - tw) + Pos(TX, GY, tz1) * Sphere(TR - tw)
    tank = (shell_out - shell_in) + vc(TX, GY, ttop - 4, ttop + 6, 12) - vc(TX, GY, ttop - 10, ttop + 7, 8)
    add("tank", "Hydrogen buffer tank, 2 L", tank, "#E5E7EB", 9, "tank")
    cw, ch = p["cradle"]
    pd_, pdep = p["cradle_pocket"]
    cradle = b(TX - cw / 2, TX + cw / 2, GY - cw / 2, GY + cw / 2, DT, DT + ch) - vc(TX, GY, DT + ch - pdep, DT + ch + 1, pd_ / 2)
    for ddx in (-53, 53):
        for ddy in (-53, 53):
            cradle = cradle - vc(TX + ddx, GY + ddy, DT - 1, DT + ch + 1, 2.75)
    add("cradle", "Tank cradle", cradle, "#E7E5E4", 9, "tank", True)
    go, gr = p["guard_offset"], p["guard_rod_d"] / 2
    gtop = d["g_top"]
    po, pi, pt = p["guard_plate"]
    rods, nuts = [], []
    for ddx in (-go, go):
        for ddy in (-go, go):
            x, y = TX + ddx, GY + ddy
            rods.append(vc(x, y, fh - 10, gtop + 12, gr))
            for z0 in (fh - 8, DT, gtop - pt - 8, gtop):
                nuts.append(vc(x, y, z0, z0 + 8, 8.5) - vc(x, y, z0 - 1, z0 + 9, gr))
    add("guard_rods", "Guard rods (4)", _union(rods), "#57534E", 9, "tank", True)
    add("guard_nuts", "Guard nuts (16)", _union(nuts), "#111827", 9, "tank")
    gp = b(TX - po / 2, TX + po / 2, GY - po / 2, GY + po / 2, gtop - pt, gtop) - b(TX - pi / 2, TX + pi / 2, GY - pi / 2, GY + pi / 2, gtop - pt - 1, gtop + 1)
    gp = gp - _union([vc(TX + ddx, GY + ddy, gtop - pt - 1, gtop + 1, gr + 0.5) for ddx in (-go, go) for ddy in (-go, go)])
    add("guard_plate", "Guard top plate", gp, "#78716C", 9, "tank", True)

    # 10 Tank manifold on the neck: transducer, thermistor, relief valve (325 kPa g), gauge,
    #    vent needle valve and the 310 kPa g supply cut switch (HBN-DDR-002)
    mz = ttop + 6
    manifold = (vc(TX, GY, ttop - 8, mz + 15, 8)
                + b(TX - 30, TX + 30, GY - 20, GY + 20, mz + 15, mz + 45)
                + vc(TX + 20, GY, mz + 45, mz + 80, 8)
                + yc(TX - 5, GY - 34, GY - 20, mz + 65, 24)
                + vc(TX - 20, GY, mz + 45, mz + 70, 6)
                + yc(TX, GY + 20, GY + 32, mz + 30, 6)
                + b(TX - 14, TX + 14, GY + 32, GY + 56, mz + 16, mz + 44))
    add("manifold", "Tank manifold", manifold, "#C2410C", 10, "tank")

    # 11 Normally closed solenoid valve and regulator
    rgx = p["reg_x"]
    reg = b(rgx - 25, rgx + 25, GY - 20, GY + 20, DT, DT + 65) + vc(rgx, GY, DT + 65, DT + 115, 22)
    add("reg", "Regulator and solenoid valve", reg, "#D4A017", 11, "fc")

    # 12 Fuel cell stack (75 x 47 x 70 mm) with front fan, on a folded 2 mm bridge
    fl, fd, fhh = p["fc"]
    fx0, fz0 = p["fc_x0"], d["fz0"]
    fc = b(fx0, fx0 + fl, GY - fd / 2, GY + fd / 2, fz0, fz0 + fhh) + yc(fx0 + fl / 2, GY - fd / 2 - 8, GY - fd / 2, fz0 + fhh / 2, 30)
    add("fc", "PEM fuel cell", fc, "#1F2937", 12, "fc")
    bridge = _hat(fx0 - 5, fx0 + fl + 5, GY - fd / 2 - 5, GY + fd / 2 + 5, fz0, DT, 2.0)
    for xx in (fx0 - 12.5, fx0 + fl + 12.5):
        for yy in (GY - 15, GY + 15):
            bridge = bridge - vc(xx, yy, DT - 1, DT + 3, 2.75)
    add("fc_bridge", "Fuel cell bridge", bridge,
        "#A8A29E", 12, "fc", True)

    # 13 Electronic load and lamp at the front right
    ll, ld, lh_ = p["load"]
    lx0, ly0 = p["load_x0"], p["load_y0"]
    load = b(lx0, lx0 + ll, ly0, ly0 + ld, DT, DT + lh_) + vc(lx0 + ll - 30, ly0 + ld / 2, DT + lh_, DT + lh_ + 40, 18)
    add("load", "Electronic load and lamp", load, "#FACC15", 13, "fc")

    # 14 Meters: display and three stage power meters on the panel face
    meters = b(-120, 120, py0 - 10, py0, DT + 350, DT + 460)
    for mx in (-380, -250, 250):
        meters = meters + b(mx, mx + 90, py0 - 8, py0, DT + 220, DT + 280)
    add("meters", "Meters, logger and display", meters, "#15803D", 14, "panel")

    # 15 H2Guard (massing stand-in): sensor head at the canopy high point beside the duct,
    #    extraction fan on the collar, controller box on the canopy
    dz1 = d["duct_top"]
    guard = (b(p["duct_x"] - 40, p["duct_x"] + 40, p["duct_y"] - 100, p["duct_y"] - 60, TOP - 45, TOP)
             + vc(*dxy, dz1, dz1 + 50, dr + 12)
             + b(90, 200, 90, 170, TOP + ct, TOP + ct + 70))
    add("h2guard", "H2Guard sensor, controller and fan", guard, "#DC2626", 15, "h2guard")

    # 3 Outlet hanger: 20 x 20 x 2 angle under the canopy; the relief and vent lines end at it
    hg = b(TX - 35, TX + 35, GY + 3, GY + 23, TOP - 2, TOP) + b(TX - 35, TX + 35, GY + 3, GY + 5, TOP - 22, TOP)
    for xx in (TX - 25, TX + 25):
        hg = hg - vc(xx, GY + 13, TOP - 3, TOP + 1, 2.25)
    for xx in (TX - 20, TX + 20):
        hg = hg - yc(xx, GY + 2, GY + 6, TOP - 10, 3.25)
    add("hanger", "Outlet hanger", hg,
        "#78716C", 3, "hood", True)

    # 16 Lines, 6 mm OD. Gas: stack to separator, separator to drier, arrestor to tank manifold,
    #    manifold to solenoid, regulator to fuel cell, relief and vent up to the hanger.
    #    Water: reservoir to cartridge, cartridge to stack, stack oxygen side back to the reservoir.
    ez_h2 = ezc + 25
    sep_top = DT + p["sep_h"] + 12
    dri_top = DT + p["drier_h"] + 12
    gas = [
        [(ex1 + 12, GY, ez_h2), (sx_ - sr + 1, GY, ez_h2)],
        [(sx_, GY, sep_top), (sx_, GY, sep_top + 12), (sx_, dyo, sep_top + 12), (dxo - 8, dyo, sep_top + 12), (dxo - 8, dyo, zd1 + 12)],
        [(dxo + 8, dyo, zd1 + 12), (dxo + 8, dyo, DT + 160), (dxo + 8, GY, DT + 160), (dx7, GY, DT + 160), (dx7, GY, dri_top)],
        [(ax1, GY, az), (108, GY, az), (108, GY, mz + 30), (TX - 30, GY, mz + 30)],
        [(TX + 30, GY, mz + 30), (rgx, GY, mz + 30), (rgx, GY, DT + 115)],
        [(rgx + 25, GY, fz0 + 5), (fx0, GY, fz0 + 5)],
        [(TX + 20, GY, mz + 80), (TX + 20, GY, TOP - 7)],
        [(TX - 20, GY, mz + 70), (TX - 20, GY, TOP - 7)],
    ]
    add("gas_lines", "Gas lines, 6 mm", _union([_tube(q, tr) for q in gas]), "#78716C", None, "lines")
    wz = rz0 + 18
    water = [
        [(rx, ry + rr + 12, wz), (rx, -60, wz), (dx_, -60, wz), (dx_, -60, DT + 18), (dx_, dy_ + drr + 12, DT + 18)],
        [(dx_, dy_, DT + p["di_h"] + 12), (dx_, dy_, 210), (-245, dy_, 210), (-245, 40, 210), (-245, 40, ez0 + 20),
         (ex0 + et / 2, 40, ez0 + 20), (ex0 + et / 2, GY + (pp + 20) / 2 + 12, ez0 + 20)],
        [(ex0 + et / 2, GY + (pp + 20) / 2 + 12, ez0 + 90), (ex0 + et / 2, 62, ez0 + 90), (ex0 + et / 2, 62, 290),
         (rx, 62, 290), (rx, ry, 290), (rx, ry, rz0 + p["res_h"])],
    ]
    add("water_lines", "Water lines, 6 mm", _union([_tube(q, tr) for q in water]), "#0EA5E9", None, "lines")
    return out


# The 15 numbered BOM groups, with the names the concept media and the appearance model use
GROUPS = [
    ("Bench deck and extrusion frame", ["rail_front", "rail_back", "end_l", "end_r", "cross_l", "cross_r",
                                        "frame_brackets", "deck", "lip"], "#9CA3AF", 1, (0, 0, -300)),
    ("Instrument back panel", ["panel"], "#D1D5DB", 2, (0, 480, -120)),
    ("Canopy hood, duct and posts", ["posts", "post_brackets", "top_rails", "top_brackets", "canopy", "collar", "hanger"],
     "#BFDBFE", 3, (0, 0, 480)),
    ("Bench DC power supply, 0 to 30 V, 10 A", ["psu"], "#374151", 4, (-260, 0, 120)),
    ("DI water reservoir and deionizer", ["res_stand", "reservoir", "di", "water_post", "water_bands"], "#38BDF8", 5, (-200, -300, 60)),
    ("PEM electrolyzer stack, about 70 W", ["ely", "ely_feet"], "#0F766E", 6, (-40, -260, 220)),
    ("Electrolyzer cells (plates and MEAs)", ["ely_cells"], "#9CA3AF", None, (-40, -260, 220)),
    ("Electrolyzer membranes", ["ely_meas"], "#111827", None, (-40, -260, 220)),
    ("Gas and water separator, drier", ["sep", "drier", "col_bracket", "col_clips"], "#6B7280", 7, (0, -380, 100)),
    ("Check valve and flame arrestor", ["arrestor", "arr_saddle", "arr_clip"], "#B45309", 8, (0, -300, 330)),
    ("Catalytic deoxidizer", ["deox", "deox_clip"], "#7C3AED", 19, (0, 260, 140)),
    ("Hydrogen buffer tank, 2 L, with guard", ["tank", "cradle", "guard_rods", "guard_nuts", "guard_plate"], "#E5E7EB", 9, (0, -120, 60)),
    ("Tank manifold: sensors, relief, gauge", ["manifold"], "#C2410C", 10, (0, -330, 330)),
    ("Regulator and solenoid valve", ["reg"], "#D4A017", 11, (60, -440, 0)),
    ("PEM fuel cell, 12 W class", ["fc", "fc_bridge"], "#1F2937", 12, (220, -150, 140)),
    ("Electronic load and lamp", ["load"], "#FACC15", 13, (250, -300, -60)),
    ("Meters, logger and display", ["meters"], "#15803D", 14, (0, 220, 220)),
    ("H2Guard sensor, controller and fan", ["h2guard"], "#DC2626", 15, (0, 0, 700)),
    ("Gas lines, 6 mm", ["gas_lines", "water_lines"], "#78716C", None, (0, -200, 180)),
]


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM group."""
    comp = build_components(p)
    return [(name, _union([comp[k].shape for k in keys]), col, bom, ex) for name, keys, col, bom, ex in GROUPS]


def assemblies(parts):
    """Named groups of parts for export."""
    from build123d import Compound
    by = {n: s for n, s, *_ in parts}
    grp = {
        "h2bench-assembly": [s for _, s, *_ in parts],
        "h2bench-frame-and-hood": [by["Bench deck and extrusion frame"], by["Instrument back panel"],
                                   by["Canopy hood, duct and posts"]],
        "h2bench-tank-module": [by["Hydrogen buffer tank, 2 L, with guard"], by["Tank manifold: sensors, relief, gauge"]],
        "h2bench-electrolyzer": [by["PEM electrolyzer stack, about 70 W"], by["Electrolyzer cells (plates and MEAs)"],
                                 by["Electrolyzer membranes"]],
    }
    # each group gets its own copies: a build123d shape can have only one parent compound
    import copy
    return {k: Compound(children=[copy.copy(x) for x in v]) for k, v in grp.items()}


# ----------------------------------------------------------------- constructability checks
# Parts that must touch (they bear on or fasten to each other).
MUST_TOUCH = [
    ("rail_front", "end_l"), ("rail_front", "end_r"), ("rail_back", "end_l"), ("rail_back", "end_r"),
    ("rail_front", "cross_l"), ("rail_back", "cross_r"), ("frame_brackets", "rail_front"), ("frame_brackets", "end_l"),
    ("frame_brackets", "cross_r"), ("deck", "rail_front"), ("deck", "cross_l"), ("lip", "deck"),
    ("posts", "end_l"), ("posts", "rail_back"), ("post_brackets", "posts"), ("post_brackets", "end_r"),
    ("post_brackets", "rail_back"), ("panel", "posts"), ("panel", "deck"), ("top_rails", "posts"),
    ("top_brackets", "top_rails"), ("top_brackets", "posts"), ("canopy", "top_rails"), ("collar", "canopy"),
    ("hanger", "canopy"), ("res_stand", "deck"), ("reservoir", "res_stand"), ("di", "deck"),
    ("water_post", "deck"), ("water_bands", "reservoir"), ("water_bands", "di"), ("water_bands", "water_post"),
    ("ely_feet", "ely"), ("ely_feet", "deck"), ("ely_cells", "ely"), ("sep", "deck"), ("drier", "deck"),
    ("col_bracket", "deck"), ("col_clips", "sep"), ("col_clips", "drier"), ("col_clips", "col_bracket"),
    ("deox", "col_bracket"), ("deox_clip", "deox"), ("deox_clip", "col_bracket"), ("gas_lines", "deox"),
    ("arr_saddle", "deck"), ("arr_clip", "arrestor"), ("arr_clip", "arr_saddle"), ("drier", "arrestor"),
    ("cradle", "deck"), ("tank", "cradle"), ("guard_rods", "guard_nuts"), ("guard_nuts", "deck"),
    ("guard_nuts", "guard_plate"), ("manifold", "tank"), ("reg", "deck"), ("fc_bridge", "deck"), ("fc", "fc_bridge"),
    ("load", "deck"), ("meters", "panel"), ("h2guard", "canopy"), ("h2guard", "collar"),
    ("gas_lines", "ely"), ("gas_lines", "sep"), ("gas_lines", "drier"), ("gas_lines", "arrestor"),
    ("gas_lines", "manifold"), ("gas_lines", "reg"), ("gas_lines", "fc"), ("gas_lines", "hanger"),
    ("water_lines", "reservoir"), ("water_lines", "di"), ("water_lines", "ely"),
]
# Overlaps that are intended: a line pushed into the fitting it connects to, a rod through its
# nuts, deck and plate, the manifold screwed into the tank neck.
ALLOWED = {frozenset(x) for x in [
    ("gas_lines", "ely"), ("gas_lines", "sep"), ("gas_lines", "drier"), ("gas_lines", "arrestor"),
    ("gas_lines", "manifold"), ("gas_lines", "reg"), ("gas_lines", "fc"),
    ("water_lines", "reservoir"), ("water_lines", "di"), ("water_lines", "ely"),
    ("guard_rods", "deck"), ("guard_rods", "guard_nuts"), ("manifold", "tank"), ("drier", "arrestor"), ("gas_lines", "deox"),
]}
# Minimum gaps between parts that must not touch (mm)
MIN_GAP = [
    ("gas_lines", "tank", 5.0), ("gas_lines", "guard_rods", 3.0), ("gas_lines", "guard_plate", 5.0),
    ("tank", "guard_rods", 15.0), ("tank", "guard_plate", 3.0), ("manifold", "guard_plate", 3.0),
    ("ely_feet", "sep", 5.0), ("ely", "sep", 5.0), ("ely_feet", "psu", 20.0), ("water_lines", "psu", 10.0),
    ("water_lines", "ely_feet", 3.0), ("res_stand", "posts", 0.0), ("panel", "top_brackets", 0.0),
    ("deox", "sep", 10.0), ("deox", "drier", 10.0), ("gas_lines", "col_bracket", 5.0), ("psu", "posts", 20.0),
    ("fc", "load", 20.0), ("water_lines", "gas_lines", 20.0), ("h2guard", "top_rails", 20.0),
]


def check(p=PARAMS, verbose=True):
    """Constructability checks with build123d. Returns (passed, failed) lists of messages."""
    import itertools
    comp = build_components(p)
    keys = list(comp)
    ok, bad = [], []
    for a, b2 in itertools.combinations(keys, 2):
        A, B = comp[a].shape, comp[b2].shape
        bba, bbb = A.bounding_box(), B.bounding_box()
        if (bba.min.X > bbb.max.X or bbb.min.X > bba.max.X or bba.min.Y > bbb.max.Y or bbb.min.Y > bba.max.Y
                or bba.min.Z > bbb.max.Z or bbb.min.Z > bba.max.Z):
            continue
        try:
            v = (A & B).volume
        except Exception:
            v = 0.0
        if v > 0.5 and frozenset((a, b2)) not in ALLOWED:
            bad.append(f"overlap {a} / {b2}: {v:.0f} mm3")
    n_ov = len(bad)
    if not bad:
        ok.append(f"no unintended overlaps among {len(keys)} parts")
    for a, b2 in MUST_TOUCH:
        dd = comp[a].shape.distance_to(comp[b2].shape)
        (ok if dd < 0.05 else bad).append(f"touch {a} / {b2}: gap {dd:.2f} mm")
    for a, b2, g in MIN_GAP:
        dd = comp[a].shape.distance_to(comp[b2].shape)
        (ok if dd >= g - 1e-6 else bad).append(f"gap {a} / {b2}: {dd:.1f} mm (needs {g:.0f})")
    # every part rests on or fastens to another part (no floating parts); the bench supply stands on the lab table
    for k in keys:
        if k == "psu":
            z0 = comp[k].shape.bounding_box().min.Z
            (ok if abs(z0) < 0.05 else bad).append(f"supported psu: stands on the lab table (z {z0:.2f} mm)")
            continue
        others = [comp[j].shape for j in keys if j != k]
        dmin = min(comp[k].shape.distance_to(o) for o in others)
        (ok if dmin < 0.05 else bad).append(f"supported {k}: nearest part {dmin:.2f} mm")
    if verbose:
        for m in bad:
            print("FAIL", m)
        print(f"constructability checks: {len(ok)} pass, {len(bad)} fail ({n_ov} overlaps)")
    return ok, bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, bad = check()
        sys.exit(1 if bad else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    asm = assemblies(parts)
    for name, shape in asm.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        print(f"wrote cad/step/{name}.step and cad/stl/{name}.stl")
    bbs = [s.bounding_box(optimal=True) for _, s, *_ in parts]
    size = [max(getattr(b.max, a) for b in bbs) - min(getattr(b.min, a) for b in bbs) for a in "XYZ"]
    l, d, h = envelope()
    print(f"assembly envelope {size[0]:.0f} x {size[1]:.0f} x {size[2]:.0f} mm (above the lab table)")
    print(f"envelope parameters {l:.0f} x {d:.0f} x {h:.0f} mm")
    print(f"tank internal volume {tank_internal_volume_l():.3f} L, straight length {tank_cyl_len():.1f} mm")
    check()
