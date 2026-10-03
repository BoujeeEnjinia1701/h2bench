"""H2Bench product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: an aluminium T-slot frame under a light HDPE deck
with a drip lip and a teal edge stripe; a printed back panel with the energy-chain schematic, a
lit logger display and three lit stage meters, panel screws and a hydrogen warning sign; a clear
polycarbonate canopy on slotted posts with an edge trim and the duct collar; a lab power supply
with lit voltage and current readouts, knurled knobs and binding posts; a HDPE reservoir with a
teal cap and graduations beside a clear deionizer cartridge showing its resin; the PEM
electrolyzer with teal end plates, tie rods and nuts, grooved titanium cells and brass ports; a
clear separator (water visible) and a clear drier (indicator gel visible); the flame arrestor
with hex ends and a flow arrow; the brushed buffer tank in its powder-coated guard with a wrapped
flammable gas label; a brass manifold with a dial gauge, relief valve, needle valve and cut
switch; the regulator with its solenoid coil; the fuel cell with grooved plates and a fan
grille; the electronic load with a lit readout and a lit lamp; and the H2Guard sensor head, fan
housing and controller with a lit status light. Every hydrogen part carries a flammable gas
label. Context is a compact section of the existing lab table top.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research and teaching prototype, not certified laboratory equipment.

Every main dimension, position and interface comes from PARAMS, levels(), tank_cyl_len() and
build_parts() in model.py (the gas lines and the membranes are taken from build_parts()
unchanged). Axes as model.py: X along the bench in energy-flow order, Y front (-Y, student side)
to back (+Y, instrument panel), Z up with Z = 0 at the top of the existing lab table. Units mm.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Sphere, extrude,
                       fillet)
from model import PARAMS, levels, tank_cyl_len, build_parts

derived = levels  # the brief's name for the derived levels (model.py has no derived())

TITLE = "H2Bench: hydrogen teaching bench from water to electricity and back"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); energy flows left "
             "to right from the power supply and electrolyzer through the guarded tank to the fuel cell "
             "and lit lamp, under the clear canopy with H2Guard at its high point"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): H2Guard, canopy and "
             "posts, back panel and meters, power supply, reservoir and deionizer, electrolyzer, "
             "separator, deoxidizer and drier, arrestor, tank with guard and manifold, regulator, fuel cell, load "
             "and lamp, gas lines, deck and frame"},
    {"name": "front", "groups": ["shell", "internal", "context"], "explode": False, "el": 12, "az": -78,
     "note": "View from the front (student side), slightly right and above (about 12 deg elevation): "
             "the gas train in energy-flow order with the hydrogen labels and lit meters"},
]

# Colours (restrained product palette; kit accent for end plates, caps and graphics)
C_ACCENT = "#0F766E"
C_ALU = "#C3C8CE"
C_DECK = "#E7E9EC"
C_PANEL = "#F2F3F4"
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_POWDER = "#343A42"
C_STEEL = "#B8BEC6"
C_TANK = "#D3D7DC"
C_TI = "#9AA0A7"
C_BRASS = "#C9A227"
C_WINDOW = "#DCEBF5"
C_WATER = "#9CCFE0"
C_RESIN = "#3E6E8E"
C_GEL = "#D98A2B"
C_LABEL = "#F4F4F2"
C_RED = "#C62828"
C_INK = "#23262B"
C_SCREEN = "#0E1216"
C_GLOW = "#5EEAD4"
C_AMBER = "#F5A524"
C_GREEN = "#22C55E"
C_LAMP = "#FFE9B8"
C_TUBE = "#EDEDEA"
C_TABLE = "#D6D3CD"


# ----------------------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _b(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _c(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _ycyl(x, y0, y1, z, r):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, abs(y1 - y0))


def _xcyl(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def _union(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _hex_z(x, y, z0, af, h):
    return Pos(x, y, z0) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _hex_x(x0, y, z, af, length):
    return Pos(x0, y, z) * extrude(Plane.YZ * RegularPolygon(af / math.sqrt(3), 6), amount=length)


def _front_face(local, x, y, z):
    """Place a local feature (layout in local X right, Y up, standing proud along +Z) on a face
    that looks toward -Y (the student side) at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * local


def _right_face(local, x, y, z):
    """As _front_face, for a face that looks toward +X (local X becomes +Y)."""
    return Pos(x, y, z) * Rot(0, 0, 90) * Rot(90, 0, 0) * local


def _knob(r, h, n=18, groove=0.9):
    """Knurled knob along +Z from z = 0 with a domed front edge."""
    k = Pos(0, 0, h / 2) * Cylinder(r, h)
    k = _fillet_try(k, _top(k), [r * 0.25, r * 0.15])
    for i in range(n):
        a = 2 * math.pi * i / n
        k -= Pos(r * math.cos(a), r * math.sin(a), h * 0.45) * Rot(0, 0, math.degrees(a)) * Box(groove * 2, groove, h * 0.9)
    return k


def _label_layers(w, h, prism=False):
    """Flammable gas label, local, facing +Z from z = 0: white plate, red GHS diamond with a white
    centre and a dark flame, and dark text bars. Returns {"plate", "red", "white", "ink"}.
    With prism=True every layer is a 400 mm deep prism centred on z = 0 (for wrapping)."""
    def zb(t0, t1):
        return (0.0, 400.0) if prism else ((t0 + t1) / 2, t1 - t0)

    s = min(h * 0.62, w * 0.36)                   # diamond side
    dx = -w / 2 + s * 0.78
    zc, tz = zb(0.0, 0.4)
    plate = Pos(0, 0, zc) * Box(w, h, tz)
    plate = _fillet_try(plate, _edges_par(plate, Axis.Z), [min(w, h) * 0.08, 0.5])
    zc, tz = zb(0.4, 0.7)
    red = Pos(dx, 0, zc) * Rot(0, 0, 45) * Box(s, s, tz)
    zc, tz = zb(0.7, 0.8)
    white = Pos(dx, 0, zc) * Rot(0, 0, 45) * Box(s * 0.8, s * 0.8, tz)
    zc, tz = zb(0.8, 0.9)
    ink = (Pos(dx, -s * 0.08, zc) * Cylinder(s * 0.16, tz)
           + Pos(dx, s * 0.12, zc) * Rot(0, 0, 45) * Box(s * 0.2, s * 0.2, tz))
    tx = dx + s * 0.78
    tw = w / 2 - tx - w * 0.06
    if tw > 2:
        zc, tz = zb(0.4, 0.6)
        ink = ink + Pos(tx + tw / 2, h * 0.18, zc) * Box(tw, h * 0.16, tz)
        ink = ink + Pos(tx + tw * 0.4, -h * 0.06, zc) * Box(tw * 0.8, h * 0.07, tz)
        ink = ink + Pos(tx + tw * 0.45, -h * 0.24, zc) * Box(tw * 0.9, h * 0.07, tz)
    return {"plate": plate, "red": red, "white": white, "ink": ink}


