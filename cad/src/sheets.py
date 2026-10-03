"""H2Bench general arrangement drawing HBN-DWG-001 (Rev P4).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/HBN-DWG-001.svg, .pdf and .png from the parametric model.
HBN-DWG-001 is free because the concept blueprint uses HBN-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, envelope, levels, tank_cyl_len, tank_internal_volume_l  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["h2bench-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
l, d, h = envelope()
deck_top, top = levels()

s = Sheet(project="H2Bench", title="General arrangement, hydrogen teaching bench", dwg_no="HBN-DWG-001",
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Frame, posts, top frame 20 x 20 Al extrusion; deck 10 HDPE; canopy 3 PC; tank 1 MPa rated. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 parametric model (HBN-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Relief 325 kPa g; 310 kPa g supply cut switch added (HBN-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Constructable design: posts, top frame, mounts, water lines (HBN-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "10 mm deck, supply beside the bench, catalytic deoxidizer (HBN-DEC-001)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 282, 42, 128, 76, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Bench {l:.0f} x {d:.0f}, {h:.0f} tall above the lab table",
    f"Deck top {deck_top:.0f}; canopy underside {top:.0f}; duct {P['duct_d']:.0f} ID",
    "Energy flows left to right: water, stack, separator,",
    "  deoxidizer, drier, arrestor, tank, regulator, fuel cell",
    f"Tank {tank_internal_volume_l():.2f} L internal, OD {P['tank_od']:.0f}, wall {P['tank_wall']:.0f},",
    f"  straight {tank_cyl_len():.0f}; four M10 guard rods on a {2 * P['guard_offset']:.0f} square",
    "Working 300 kPa g; supply cut 310 kPa g; relief 325 kPa g",
    "Relief and vent lines 6 OD to a hanger under the canopy",
    "Vent needle valve: 300 to 20 kPa g in 3 min or more",
    "H2Guard sensor at the canopy high point beside the duct",
    "Fuel cell supply about 50 kPa g; 12 W class, 75 x 47 x 70",
    "Supply stands on the lab table beside the bench",
    "Bench about 24.4 kg without its supply (HBN-CAL-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=133, width=140)
s.save(ROOT / "cad/drawings/HBN-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/HBN-DWG-001.svg, .pdf, .png")
