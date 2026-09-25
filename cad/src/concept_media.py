"""H2Bench concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the bench, left to right in the order the energy flows (water and power in,
electrolyzer, gas treatment, buffer tank, regulator, fuel cell, load). Y front (-Y, student
side) to back (+Y, instrument panel). Z up; the bench deck sits on an existing lab table.
Units mm. Energy figures are first-order estimates from HBN-PRC-001.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot
from concept import Part, render_all, human_figure


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def vcyl(x, y, z0, z1, r):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def xcyl(x0, x1, y, z, r):
    """Cylinder along X."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


L, D = 900.0, 450.0          # bench deck length (X) and depth (Y)
DECK = 30.0                  # deck top height above the lab table
TOP = 600.0                  # canopy underside
GY = -40.0                   # Y of the gas train centreline

# 1 Bench deck on an aluminium extrusion frame
deck = box(-L / 2, L / 2, -D / 2, D / 2, 0, DECK)

# 2 Instrument back panel
panel = box(-L / 2, L / 2, D / 2 - 20, D / 2, DECK, TOP)

# 3 Canopy hood with extraction duct and two front posts (hydrogen rises into it)
canopy = (box(-L / 2, L / 2, -120, D / 2, TOP, TOP + 10)
          + box(-L / 2, -L / 2 + 20, -120, -100, DECK, TOP)
          + box(L / 2 - 20, L / 2, -120, -100, DECK, TOP)
          + (vcyl(0, 120, TOP + 10, TOP + 110, 55) - vcyl(0, 120, TOP - 1, TOP + 111, 50)))

# 4 Bench DC power supply, 0 to 30 V, 10 A
psu = box(-440, -290, -20, 190, DECK, 170) + box(-430, -300, -24, -20, 60, 150)

# 5 Deionized water reservoir and deionizer cartridge
water = vcyl(-370, -140, DECK, 200, 55) + vcyl(-270, -150, DECK, 230, 25)

# 6 PEM electrolyzer stack, 4 cells, about 70 W: end plates, tie rods and feet, with the cell
#   block (titanium plates and four membrane electrode assemblies) as a separate unnumbered part
ely = (box(-215, -200, GY - 55, GY + 55, 45, 155) + box(-100, -85, GY - 55, GY + 55, 45, 155)
       + box(-215, -85, GY - 50, GY - 30, DECK, 45) + box(-215, -85, GY + 30, GY + 50, DECK, 45))
plates = box(-200, -100, GY - 45, GY + 45, 55, 145)
meas = None
for i in range(4):
    x0 = -196 + i * 25
    slab = box(x0 + 8, x0 + 14, GY - 42, GY + 42, 58, 142)
    meas = slab if meas is None else meas + slab
plates = plates - meas
for dy in (-47, 47):
    for z in (52, 148):
        ely = ely + xcyl(-225, -75, GY + dy, z, 4)

# 7 Gas and water separator with silica gel drier
sep = vcyl(-30, GY, DECK, 190, 30) + vcyl(25, GY, DECK, 160, 20)

# 8 Check valve and flame arrestor, inline, on a small post
arrestor = xcyl(50, 105, GY, 150, 14) + box(70, 85, GY - 8, GY + 8, DECK, 137)

# 9 Hydrogen buffer tank, 2 L, with cradle and tube guard
TX, TR, TZ0, TZ1 = 175.0, 55.0, 50.0, 300.0
shell_out = vcyl(TX, GY, TZ0, TZ1, TR) + Pos(TX, GY, TZ1) * Sphere(TR)
shell_in = vcyl(TX, GY, TZ0 + 3, TZ1, TR - 3) + Pos(TX, GY, TZ1) * Sphere(TR - 3)
tank = (shell_out - shell_in) + vcyl(TX, GY, TZ0 - 2, TZ0 + 3, TR)
tank = tank + box(TX - 65, TX + 65, GY - 65, GY + 65, DECK, TZ0 - 2)
for dx in (-78, 78):
    for dy in (-78, 78):
        tank = tank + vcyl(TX + dx, GY + dy, DECK, 365, 5)
tank = tank + (box(TX - 83, TX + 83, GY - 83, GY + 83, 360, 368) - box(TX - 73, TX + 73, GY - 73, GY + 73, 359, 369))

# 10 Tank manifold: pressure transducer, thermistor, relief valve, gauge, manual vent
manifold = (box(TX - 30, TX + 30, GY - 20, GY + 20, 352, 385)
            + vcyl(TX + 20, GY, 385, 420, 8)
            + Pos(TX - 5, GY - 27, 405) * Rot(90, 0, 0) * Cylinder(24, 14)
            + box(TX - 10, TX, GY - 20, GY - 20 + 1, 385, 393))