def _wrap_label(w, h, cx, cy, zc, R, angle):
    """Flammable gas label wrapped onto a vertical cylinder of radius R at (cx, cy), centred at
    height zc and turned `angle` degrees from the front (-Y) toward +X."""
    lay = _label_layers(w, h, prism=True)
    rng = {"plate": (0.0, 0.4), "red": (0.4, 0.7), "white": (0.7, 0.8), "ink": (0.4, 0.9)}
    out = {}
    for k, (r0, r1) in rng.items():
        prism = _front_face(lay[k], cx, cy, zc)
        band = _zcyl(cx, cy, zc - h, zc + h, R + r1) - _zcyl(cx, cy, zc - h - 1, zc + h + 1, R + r0)
        out[k] = Pos(cx, cy, 0) * Rot(0, 0, angle) * Pos(-cx, -cy, 0) * (prism & band)
    return out


def product_parts(P=PARAMS):
    deck_top, TOP = levels(P)
    L, D = P["bench_l"], P["bench_d"]
    fh, s = P["frame_h"], P["post"]
    GY = P["gas_y"]
    base = {n: sh for n, sh, *_ in build_parts(P)}
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def add_label(prefix, layers, bom, group, explode):
        add(f"{prefix} hydrogen label", layers["plate"] + layers["white"], C_LABEL, "paper", bom, group, explode)
        add(f"{prefix} hydrogen label diamond", layers["red"], C_RED, "painted", bom, group, explode)
        add(f"{prefix} hydrogen label print", layers["ink"], C_INK, "paper", bom, group, explode)

    def placed(layers, fn, x, y, z):
        return {k: fn(v, x, y, z) for k, v in layers.items()}

    # ------------------------------------------------------------ 1 deck and frame
    E1 = (0, 0, -300)
    frame = _union([_b(-L / 2, L / 2, -D / 2, -D / 2 + s, 0, fh), _b(-L / 2, L / 2, D / 2 - s, D / 2, 0, fh),
                    _b(-L / 2, -L / 2 + s, -D / 2 + s, D / 2 - s, 0, fh), _b(L / 2 - s, L / 2, -D / 2 + s, D / 2 - s, 0, fh),
                    _b(-L / 6 - s / 2, -L / 6 + s / 2, -D / 2 + s, D / 2 - s, 0, fh),
                    _b(L / 6 - s / 2, L / 6 + s / 2, -D / 2 + s, D / 2 - s, 0, fh)])
    g0, g1 = fh / 2 - 3, fh / 2 + 3                 # T-slot on the outer faces
    frame -= _b(-L / 2 - 1, L / 2 + 1, -D / 2 - 1, -D / 2 + 2, g0, g1)
    frame -= _b(-L / 2 - 1, L / 2 + 1, D / 2 - 2, D / 2 + 1, g0, g1)
    frame -= _b(-L / 2 - 1, -L / 2 + 2, -D / 2 + s, D / 2 - s, g0, g1)
    frame -= _b(L / 2 - 2, L / 2 + 1, -D / 2 + s, D / 2 - s, g0, g1)
    add("Aluminium extrusion frame", frame, C_ALU, "metal", 1, "shell", E1)

    lh = P["lip_h"]
    deck = _b(-L / 2, L / 2, -D / 2, D / 2, fh, deck_top + lh)
    deck = _fillet_try(deck, _edges_par(deck, Axis.Z), [8.0, 6.0, 4.0])
    deck = _fillet_try(deck, _top(deck), [2.0, 1.5, 1.0])
    pocket = _b(-L / 2 + 6, L / 2 - 6, -D / 2 + 6, D / 2 - 6, deck_top, deck_top + lh + 1)
    pocket = _fillet_try(pocket, _edges_par(pocket, Axis.Z), [4.0, 2.0])
    deck -= pocket
    add("HDPE deck with drip lip", deck, C_DECK, "plastic", 1, "shell", E1)
    stripe = _b(-L / 2 + 20, L / 2 - 20, -D / 2 - 0.4, -D / 2, fh + 5, fh + 11)
    add("Deck accent stripe", stripe, C_ACCENT, "painted", 1, "shell", E1)
    np_ = _b(-L / 2 + 30, -L / 2 + 120, -D / 2 - 0.6, -D / 2, fh + 14, fh + 18.5)
    add("Deck name plate", np_, C_DARK, "painted", 17, "shell", E1)

    # ------------------------------------------------------------ 2 back panel
    E2 = (0, 480, -120)
    pt = P["panel_t"]
    py1 = D / 2
    pf = py1 - pt
    zl = deck_top + lh
    panel = _b(-L / 2, L / 2, pf, py1, zl, TOP)
    panel = _fillet_try(panel, _edges_par(panel, Axis.Y), [12.0, 8.0, 4.0])
    add("Instrument back panel (printed)", panel, C_PANEL, "painted", 2, "shell", E2)
    scr = []
    for x in (-L / 2 + 14, -L / 6, L / 6, L / 2 - 14):
        for z in (zl + 14, TOP - 14):
            sc = _ycyl(x, pf - 1.4, pf, z, 3.2)
            sc = _fillet_try(sc, _front(sc), [0.6, 0.3])
            scr.append(sc - _c(x, pf - 1.4, z, 3.8, 0.8, 0.8))
    add("Panel screws", _union(scr), C_STEEL, "metal", 17, "shell", E2)
    # printed energy-chain schematic: title, flow line with a node per stage, captions
    zs = deck_top + 520
    stages = [-380 + 105 * k for k in range(7)]    # seven stages, power in to lamp out
    line = _b(stages[0], stages[-1], pf - 0.3, pf, zs - 1.5, zs + 1.5)
    nodes = _union([_ycyl(x, pf - 0.5, pf, zs, 9.0) for x in stages])
    arrows = _union([Pos((a + b_) / 2, pf - 0.3, zs) * Rot(90, 0, 0) * extrude(RegularPolygon(5, 3), amount=0.3)
                     for a, b_ in zip(stages, stages[1:])])
    add("Panel schematic flow line", line + nodes + arrows, C_ACCENT, "painted", 2, "shell", E2)
    ink = [_b(-L / 2 + 30, -L / 2 + 170, pf - 0.3, pf, TOP - 50, TOP - 38),
           _b(-L / 2 + 30, -L / 2 + 250, pf - 0.3, pf, TOP - 64, TOP - 60)]
    for x in stages:
        ink.append(_b(x - 22, x + 22, pf - 0.3, pf, zs - 24, zs - 19))
        ink.append(_b(x - 14, x + 14, pf - 0.3, pf, zs - 31, zs - 28))
        ink.append(_ycyl(x, pf - 0.7, pf - 0.5, zs, 4.0))
    add("Panel schematic print", _union(ink), C_INK, "paper", 2, "shell", E2)
    sign = placed(_label_layers(96, 60), _front_face, 372, pf, deck_top + 440)
    add_label("Panel warning sign", sign, 17, "shell", E2)

    # ------------------------------------------------------------ 3 canopy hood, posts, duct
    E3 = (0, 0, 480)
    cy0 = P["canopy_front_y"]
    ct = P["canopy_t"]
    dr = P["duct_d"] / 2
    dx_, dy_ = P["duct_x"], P["duct_y"]
    sheet = _b(-L / 2, L / 2, cy0, D / 2, TOP, TOP + ct)
    sheet = _fillet_try(sheet, _edges_par(sheet, Axis.Z), [10.0, 6.0])
    sheet -= _zcyl(dx_, dy_, TOP - 1, TOP + ct + 1, dr)
    add("Polycarbonate canopy", sheet, C_WINDOW, "clear", 3, "shell", E3)
    trim = (_b(-L / 2, L / 2, cy0 - 1, cy0 + 9, TOP - 5, TOP + ct + 3)
            + _b(-L / 2, -L / 2 + 10, cy0, D / 2, TOP - 5, TOP + ct + 3)
            + _b(L / 2 - 10, L / 2, cy0, D / 2, TOP - 5, TOP + ct + 3))
    trim = _fillet_try(trim, _edges_par(trim, Axis.Z), [3.0, 1.5])
    add("Canopy edge trim", trim, C_ALU, "metal", 3, "shell", E3)
    posts = []
    for x0 in (-L / 2, L / 2 - s):
        pst = _b(x0, x0 + s, cy0, cy0 + s, zl, TOP - 5)
        cx, cyy = x0 + s / 2, cy0 + s / 2
        for (ox, oy, sx_, sy_) in [(s / 2, 0, 3, 5), (-s / 2, 0, 3, 5), (0, s / 2, 5, 3), (0, -s / 2, 5, 3)]:
            pst -= _c(cx + ox, cyy + oy, (zl + TOP) / 2, sx_, sy_, TOP - zl - 20)
        posts.append(pst)
    add("Canopy posts (T-slot extrusion)", _union(posts), C_ALU, "metal", 3, "shell", E3)
    feet = _union([_b(x0 - 4, x0 + s + 4, cy0 - 4, cy0 + s + 4, zl, zl + 6) for x0 in (-L / 2 + 4, L / 2 - s - 4)])
    feet = _fillet_try(feet, _edges_par(feet, Axis.Z), [2.0, 1.0])
    add("Post foot brackets", feet, C_DARK, "painted", 3, "shell", E3)
    dz0, dz1 = TOP + ct, TOP + ct + P["duct_h"]
    collar = _zcyl(dx_, dy_, TOP, dz1, dr + 3) - _zcyl(dx_, dy_, TOP - 1, dz1 + 1, dr)
    flange = _zcyl(dx_, dy_, dz0, dz0 + 3, dr + 14) - _zcyl(dx_, dy_, dz0 - 1, dz0 + 4, dr + 1)
    flange = _fillet_try(flange, _top(flange), [1.0, 0.5])
    bead = _zcyl(dx_, dy_, dz0 + 40, dz0 + 44, dr + 4.5) - _zcyl(dx_, dy_, dz0 + 39, dz0 + 45, dr + 1)
    add("Duct collar and flange", collar + flange + bead, C_SHELL, "plastic", 3, "shell", E3)

    # ------------------------------------------------------------ 4 bench power supply
    E4 = (-260, 0, 120)
    pl, pd, ph = P["psu"]
    x0, y0 = P["psu_x0"], P["psu_y0"]
    case = _b(x0, x0 + pl, y0, y0 + pd, 0, 0 + ph)
    case = _fillet_try(case, _edges_par(case, Axis.Y), [6.0, 4.0, 2.0])
    for k in range(7):                             # top vent slots
        case -= _b(x0 + 30, x0 + pl - 30, y0 + 90 + 12 * k, y0 + 95 + 12 * k, 0 + ph - 1.2, 0 + ph + 1)
    add("Power supply case", case, C_SHELL2, "painted", 4, "shell", E4)
    fz0, fz1 = 0 + 30, 0 + ph - 20
    fx0, fx1 = x0 + 10, x0 + pl - 10
    fp = _b(fx0, fx1, y0 - 4, y0, fz0, fz1)
    fp = _fillet_try(fp, _edges_par(fp, Axis.Y), [4.0, 2.0])
    fp = _fillet_try(fp, _front(fp), [1.0, 0.5])
    add("Power supply front panel", fp, C_BLACK, "plastic", 4, "shell", E4)
    fy = y0 - 4
    dzp = fz1 - 20
    scr_ = _union([_b(xc - 22, xc + 22, fy - 0.3, fy, dzp - 9, dzp + 9) for xc in (fx0 + 32, fx1 - 32)])
    add("Power supply display windows", scr_, C_SCREEN, "screen", 4, "shell", E4)
    digv = _union([_b(fx0 + 16 + 9 * i, fx0 + 22 + 9 * i, fy - 0.6, fy - 0.3, dzp - 5, dzp + 5) for i in range(4)])
    diga = _union([_b(fx1 - 48 + 9 * i, fx1 - 42 + 9 * i, fy - 0.6, fy - 0.3, dzp - 5, dzp + 5) for i in range(4)])
    add("Voltage readout (lit)", digv, C_AMBER, "emissive", 4, "shell", E4)
    add("Current readout (lit)", diga, C_GREEN, "emissive", 4, "shell", E4)
    knobs = _union([_front_face(_knob(9.0, 10.0), xc, fy, dzp - 32) for xc in (fx0 + 32, fx1 - 32)])
    add("Power supply knobs", knobs, C_DARK, "rubber", 4, "shell", E4)
    posts_ = []
    for i, (col, nm) in enumerate([("#B91C1C", "red"), (C_BLACK, "black"), ("#15803D", "earth")]):
        xc = fx0 + 35 + 30 * i
        bp = _ycyl(xc, fy - 9, fy, fz0 + 12, 5.0)
        bp = _fillet_try(bp, _front(bp), [1.2, 0.6])
        add(f"Binding post, {nm}", bp, col, "plastic", 4, "shell", E4)
    sw = _b(fx1 - 22, fx1 - 8, fy - 3, fy, fz0 + 6, fz0 + 18)
    sw = _fillet_try(sw, _edges_par(sw, Axis.Y), [1.5, 0.8])
    add("Power switch", sw, C_ACCENT, "plastic", 4, "shell", E4)

    # ------------------------------------------------------------ 5 reservoir and deionizer
    E5 = (-200, -300, 60)
    rx, ry = P["res_x"], P["res_y"]
    rr, rh = P["res_d"] / 2, P["res_h"]
    body = _zcyl(rx, ry, deck_top, deck_top + rh - 14, rr)
    body = _fillet_try(body, _top(body), [10.0, 6.0])
    body += _zcyl(rx, ry, deck_top + rh - 20, deck_top + rh - 12, 22)
    add("DI water reservoir (HDPE)", body, "#EEF1F2", "plastic", 5, "shell", E5)
    cap = _zcyl(rx, ry, deck_top + rh - 14, deck_top + rh, 24)
    cap = _fillet_try(cap, _top(cap), [2.5, 1.5])
    for i in range(20):
        a = 2 * math.pi * i / 20
        cap -= Pos(rx + 24 * math.cos(a), ry + 24 * math.sin(a), deck_top + rh - 8) * Rot(0, 0, math.degrees(a)) * Box(2, 1.4, 10)
    add("Reservoir cap", cap, C_ACCENT, "plastic", 5, "shell", E5)
    grad = []
    for k in range(6):                             # graduations on the front
        z = deck_top + 30 + 20 * k
        w = 14 if k % 2 == 0 else 8
        a = Pos(rx, ry, z) * Rot(0, 0, -60) * _b(rr - 0.2, rr + 0.4, -w / 2, w / 2, -0.8, 0.8)
        grad.append(a)
    add("Reservoir graduations", _union(grad), C_INK, "paper", 5, "shell", E5)
    cxr, cyr = rx + 100, ry - 10
    cart = _zcyl(cxr, cyr, deck_top + 16, deck_top + 184, 24) - _zcyl(cxr, cyr, deck_top + 15, deck_top + 185, 22)
    add("Deionizer cartridge body", cart, C_WINDOW, "clear", 5, "shell", E5)
    resin = _zcyl(cxr, cyr, deck_top + 18, deck_top + 150, 21.5)
    add("Mixed-bed resin (colour change)", resin, C_RESIN, "plastic", 5, "internal", E5)
    resin2 = _zcyl(cxr, cyr, deck_top + 150, deck_top + 180, 21.5)
    add("Resin, exhausted zone", resin2, "#B79A55", "plastic", 5, "internal", E5)
    ec = _zcyl(cxr, cyr, deck_top, deck_top + 16, 25) + _zcyl(cxr, cyr, deck_top + 184, deck_top + 200, 25)
    ec = _fillet_try(ec, ec.edges(), [2.0, 1.0])
    ec += _zcyl(cxr, cyr, deck_top + 200, deck_top + 208, 4)
    add("Cartridge end caps", ec, C_DARK, "plastic", 5, "shell", E5)

    # ------------------------------------------------------------ 6 PEM electrolyzer
    E6 = (-40, -260, 220)
    ex0, n, pitch, pp, et = P["ely_x0"], P["ely_cells"], P["ely_pitch"], P["ely_plate"], P["ely_end_t"]
    ez0 = deck_top + P["ely_lift"]
    ex1 = ex0 + 2 * et + n * pitch
    ezc = ez0 + (pp + 20) / 2
    hy = (pp + 20) / 2
    ends = []
    for a0 in (ex0, ex1 - et):
        e = _b(a0, a0 + et, GY - hy, GY + hy, ez0, ez0 + pp + 20)
        e = _fillet_try(e, _edges_par(e, Axis.X), [6.0, 4.0, 2.0])
        e = _fillet_try(e, e.edges().filter_by(Axis.Y) + e.edges().filter_by(Axis.Z), [1.2, 0.6])
        ends.append(e)
    add("Electrolyzer end plates", _union(ends), C_ACCENT, "painted", 6, "shell", E6)
    feet6 = _b(ex0, ex1, GY - 50, GY - 30, deck_top, ez0) + _b(ex0, ex1, GY + 30, GY + 50, deck_top, ez0)
    feet6 = _fillet_try(feet6, _edges_par(feet6, Axis.Y), [2.0, 1.0])
    add("Electrolyzer feet", feet6, C_DARK, "rubber", 6, "shell", E6)
    rods, nuts = [], []
    for dy in (-(pp + 4) / 2, (pp + 4) / 2):
        for z in (ez0 + 7, ez0 + pp + 13):
            rods.append(_xcyl(ex0 - 10, ex1 + 10, GY + dy, z, 4))
            nuts.append(_hex_x(ex0 - 8, GY + dy, z, 13.0, 7.0))
            nuts.append(_hex_x(ex1 + 1, GY + dy, z, 13.0, 7.0))
    add("Tie rods", _union(rods), C_STEEL, "metal", 6, "shell", E6)
    add("Tie rod nuts", _union(nuts), C_STEEL, "metal", 17, "shell", E6)
    ports = (_xcyl(ex1, ex1 + 12, GY, ezc + 25, 5) + _hex_x(ex1 + 2, GY, ezc + 25, 12.0, 5.0)
             + _ycyl(ex0 + et + 10, GY + hy, GY + hy + 12, ezc + 30, 5))
    add("Electrolyzer ports (H2 and O2)", ports, C_BRASS, "metal", 6, "shell", E6)
    plates = base["Electrolyzer cells (plates and MEAs)"]
    for i in range(n + 1):                         # cell boundaries on the outer faces
        xg = ex0 + et + i * pitch
        if 0 < i < n:
            plates -= _b(xg - 0.8, xg + 0.8, GY - pp / 2 - 1, GY + pp / 2 + 1, ez0 + 8, ez0 + pp + 12) \
                - _b(xg - 1, xg + 1, GY - pp / 2 + 1.5, GY + pp / 2 - 1.5, ez0 + 11.5, ez0 + pp + 8.5)
    for i in range(n):
        xm = ex0 + et + i * pitch + pitch / 2
        plates -= _b(xm - 0.4, xm + 0.4, GY - pp / 2 - 1, GY - pp / 2 + 0.6, ez0 + 18, ez0 + pp + 2)
    add("Electrolyzer cells (titanium plates)", plates, C_TI, "metal", 6, "internal", E6)
    add("Electrolyzer membranes (MEAs)", base["Electrolyzer membranes"], C_BLACK, "plastic", 6, "internal", E6)
    add_label("Electrolyzer", placed(_label_layers(58, 30), _right_face, ex1, GY - 8, ez0 + 34), 17, "shell", E6)

    # ------------------------------------------------------------ 7 separator and drier
    E7 = (0, -380, 100)
    sx_, sr, sh = P["sep_x"], P["sep_d"] / 2, P["sep_h"]
    dx7, dr7, dh7 = P["drier_x"], P["drier_d"] / 2, P["drier_h"]
    sep = _zcyl(sx_, GY, deck_top + 14, deck_top + sh - 14, sr - 1) - _zcyl(sx_, GY, deck_top + 13, deck_top + sh - 13, sr - 3)
    add("Separator column (clear)", sep, C_WINDOW, "clear", 7, "shell", E7)
    water = _zcyl(sx_, GY, deck_top + 14, deck_top + 70, sr - 3.2)
    add("Separator water", water, C_WATER, "plastic", 7, "internal", E7)
    dri = _zcyl(dx7, GY, deck_top + 12, deck_top + dh7 - 12, dr7 - 1) - _zcyl(dx7, GY, deck_top + 11, deck_top + dh7 - 11, dr7 - 2.5)
    add("Drier body (clear)", dri, C_WINDOW, "clear", 7, "shell", E7)
    gel = _zcyl(dx7, GY, deck_top + 12, deck_top + dh7 - 22, dr7 - 2.7)
    add("Silica gel with indicator", gel, C_GEL, "plastic", 7, "internal", E7)
    caps7 = []
    for (xc, r, h) in [(sx_, sr, sh), (dx7, dr7, dh7)]:
        for z0_, z1_ in [(deck_top, deck_top + 14), (deck_top + h - 14, deck_top + h)]:
            cc = _zcyl(xc, GY, z0_, z1_, r)
            cc = _fillet_try(cc, cc.edges(), [2.0, 1.0])
            caps7.append(cc)
    add("Separator and drier end caps", _union(caps7), C_DARK, "plastic", 7, "shell", E7)

    # 19 catalytic deoxidizer between separator and drier, on the column bracket (model.py geometry, 2026-10-02)
    E19 = (0, 260, 140)
    cb_y = GY + sr + 5
    cbx0, cbx1 = sx_ - 20, dx7 + 22
    cbr = _b(cbx0, cbx1, cb_y, cb_y + 3, deck_top, deck_top + 150) + _b(cbx0, cbx1, cb_y, cb_y + 23, deck_top, deck_top + 3)
    add("Column bracket (folded aluminium)", cbr, C_ALU, "metal", 7, "shell", E7)
    dxo, dro, dho = P["deox_x"], P["deox_d"] / 2, P["deox_h"]
    dyo = cb_y + 3 + 5 + dro
    zd0, zd1 = deck_top + 3, deck_top + 3 + dho
    body = _zcyl(dxo, dyo, zd0, zd1, dro)
    body = _fillet_try(body, body.edges(), [3.0, 2.0])
    add("Deoxidizer cartridge", body, C_STEEL, "metal", 19, "shell", E19)
    cap19 = _zcyl(dxo, dyo, zd1, zd1 + 6, dro - 3) + _zcyl(dxo - 8, dyo, zd1 + 6, zd1 + 12, 4.0) + _zcyl(dxo + 8, dyo, zd1 + 6, zd1 + 12, 4.0)
    add("Deoxidizer head and ports", cap19, C_BRASS, "metal", 19, "shell", E19)
    zc = zd0 + 70
    clip19 = _zcyl(dxo, dyo, zc, zc + 10, dro + 1.5) - _zcyl(dxo, dyo, zc - 1, zc + 11, dro) + _b(dxo - 6, dxo + 6, cb_y + 3, dyo - dro - 0.5, zc, zc + 10)
    add("Deoxidizer clip", clip19, C_DARK, "metal", 19, "shell", E19)

    # ------------------------------------------------------------ 8 check valve and flame arrestor
    E8 = (0, -300, 330)
    gz = deck_top + 150.0
    arr = _xcyl(58, 97, GY, gz, 14)
    arr = _fillet_try(arr, arr.edges(), [3.0, 2.0])
    arr += _hex_x(50, GY, gz, 20.0, 8.0) + _hex_x(97, GY, gz, 20.0, 8.0)
    for k in range(5):
        arr -= _xcyl(64 + 6 * k, 65.5 + 6 * k, GY, gz, 15) - _xcyl(63, 67.5 + 6 * k, GY, gz, 13.3)
    add("Check valve and flame arrestor (stainless)", arr, C_STEEL, "metal", 8, "shell", E8)
    post8 = _b(70, 85, GY - 8, GY + 8, deck_top, gz - 13)
    post8 = _fillet_try(post8, _edges_par(post8, Axis.Z), [2.0, 1.0])
    post8 += _b(64, 91, GY - 14, GY + 14, deck_top, deck_top + 4)
    add("Arrestor post", post8, C_POWDER, "painted", 8, "shell", E8)
    arrow = Pos(77.5, GY - 14.3, gz) * Rot(90, 0, 0) * (
        Pos(-4, 0, 0) * Box(12, 3, 0.4) + Pos(4, 0, 0) * extrude(RegularPolygon(4.5, 3), amount=0.4, both=True))
    add("Flow direction arrow", arrow, C_ACCENT, "paper", 17, "shell", E8)

    # ------------------------------------------------------------ 9 buffer tank and guard
    E9 = (0, -120, 60)
    TX, TR, tw, tz0 = P["tank_x"], P["tank_od"] / 2, P["tank_wall"], deck_top + P["cradle"][1] - P["cradle_pocket"][1]
    lc = tank_cyl_len(P)
    tz1 = tz0 + tw + lc
    tank_top = tz1 + TR
    shell_out = _zcyl(TX, GY, tz0, tz1, TR) + Pos(TX, GY, tz1) * Sphere(TR)
    shell_in = _zcyl(TX, GY, tz0 + tw, tz1, TR - tw) + Pos(TX, GY, tz1) * Sphere(TR - tw)
    shell = _fillet_try(shell_out, shell_out.faces().sort_by(Axis.Z)[0].edges(), [5.0, 3.0]) - shell_in
    add("Hydrogen buffer tank (2 L)", shell, C_TANK, "metal", 9, "shell", E9)
    shoulder = (Pos(TX, GY, tz1) * Sphere(TR + 0.5) - Pos(TX, GY, tz1) * Sphere(TR - 1)) & _b(
        TX - TR - 2, TX + TR + 2, GY - TR - 2, GY + TR + 2, tz1 + 8, tz1 + 30)
    add("Tank shoulder band (hydrogen red)", shoulder, C_RED, "painted", 9, "shell", E9)
    cradle = _b(TX - 65, TX + 65, GY - 65, GY + 65, deck_top, tz0)
    cradle = _fillet_try(cradle, _edges_par(cradle, Axis.Z), [6.0, 3.0])
    cradle -= _zcyl(TX, GY, tz0 - 4, tz0 + 1, TR + 2)
    add("Tank cradle", cradle, C_POWDER, "painted", 9, "shell", E9)
    g_top = tank_top + P["guard_top_gap"]
    go, gr = P["guard_offset"], P["guard_rod_d"] / 2
    rods9 = [_zcyl(TX + a, GY + b_, deck_top, g_top - 4, gr) for a in (-go, go) for b_ in (-go, go)]
    ring = _b(TX - go - 5, TX + go + 5, GY - go - 5, GY + go + 5, g_top - 8, g_top)
    ring = _fillet_try(ring, _edges_par(ring, Axis.Z), [8.0, 5.0])
    hole = _b(TX - go + 5, TX + go - 5, GY - go + 5, GY + go - 5, g_top - 9, g_top + 1)
    hole = _fillet_try(hole, _edges_par(hole, Axis.Z), [4.0, 2.0])
    guard = _union(rods9) + (ring - hole)
    add("Tank guard (powder-coated steel)", guard, C_POWDER, "painted", 9, "shell", E9)
    bolts = _union([_hex_z(TX + a, GY + b_, deck_top, 12.0, 5.0) for a in (-go, go) for b_ in (-go, go)])
    add("Guard foot nuts", bolts, C_STEEL, "metal", 17, "shell", E9)
    # wrapped flammable gas label, facing the front right
    add_label("Tank", _wrap_label(64, 44, TX, GY, tz0 + tw + lc * 0.45, TR, 40), 17, "shell", E9)

    # ------------------------------------------------------------ 10 tank manifold
    E10 = (0, -120, 250)
    mz = tank_top
    blk = _b(TX - 30, TX + 30, GY - 20, GY + 20, mz + 15, mz + 45)
    blk = _fillet_try(blk, blk.edges(), [2.0, 1.0])
    blk += _zcyl(TX, GY, mz - 2, mz + 15, 10) + _hex_z(TX, GY, mz + 4, 22.0, 6.0)
    add("Manifold block and boss (brass)", blk, C_BRASS, "metal", 10, "shell", E10)
    rel = _zcyl(TX + 20, GY, mz + 45, mz + 70, 8) + _hex_z(TX + 20, GY, mz + 47, 17.0, 6.0)
    add("Relief valve, 325 kPa gauge", rel, C_BRASS, "metal", 10, "shell", E10)
    relcap = _zcyl(TX + 20, GY, mz + 70, mz + 80, 8.4)
    relcap = _fillet_try(relcap, _top(relcap), [2.0, 1.0])
    add("Relief valve cap", relcap, C_RED, "painted", 10, "shell", E10)
    nv = _zcyl(TX - 20, GY, mz + 45, mz + 56, 5) + Pos(TX - 20, GY, mz + 56) * _knob(7.0, 14.0, n=14, groove=0.8)
    add("Vent needle valve and knob", nv, C_BLACK, "plastic", 10, "shell", E10)
    gx, gyc, gzc = TX - 5, GY - 27, mz + 65
    stem = _zcyl(gx, GY - 20, mz + 40, gzc - 20, 4) + _ycyl(gx, GY - 20, GY - 26, gzc - 20, 4)
    add("Gauge stem", stem, C_BRASS, "metal", 10, "shell", E10)
    case10 = _ycyl(gx, gyc + 7, gyc - 7, gzc, 24)
    case10 = _fillet_try(case10, _front(case10), [2.0, 1.0])
    case10 -= _ycyl(gx, gyc - 8, gyc - 5, gzc, 20.5)
    add("Pressure gauge case", case10, C_STEEL, "metal", 10, "shell", E10)
    dial = _ycyl(gx, gyc - 5, gyc - 5.4, gzc, 20.5)
    add("Gauge dial", dial, C_LABEL, "paper", 10, "shell", E10)
    ticks = []
    for i in range(9):
        a = math.radians(225 - 270 * i / 8)
        ticks.append(Pos(gx + 16 * math.cos(a), gyc - 5.55, gzc + 16 * math.sin(a)) * Rot(0, -math.degrees(a), 0) * Box(4, 0.3, 0.9))
    a = math.radians(40)
    ticks.append(Pos(gx + 6 * math.cos(a), gyc - 5.7, gzc + 6 * math.sin(a)) * Rot(0, -math.degrees(a), 0) * Box(15, 0.4, 1.4))
    ticks.append(_ycyl(gx, gyc - 5.5, gyc - 6.2, gzc, 1.8))
    add("Gauge scale and needle", _union(ticks), C_INK, "paper", 10, "shell", E10)
    arc = _ycyl(gx, gyc - 5.45, gyc - 5.6, gzc, 19) - _ycyl(gx, gyc - 5, gyc - 6, gzc, 17.5)
    arc &= _b(gx + 6, gx + 25, gyc - 10, gyc, gzc - 14, gzc + 4)
    add("Gauge red zone", arc, C_RED, "painted", 10, "shell", E10)
    glass = _ycyl(gx, gyc - 6.8, gyc - 7.6, gzc, 21)
    add("Gauge glass", glass, C_WINDOW, "clear", 10, "shell", E10)
    swp = _ycyl(TX, GY + 20, GY + 32, mz + 30, 6)
    add("Cut switch port", swp, C_BRASS, "metal", 10, "shell", E10)
    swb = _b(TX - 14, TX + 14, GY + 32, GY + 56, mz + 16, mz + 44)
    swb = _fillet_try(swb, swb.edges(), [3.0, 1.5])
    add("310 kPa gauge cut switch", swb, C_DARK, "plastic", 10, "shell", E10)
    swl = _b(TX + 14, TX + 14.4, GY + 36, GY + 52, mz + 22, mz + 38)
    add("Cut switch set-point label", swl, C_ACCENT, "paper", 10, "shell", E10)

    # ------------------------------------------------------------ 11 regulator and solenoid
    E11 = (150, -470, 30)
    rgx = P["reg_x"]
    rb = _b(rgx - 25, rgx + 25, GY - 20, GY + 20, deck_top, deck_top + 65)
    rb = _fillet_try(rb, _edges_par(rb, Axis.Z), [5.0, 3.0])
    rb = _fillet_try(rb, _top(rb), [2.0, 1.0])
    add("Regulator and valve body (brass)", rb, C_BRASS, "metal", 11, "shell", E11)
    rk = _front_face(_knob(11.0, 12.0), rgx, GY - 20, deck_top + 34)
    add("Regulator set knob", rk, C_BLACK, "rubber", 11, "shell", E11)
    coil = _zcyl(rgx, GY, deck_top + 65, deck_top + 115, 22)
    coil = _fillet_try(coil, coil.edges(), [3.0, 2.0])
    add("Solenoid coil (normally closed)", coil, C_BLACK, "plastic", 11, "shell", E11)
    cl = (_zcyl(rgx, GY, deck_top + 75, deck_top + 105, 22.3) - _zcyl(rgx, GY, deck_top + 74, deck_top + 106, 21)) \
        & _b(rgx - 14, rgx + 14, GY - 30, GY, deck_top + 70, deck_top + 110)
    add("Solenoid coil label", cl, C_LABEL, "paper", 11, "shell", E11)
    add_label("Regulator", placed(_label_layers(28, 20), _right_face, rgx + 25, GY, deck_top + 42), 17, "shell", E11)

    # ------------------------------------------------------------ 12 fuel cell
    E12 = (220, -150, 140)
    fl, fd, fhh = P["fc"]
    fcx0, fs = P["fc_x0"], P["fc_stand_h"]
    fz0 = deck_top + fs
    stand = _b(fcx0 - 5, fcx0 + fl + 5, GY - fd / 2 - 5, GY + fd / 2 + 5, deck_top, fz0)
    stand = _fillet_try(stand, _edges_par(stand, Axis.Z), [4.0, 2.0])
    stand = _fillet_try(stand, _top(stand), [1.5, 0.8])
    add("Fuel cell stand", stand, C_SHELL2, "painted", 12, "shell", E12)
    stack = _b(fcx0 + 6, fcx0 + fl - 6, GY - fd / 2, GY + fd / 2, fz0, fz0 + fhh)
    cp = (fl - 12) / 13
    for i in range(1, 13):
        xg = fcx0 + 6 + i * cp
        stack -= _b(xg - 0.5, xg + 0.5, GY - fd / 2 - 1, GY + fd / 2 + 1, fz0 + 3, fz0 + fhh + 1) \
            - _b(xg - 0.6, xg + 0.6, GY - fd / 2 + 1.2, GY + fd / 2 - 1.2, fz0 + 2, fz0 + fhh - 1.2)
    add("Fuel cell stack (13 cells)", stack, C_BLACK, "plastic", 12, "internal", E12)
    epl = []
    for a0 in (fcx0, fcx0 + fl - 6):
        e = _b(a0, a0 + 6, GY - fd / 2, GY + fd / 2, fz0, fz0 + fhh)
        epl.append(_fillet_try(e, _edges_par(e, Axis.X), [3.0, 1.5]))
    add("Fuel cell end plates", _union(epl), C_ACCENT, "painted", 12, "shell", E12)
    fy0 = GY - fd / 2
    fzc = fz0 + fhh / 2
    fan = _ycyl(fcx0 + fl / 2, fy0 - 8, fy0, fzc, 30) - _ycyl(fcx0 + fl / 2, fy0 - 9, fy0 - 2, fzc, 26)
    fan = _fillet_try(fan, _front(fan), [1.5, 0.8])
    add("Fan housing", fan, C_DARK, "plastic", 12, "shell", E12)
    blades = _ycyl(fcx0 + fl / 2, fy0 - 5, fy0 - 2, fzc, 8)
    for i in range(7):
        a = 360 * i / 7
        blades += Pos(fcx0 + fl / 2, fy0 - 3.5, fzc) * Rot(0, a, 0) * Pos(16, 0, 0) * Rot(20, 0, 0) * Box(18, 1.2, 7)
    add("Fan rotor", blades, C_BLACK, "plastic", 12, "internal", E12)
    grille = _ycyl(fcx0 + fl / 2, fy0 - 8.8, fy0 - 7.6, fzc, 27) - _ycyl(fcx0 + fl / 2, fy0 - 9, fy0 - 7, fzc, 25.5)
    grille += _ycyl(fcx0 + fl / 2, fy0 - 8.8, fy0 - 7.6, fzc, 16) - _ycyl(fcx0 + fl / 2, fy0 - 9, fy0 - 7, fzc, 14.8)
    grille += _ycyl(fcx0 + fl / 2, fy0 - 8.8, fy0 - 7.6, fzc, 6)
    for a in (0, 45, 90, 135):
        grille += Pos(fcx0 + fl / 2, fy0 - 8.2, fzc) * Rot(0, a, 0) * Box(53, 1.2, 1.4)
    add("Fan finger guard", grille, C_STEEL, "metal", 12, "shell", E12)
    fcin = _xcyl(fcx0 + fl - 1, fcx0 + fl + 8, GY + 10, fz0 + 20, 4) + _hex_x(fcx0 + fl + 1, GY + 10, fz0 + 20, 10.0, 4.0)
    add("Fuel cell inlet fitting", fcin, C_BRASS, "metal", 12, "shell", E12)
    add_label("Fuel cell", placed(_label_layers(36, 24), _right_face, fcx0 + fl, GY, fz0 + 46), 17, "shell", E12)

    # ------------------------------------------------------------ 13 electronic load and lamp
    E13 = (250, -380, 40)
    ll, ld, lh = P["load"]
    lx0, ly0 = P["load_x0"], P["load_y0"]
    lb = _b(lx0, lx0 + ll, ly0, ly0 + ld, deck_top, deck_top + lh)
    lb = _fillet_try(lb, _edges_par(lb, Axis.Y), [6.0, 4.0])
    lb = _fillet_try(lb, _edges_par(lb, Axis.Z), [3.0, 1.5])
    lb -= _b(lx0 - 1, lx0 + ll + 1, ly0 - 1, ly0 + 0.8, deck_top + 8, deck_top + 8.8)
    add("Electronic load case", lb, C_SHELL, "plastic", 13, "shell", E13)
    lsc = _b(lx0 + 12, lx0 + 62, ly0 - 0.3, ly0, deck_top + 18, deck_top + 40)
    add("Load display", lsc, C_SCREEN, "screen", 13, "shell", E13)
    ldg = _union([_b(lx0 + 16 + 10 * i, lx0 + 22 + 10 * i, ly0 - 0.6, ly0 - 0.3, deck_top + 23, deck_top + 35) for i in range(4)])
    add("Load readout (lit)", ldg, C_GLOW, "emissive", 13, "shell", E13)
    lk = _front_face(_knob(8.0, 9.0), lx0 + 82, ly0, deck_top + 28)
    add("Load current knob", lk, C_DARK, "rubber", 13, "shell", E13)
    lamp_x, lamp_y = lx0 + ll - 30, ly0 + ld / 2
    lbase = _zcyl(lamp_x, lamp_y, deck_top + lh, deck_top + lh + 14, 18)
    lbase = _fillet_try(lbase, _top(lbase), [3.0, 1.5])
    lbase += _zcyl(lamp_x, lamp_y, deck_top + lh + 14, deck_top + lh + 20, 9)
    add("Lamp holder", lbase, C_STEEL, "metal", 13, "shell", E13)
    bulb = Pos(lamp_x, lamp_y, deck_top + lh + 40 - 14) * Sphere(14) + _zcyl(lamp_x, lamp_y, deck_top + lh + 18, deck_top + lh + 26, 8)
    add("LED lamp (lit)", bulb, C_LAMP, "emissive", 13, "shell", E13)

    # ------------------------------------------------------------ 14 meters, logger and display
    E14 = (0, 220, 220)
    dz = deck_top + 350
    disp = _b(-120, 120, pf - 10, pf, dz, dz + 110)
    disp = _fillet_try(disp, _edges_par(disp, Axis.Y), [6.0, 4.0])
    disp = _fillet_try(disp, _front(disp), [1.5, 1.0])
    add("Logger display bezel", disp, C_BLACK, "plastic", 14, "shell", E14)
    add("Logger display glass", _b(-106, 106, pf - 10.3, pf - 10, dz + 12, dz + 98), C_SCREEN, "screen", 14, "shell", E14)
    ui = [_b(-100, -20, pf - 10.6, pf - 10.3, dz + 84, dz + 90)]
    pts = [(-98, 30), (-80, 48), (-62, 58), (-44, 64), (-26, 67), (-8, 68)]
    for (a, za), (b_, zb) in zip(pts, pts[1:]):
        ln = math.hypot(b_ - a, zb - za)
        ang = math.degrees(math.atan2(zb - za, b_ - a))
        ui.append(Pos((a + b_) / 2, pf - 10.45, dz + (za + zb) / 2) * Rot(0, -ang, 0) * Box(ln + 1.5, 0.3, 1.6))
    for i, hgt in enumerate((52, 38, 30, 14)):
        ui.append(_b(12 + 22 * i, 28 + 22 * i, pf - 10.6, pf - 10.3, dz + 20, dz + 20 + hgt))
    add("Logger display content (lit)", _union(ui), C_GLOW, "emissive", 14, "shell", E14)
    mets, glass14, digs = [], [], []
    for mx in (-380, -250, 250):
        m = _b(mx, mx + 90, pf - 8, pf, deck_top + 220, deck_top + 280)
        m = _fillet_try(m, _edges_par(m, Axis.Y), [4.0, 2.0])
        mets.append(m)
        glass14.append(_b(mx + 8, mx + 82, pf - 8.3, pf - 8, deck_top + 234, deck_top + 272))
        digs += [_b(mx + 14 + 12 * i, mx + 22 + 12 * i, pf - 8.6, pf - 8.3, deck_top + 250, deck_top + 266) for i in range(5)]
        digs.append(_b(mx + 14, mx + 60, pf - 8.6, pf - 8.3, deck_top + 239, deck_top + 243))
    add("Stage power meters", _union(mets), C_BLACK, "plastic", 14, "shell", E14)
    add("Stage meter windows", _union(glass14), C_SCREEN, "screen", 14, "shell", E14)
    add("Stage meter readouts (lit)", _union(digs), C_GLOW, "emissive", 14, "shell", E14)

    # ------------------------------------------------------------ 15 H2Guard (from its own project)
    E15 = (0, 0, 700)
    hx0, hx1 = dx_ - 40, dx_ + 40
    hy0, hy1 = dy_ - 100, dy_ - 60
    head = _b(hx0, hx1, hy0, hy1, TOP - 45, TOP)
    head = _fillet_try(head, _edges_par(head, Axis.Z), [6.0, 4.0])
    head = _fillet_try(head, head.faces().sort_by(Axis.Z)[0].edges(), [3.0, 2.0])
    for k in range(5):
        head -= _b(hx0 + 16 + 11 * k, hx0 + 20 + 11 * k, hy0 + 8, hy1 - 8, TOP - 46, TOP - 43.5)
    add("H2Guard sensor head", head, C_SHELL, "plastic", 15, "shell", E15)
    add("H2Guard head band", _b(hx0 + 8, hx1 - 8, hy0 - 0.4, hy0, TOP - 14, TOP - 10), C_ACCENT, "painted", 15, "shell", E15)
    add("H2Guard head status light (lit)", _ycyl(hx1 - 14, hy0 - 1.2, hy0, TOP - 28, 2.4), C_GREEN, "emissive", 15, "shell", E15)
    fz = dz1
    fanh = _zcyl(dx_, dy_, fz, fz + 50, dr + 12)
    fanh = _fillet_try(fanh, _top(fanh), [6.0, 4.0])
    fanh -= _zcyl(dx_, dy_, fz + 46, fz + 51, dr + 2)
    add("H2Guard extraction fan housing", fanh, C_SHELL, "plastic", 15, "shell", E15)
    fg = _zcyl(dx_, dy_, fz + 46, fz + 47.5, 16)
    for r0 in (26, 38, 50):
        fg += _zcyl(dx_, dy_, fz + 46, fz + 47.5, r0 + 1.5) - _zcyl(dx_, dy_, fz + 45, fz + 48, r0)
    for a in (0, 60, 120):
        fg += Pos(dx_, dy_, fz + 46.75) * Rot(0, 0, a) * Box(2 * dr + 4, 2.5, 1.5)
    add("H2Guard fan grille", fg, C_DARK, "plastic", 15, "shell", E15)
    add("H2Guard fan band", _zcyl(dx_, dy_, fz + 14, fz + 22, dr + 12.4) - _zcyl(dx_, dy_, fz + 13, fz + 23, dr + 11),
        C_ACCENT, "painted", 15, "shell", E15)
    cb = _b(90, 200, 90, 170, dz0, dz0 + 70)
    cb = _fillet_try(cb, _edges_par(cb, Axis.Z), [8.0, 5.0])
    cb = _fillet_try(cb, _top(cb), [3.0, 2.0])
    cb -= _b(88, 202, 88, 172, dz0 + 50, dz0 + 50.8) - _b(92, 198, 92, 168, dz0 + 49, dz0 + 52)
    add("H2Guard controller", cb, C_SHELL, "plastic", 15, "shell", E15)
    add("H2Guard controller window", _b(105, 185, 89.6, 90, dz0 + 14, dz0 + 42), C_SCREEN, "screen", 15, "shell", E15)
    add("H2Guard readout (lit)", _b(112, 160, 89.3, 89.6, dz0 + 26, dz0 + 34), C_GLOW, "emissive", 15, "shell", E15)
    add("H2Guard status light (lit)", _ycyl(175, 88.6, 89.6, dz0 + 30, 3.0), C_GREEN, "emissive", 15, "shell", E15)
    add_label("H2Guard", _wrap_label(40, 17, dx_, dy_, fz + 33, dr + 12, 25), 17, "shell", E15)

    # ------------------------------------------------------------ 16 gas lines (from model.py)
    add("Gas lines, 6 mm (PTFE)", base["Gas lines, 6 mm"], C_TUBE, "plastic", 16, "internal", (0, -200, 180))

    # ------------------------------------------------------------ context: existing lab table top
    top_ = _b(P["psu_x0"] - 50, L / 2 + 60, -D / 2 - 80, D / 2 + 30, -28, 0)   # long enough for the supply beside the bench
    top_ = _fillet_try(top_, _edges_par(top_, Axis.Z), [10.0, 6.0])
    top_ = _fillet_try(top_, _top(top_), [3.0, 2.0])
    add("Lab table top (existing)", top_, C_TABLE, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
