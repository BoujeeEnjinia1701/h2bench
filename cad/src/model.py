"""H2Bench parametric model (build123d), TRL 3 (HBN-DDR-002 decisions applied).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl and prints the main envelopes.

Massing-plus detail: correct main dimensions and interfaces (gas train order and ports, tank
internal volume, guard clearance, canopy high point and duct, H2Guard sensor position); not
fabrication detail. Geometry for HBN-DWG-001 and the concept media is built from here.

Axes: X along the bench, left to right in the order the energy flows (water and power in,
electrolyzer, gas treatment, buffer tank, regulator, fuel cell, load). Y front (-Y, student
side) to back (+Y, instrument panel). Z up; Z = 0 is the top of the existing lab table.
Units mm.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Bench (HBN-REQ-001 R13)
    "bench_l": 900.0, "bench_d": 450.0,
    "frame_h": 20.0,            # 20 x 20 mm aluminium extrusion frame
    "deck_t": 12.0,             # HDPE deck with drip lip
    "lip_h": 8.0,
    "panel_t": 3.0, "panel_standoff": 17.0,
    "canopy_clear": 570.0,      # deck top to canopy underside
    "canopy_t": 3.0, "canopy_front_y": -120.0,
    "post": 20.0,
    "duct_d": 100.0, "duct_h": 100.0, "duct_x": 0.0, "duct_y": 120.0,
    # Gas train centreline
    "gas_y": -40.0, "tube_od": 6.0,
    # 4 Bench power supply (L x D x H)
    "psu": (150.0, 210.0, 140.0), "psu_x0": -440.0, "psu_y0": -20.0,
    # 5 Reservoir and deionizer
    "res_d": 110.0, "res_h": 170.0, "res_x": -370.0, "res_y": -140.0,
    # 6 PEM electrolyzer: 4 cells, 56 cm2 active area class, 25 mm cell pitch
    "ely_cells": 4, "ely_pitch": 25.0, "ely_plate": 90.0, "ely_end_t": 15.0,
    "ely_x0": -215.0, "ely_z0": 45.0,
    # 7 Separator and drier
    "sep_d": 60.0, "sep_h": 160.0, "sep_x": -30.0, "drier_d": 40.0, "drier_h": 130.0, "drier_x": 25.0,
    # 9 Buffer tank: internal volume is the design input, cylinder length follows from it
    "tank_v_l": 2.0, "tank_od": 110.0, "tank_wall": 3.0, "tank_x": 175.0, "tank_z0": 50.0,
    "guard_offset": 78.0, "guard_rod_d": 10.0, "guard_top_gap": 60.0,
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


def envelope(p=PARAMS):
    """Overall bench envelope above the lab table (mm): length, depth, height."""
    deck_top, top = levels(p)
    height = top + p["canopy_t"] + p["duct_h"] + 50.0   # H2Guard fan housing is 50 mm on the duct
    return p["bench_l"], p["bench_d"], height


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _vcyl(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _xcyl(x0, x1, y, z, r):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _ycyl(x, y0, y1, z, r):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Pos, Sphere
    b, vc, xc, yc = _box, _vcyl, _xcyl, _ycyl
    L, D = p["bench_l"], p["bench_d"]
    deck_top, TOP = levels(p)
    fh = p["frame_h"]
    GY, tr = p["gas_y"], p["tube_od"] / 2
    parts = []

    # 1 Bench deck on a 20 x 20 mm extrusion frame, with a drip lip round the deck
    s = p["post"]
    frame = (b(-L / 2, L / 2, -D / 2, -D / 2 + s, 0, fh) + b(-L / 2, L / 2, D / 2 - s, D / 2, 0, fh)
             + b(-L / 2, -L / 2 + s, -D / 2, D / 2, 0, fh) + b(L / 2 - s, L / 2, -D / 2, D / 2, 0, fh)
             + b(-L / 6 - s / 2, -L / 6 + s / 2, -D / 2, D / 2, 0, fh)
             + b(L / 6 - s / 2, L / 6 + s / 2, -D / 2, D / 2, 0, fh))
    deck = b(-L / 2, L / 2, -D / 2, D / 2, fh, deck_top)
    lip = (b(-L / 2, L / 2, -D / 2, D / 2, deck_top, deck_top + p["lip_h"])
           - b(-L / 2 + 6, L / 2 - 6, -D / 2 + 6, D / 2 - 6, deck_top - 1, deck_top + p["lip_h"] + 1))
    parts.append(("Bench deck and extrusion frame", frame + deck + lip, "#9CA3AF", 1, (0, 0, -300)))

    # 2 Instrument back panel on standoffs at the rear edge
    py1 = D / 2
    panel = b(-L / 2, L / 2, py1 - p["panel_t"], py1, deck_top + p["lip_h"], TOP)
    parts.append(("Instrument back panel", panel, "#D1D5DB", 2, (0, 480, -120)))

    # 3 Canopy hood with the duct collar at its single high point, and two front posts
    cy0 = p["canopy_front_y"]
    dr = p["duct_d"] / 2
    canopy = (b(-L / 2, L / 2, cy0, D / 2, TOP, TOP + p["canopy_t"])
              - vc(p["duct_x"], p["duct_y"], TOP - 1, TOP + p["canopy_t"] + 1, dr))
    canopy = canopy + (vc(p["duct_x"], p["duct_y"], TOP, TOP + p["canopy_t"] + p["duct_h"], dr + 3)
                       - vc(p["duct_x"], p["duct_y"], TOP - 1, TOP + p["canopy_t"] + p["duct_h"] + 1, dr))
    zl = deck_top + p["lip_h"]
    canopy = canopy + b(-L / 2, -L / 2 + s, cy0, cy0 + s, zl, TOP) + b(L / 2 - s, L / 2, cy0, cy0 + s, zl, TOP)
    parts.append(("Canopy hood, duct and posts", canopy, "#BFDBFE", 3, (0, 0, 480)))

    # 4 Bench DC power supply, 0 to 30 V, 0 to 10 A
    pl, pd, ph = p["psu"]
    x0, y0 = p["psu_x0"], p["psu_y0"]
    psu = b(x0, x0 + pl, y0, y0 + pd, deck_top, deck_top + ph) + b(x0 + 10, x0 + pl - 10, y0 - 4, y0, deck_top + 30, deck_top + ph - 20)
    parts.append(("Bench DC power supply, 0 to 30 V, 10 A", psu, "#374151", 4, (-260, 0, 120)))

    # 5 Reservoir and deionizer cartridge
    rx, ry = p["res_x"], p["res_y"]
    water = vc(rx, ry, deck_top, deck_top + p["res_h"], p["res_d"] / 2) + vc(rx + 100, ry - 10, deck_top, deck_top + 200, 25)
    parts.append(("DI water reservoir and deionizer", water, "#38BDF8", 5, (-200, -300, 60)))

    # 6 PEM electrolyzer: end plates, tie rods and feet; cell block and membranes as unnumbered parts
    ex0, n, pitch, pp, et = p["ely_x0"], p["ely_cells"], p["ely_pitch"], p["ely_plate"], p["ely_end_t"]
    ez0 = p["ely_z0"]
    block_l = n * pitch
    ex1 = ex0 + 2 * et + block_l
    ezc = ez0 + (pp + 20) / 2
    ely = (b(ex0, ex0 + et, GY - (pp + 20) / 2, GY + (pp + 20) / 2, ez0, ez0 + pp + 20)
           + b(ex1 - et, ex1, GY - (pp + 20) / 2, GY + (pp + 20) / 2, ez0, ez0 + pp + 20)
           + b(ex0, ex1, GY - 50, GY - 30, deck_top, ez0) + b(ex0, ex1, GY + 30, GY + 50, deck_top, ez0))
    for dy in (-(pp + 4) / 2, (pp + 4) / 2):
        for z in (ez0 + 7, ez0 + pp + 13):
            ely = ely + xc(ex0 - 10, ex1 + 10, GY + dy, z, 4)
    # ports on the right end plate: H2 out (upper, toward the separator), O2 out to the hood (rear)
    ely = ely + xc(ex1, ex1 + 12, GY, ezc + 25, 5) + yc(ex0 + et + 10, GY + (pp + 20) / 2, GY + (pp + 20) / 2 + 12, ezc + 30, 5)
    plates = b(ex0 + et, ex1 - et, GY - pp / 2, GY + pp / 2, ez0 + 10, ez0 + pp + 10)
    meas = _union([b(ex0 + et + i * pitch + 10, ex0 + et + i * pitch + 16, GY - pp / 2 + 3, GY + pp / 2 - 3,
                     ez0 + 13, ez0 + pp + 7) for i in range(n)])
    plates = plates - meas
    parts.append(("PEM electrolyzer stack, about 70 W", ely, "#0F766E", 6, (-40, -260, 220)))
    parts.append(("Electrolyzer cells (plates and MEAs)", plates, "#9CA3AF", None, (-40, -260, 220)))
    parts.append(("Electrolyzer membranes", meas, "#111827", None, (-40, -260, 220)))

    # 7 Separator column and silica gel drier
    sep = (vc(p["sep_x"], GY, deck_top, deck_top + p["sep_h"], p["sep_d"] / 2)
           + vc(p["drier_x"], GY, deck_top, deck_top + p["drier_h"], p["drier_d"] / 2))
    parts.append(("Gas and water separator, drier", sep, "#6B7280", 7, (0, -380, 100)))

    # 8 Check valve and flame arrestor inline on a post
    gz = deck_top + 150.0                     # gas line height between drier and tank
    arrestor = xc(50, 105, GY, gz, 14) + b(70, 85, GY - 8, GY + 8, deck_top, gz - 13)
    parts.append(("Check valve and flame arrestor", arrestor, "#B45309", 8, (0, -300, 330)))

    # 9 Buffer tank: shell with flat base and domed top, cradle and four-rod guard with top ring
    TX, TR, tw, tz0 = p["tank_x"], p["tank_od"] / 2, p["tank_wall"], p["tank_z0"]
    lc = tank_cyl_len(p)
    tz1 = tz0 + tw + lc                        # start of the dome (inner and outer share it)
    shell_out = vc(TX, GY, tz0, tz1, TR) + Pos(TX, GY, tz1) * Sphere(TR)
    shell_in = vc(TX, GY, tz0 + tw, tz1, TR - tw) + Pos(TX, GY, tz1) * Sphere(TR - tw)
    tank = shell_out - shell_in
    tank = tank + b(TX - 65, TX + 65, GY - 65, GY + 65, deck_top, tz0)
    tank_top = tz1 + TR
    g_top = tank_top + p["guard_top_gap"]
    go, gr = p["guard_offset"], p["guard_rod_d"] / 2
    for dx in (-go, go):
        for dy in (-go, go):
            tank = tank + vc(TX + dx, GY + dy, deck_top, g_top, gr)
    tank = tank + (b(TX - go - 5, TX + go + 5, GY - go - 5, GY + go + 5, g_top - 8, g_top)
                   - b(TX - go + 5, TX + go - 5, GY - go + 5, GY + go - 5, g_top - 9, g_top + 1))
    parts.append(("Hydrogen buffer tank, 2 L, with guard", tank, "#E5E7EB", 9, (0, -120, 60)))

    # 10 Tank manifold on the top boss: transducer, thermistor, relief valve (325 kPa g), gauge,
    #    vent needle valve and the pressure switch that cuts the supply at 310 kPa g (HBN-DDR-002)
    mz = tank_top
    manifold = (vc(TX, GY, mz - 2, mz + 15, 10)
                + b(TX - 30, TX + 30, GY - 20, GY + 20, mz + 15, mz + 45)
                + vc(TX + 20, GY, mz + 45, mz + 80, 8)                      # relief valve
                + Pos(TX - 5, GY - 27, mz + 65) * _ycyl(0, -7, 7, 0, 24)    # gauge
                + vc(TX - 20, GY, mz + 45, mz + 70, 6)                      # vent needle valve
                + _ycyl(TX, GY + 20, GY + 32, mz + 30, 6)                   # port to the cut switch
                + b(TX - 14, TX + 14, GY + 32, GY + 56, mz + 16, mz + 44))  # 310 kPa g cut switch
    parts.append(("Tank manifold: sensors, relief, gauge", manifold, "#C2410C", 10, (0, -120, 250)))

    # 11 Normally closed solenoid valve and regulator
    rx = p["reg_x"]
    reg = b(rx - 25, rx + 25, GY - 20, GY + 20, deck_top, deck_top + 65) + vc(rx, GY, deck_top + 65, deck_top + 115, 22)
    parts.append(("Regulator and solenoid valve", reg, "#D4A017", 11, (60, -440, 0)))

    # 12 Fuel cell stack (75 x 47 x 70 mm) with front fan on a stand
    fl, fd, fhh = p["fc"]
    fx0, fs = p["fc_x0"], p["fc_stand_h"]
    fz0 = deck_top + fs
    fc = (b(fx0 - 5, fx0 + fl + 5, GY - fd / 2 - 5, GY + fd / 2 + 5, deck_top, fz0)
          + b(fx0, fx0 + fl, GY - fd / 2, GY + fd / 2, fz0, fz0 + fhh)
          + yc(fx0 + fl / 2, GY - fd / 2 - 8, GY - fd / 2, fz0 + fhh / 2, 30))
    parts.append(("PEM fuel cell, 12 W class", fc, "#1F2937", 12, (220, -150, 140)))

    # 13 Electronic load and lamp at the front right
    ll, ld, lh = p["load"]
    lx0, ly0 = p["load_x0"], p["load_y0"]
    load = b(lx0, lx0 + ll, ly0, ly0 + ld, deck_top, deck_top + lh) + vc(lx0 + ll - 30, ly0 + ld / 2, deck_top + lh, deck_top + lh + 40, 18)
    parts.append(("Electronic load and lamp", load, "#FACC15", 13, (250, -300, -60)))

    # 14 Meters: display and three stage power meters on the panel face
    pf = py1 - p["panel_t"]
    meters = b(-120, 120, pf - 10, pf, deck_top + 350, deck_top + 460)
    for mx in (-380, -250, 250):
        meters = meters + b(mx, mx + 90, pf - 8, pf, deck_top + 220, deck_top + 280)
    parts.append(("Meters, logger and display", meters, "#15803D", 14, (0, 220, 220)))

    # 15 H2Guard (massing stand-in): sensor head at the canopy high point next to the duct,
    #    extraction fan housing on the duct, controller box on the canopy
    dz1 = TOP + p["canopy_t"] + p["duct_h"]
    guard = (b(p["duct_x"] - 40, p["duct_x"] + 40, p["duct_y"] - 100, p["duct_y"] - 60, TOP - 45, TOP)
             + vc(p["duct_x"], p["duct_y"], dz1, dz1 + 50, dr + 12)
             + b(90, 200, 90, 170, TOP + p["canopy_t"], TOP + 73))
    parts.append(("H2Guard sensor, controller and fan", guard, "#DC2626", 15, (0, 0, 700)))

    # 16 Gas lines, 6 mm OD (not numbered in the exploded view): electrolyzer H2 port to the
    #    separator, drier to arrestor to tank manifold, manifold to solenoid, regulator to fuel cell,
    #    and the relief and vent line up to the canopy
    hz = ezc + 25
    tubes = [xc(ex1 + 12, p["sep_x"] - p["sep_d"] / 2, GY, hz, tr),
             xc(p["sep_x"] + p["sep_d"] / 2, p["drier_x"] - p["drier_d"] / 2, GY, deck_top + 110, tr),
             vc(p["drier_x"], GY, deck_top + p["drier_h"], gz, tr), xc(p["drier_x"], 50, GY, gz, tr),
             xc(105, 108, GY, gz, tr), vc(108, GY, gz, mz + 30, tr),
             xc(108, TX - 30, GY, mz + 30, tr),
             xc(TX + 30, rx, GY, mz + 30, tr), vc(rx, GY, deck_top + 115, mz + 30, tr),
             xc(rx + 25, fx0, GY, deck_top + 45, tr),
             vc(TX + 20, GY, mz + 80, TOP, tr)]
    parts.append(("Gas lines, 6 mm", _union(tubes), "#78716C", None, (0, -200, 180)))
    return parts


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


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    parts = build_parts()
    asm = assemblies(parts)
    for name, shape in asm.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
        print(f"wrote cad/step/{name}.step and cad/stl/{name}.stl")
    bbs = [s.bounding_box(optimal=True) for _, s, *_ in parts]
    size = [max(getattr(b.max, a) for b in bbs) - min(getattr(b.min, a) for b in bbs) for a in "XYZ"]
    l, d, h = envelope()
    print(f"assembly envelope {size[0]:.0f} x {size[1]:.0f} x {size[2]:.0f} mm (above the lab table)")
    print(f"envelope parameters {l:.0f} x {d:.0f} x {h:.0f} mm")
    print(f"tank internal volume {tank_internal_volume_l():.3f} L, straight length {tank_cyl_len():.1f} mm")
    # simple clash check between numbered parts (tubes and the cell block excluded)
    import itertools
    named = [(n, s) for n, s, c, bom, e in parts if bom is not None]
    clashes = []
    for (n1, s1), (n2, s2) in itertools.combinations(named, 2):
        try:
            v = (s1 & s2).volume
        except Exception:
            v = 0.0
        if v > 1.0 and {n1, n2} != {"Hydrogen buffer tank, 2 L, with guard", "Tank manifold: sensors, relief, gauge"}:
            clashes.append((n1, n2, v))  # the manifold boss entering the tank port is intended
    for c in clashes:
        print(f"overlap: {c[0]} / {c[1]}: {c[2]:.0f} mm3")
    print(f"clash check: {len(clashes)} overlaps between numbered parts")
