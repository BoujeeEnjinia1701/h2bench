"""H2Bench concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Proportions, main parts and interfaces; not for fabrication.

Axes: X along the bench, left to right in the order the energy flows (water and power in,
electrolyzer, gas treatment, buffer tank, regulator, fuel cell, load). Y front (-Y, student
side) to back (+Y, instrument panel). Z up; Z = 0 is the top of the existing lab table.
Units mm. Energy figures are from HBN-CAL-001 (paper estimates, not measurements).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all, human_figure, _render  # noqa: E402
from model import PARAMS, build_parts  # noqa: E402

parts = [Part(n, s, c, bom, e) for n, s, c, bom, e in build_parts()]


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


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
    date="2026-10-02",
    key_figures=["Electrolyzer 70 W, 4-cell PEM, 256 mL/min H2",
                 "2.0 L tank, 7.9 L H2 at 300 kPa gauge; relief 325",
                 "Fill 17.7 min; fuel cell 10.8 W net for 29.0 min",
                 "Round trip 25.1 %, HHV basis (HBN-CAL-001)",
                 "Bench 900 x 450 mm, 753 mm tall, about 24 kg",
                 "Runs only with the H2Guard interlock active"],
    scale_figure=False, context=context, cut=False,
    flow={"title": "energy per lesson cycle, HHV basis (estimates, HBN-CAL-001)", "unit": "Wh",
          "stages": [("Electricity in", 20.8), ("Electrolyzer (H2)", 15.0), ("Buffer tank", 14.7),
                     ("Fuel cell, net DC", 5.2)],
          "losses": [(1, "Electrolyzer heat (est.)", 5.8), (2, "Leak, vent (est.)", 0.3),
                     (3, "FC heat, purge, fan (est.)", 9.5)]},
)
# Cutaway: the kit cuts at the mean Y of all parts, which misses the gas train. Cut instead on
# the gas train centreline (Y = gas_y) and keep the back half, looking from the front.
cutter = Pos(0, PARAMS["gas_y"] + 5000, 0) * Box(10000, 10000, 10000)
cut_parts = []
for p in parts:
    try:
        c = p.shape & cutter
        if c.volume > 1e-6:
            cut_parts.append(Part(p.name, c, p.color, p.bom, p.explode, p.alpha))
    except Exception:
        cut_parts.append(p)
_render(cut_parts, ROOT / "media/cutaway.png", azim=-90, elev=18, title="H2Bench: cutaway on the gas train centreline")

for d in (ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
print("media refreshed")