# 11 Pressure regulator (to about 50 kPa gauge) on a normally closed solenoid valve
reg = box(255, 305, GY - 20, GY + 20, DECK, 95) + vcyl(280, GY, 95, 145, 22)

# 12 PEM fuel cell, 12 W class, open cathode, on a stand with its fan on the front face
fc = (box(330, 430, GY - 55, GY + 55, DECK, 45) + box(330, 430, GY - 55, GY + 55, 45, 145)
      + Pos(380, GY - 58, 95) * Rot(90, 0, 0) * Cylinder(36, 6))

# 13 Electronic load and lamp panel
load = box(300, 440, -215, -160, DECK, 80) + vcyl(410, -188, 80, 120, 18)

# 14 Meters and logger: display and three stage power meters on the panel face
meters = box(-120, 120, D / 2 - 30, D / 2 - 20, 380, 490)
for x0 in (-380, -250, 250):
    meters = meters + box(x0, x0 + 90, D / 2 - 28, D / 2 - 20, 250, 310)

# 15 H2Guard: sensor head under the canopy beside the duct, extraction fan on the duct and
#    controller box on the canopy roof (a massing stand-in for the H2Guard wall unit)
guard = (box(-40, 40, 20, 60, TOP - 45, TOP)
         + vcyl(0, 120, TOP + 110, TOP + 160, 62)
         + box(90, 200, 90, 170, TOP + 10, TOP + 80))

parts = [
    Part("Bench deck and extrusion frame", deck, "#9CA3AF", 1, (0, 0, -300)),
    Part("Instrument back panel", panel, "#D1D5DB", 2, (0, 480, -120)),
    Part("Canopy hood, duct and posts", canopy, "#BFDBFE", 3, (0, 0, 480)),
    Part("Bench DC power supply, 0 to 30 V, 10 A", psu, "#374151", 4, (-260, 0, 120)),
    Part("DI water reservoir and deionizer", water, "#38BDF8", 5, (-200, -300, 60)),
    Part("PEM electrolyzer stack, about 70 W", ely, "#0F766E", 6, (-40, -260, 220)),
    Part("Electrolyzer cells (plates and MEAs)", plates, "#9CA3AF", None, (-40, -260, 220)),
    Part("Electrolyzer membranes", meas, "#111827", None, (-40, -260, 220)),
    Part("Gas and water separator, drier", sep, "#6B7280", 7, (0, -380, 100)),
    Part("Check valve and flame arrestor", arrestor, "#B45309", 8, (0, -300, 330)),
    Part("Hydrogen buffer tank, 2 L, with guard", tank, "#E5E7EB", 9, (0, -120, 60)),
    Part("Tank manifold: sensors, relief, gauge", manifold, "#C2410C", 10, (0, -120, 250)),
    Part("Regulator and solenoid valve", reg, "#D4A017", 11, (60, -440, 0)),
    Part("PEM fuel cell, 12 W class", fc, "#1F2937", 12, (220, -150, 140)),
    Part("Electronic load and lamp", load, "#FACC15", 13, (250, -300, -60)),
    Part("Meters, logger and display", meters, "#15803D", 14, (0, 220, 220)),
    Part("H2Guard sensor, controller and fan", guard, "#DC2626", 15, (0, 0, 700)),
]

# Context for scale: the existing lab table the bench sits on, and a 1.75 m person on the floor
TH = 750.0
table = box(-700, 700, -350, 350, -30, 0)
for sx in (-1, 1):
    for sy in (-1, 1):
        table = table + box(sx * 660 - 20, sx * 660 + 20, sy * 310 - 20, sy * 310 + 20, -TH, -30)
person = human_figure(1750.0, x=1250.0, y=-100.0, z=-TH)
context = [Part("Lab table (existing)", table, "#C8CDD3"), person]

render_all(
    parts, project="H2Bench", title="Hydrogen teaching bench concept", dwg_no="HBN-DWG-010",
    date="2026-09-25",
    key_figures=["Electrolyzer about 70 W, 4-cell PEM (estimate)",
                 "About 7.9 L H2 held at up to 300 kPa gauge",
                 "Fill about 18 min; fuel cell 11 W for 29 min (est.)",
                 "Round trip about 25 %, HHV basis (estimate)",
                 "Bench 900 x 450 mm, about 770 mm tall",
                 "Runs only with the H2Guard interlock active"],
    scale_figure=False, context=context,
    flow={"title": "energy per lesson cycle, HHV basis (all values are estimates)", "unit": "Wh",
          "stages": [("Electricity in", 20.8), ("Electrolyzer (H2)", 15.0), ("Buffer tank", 14.7),
                     ("Fuel cell, net DC", 5.2)],
          "losses": [(1, "Electrolyzer heat (est.)", 5.8), (2, "Leak, vent (est.)", 0.3),
                     (3, "FC heat, purge, fan (est.)", 9.5)]},
)
