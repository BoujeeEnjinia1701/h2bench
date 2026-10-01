"""H2Bench sizing calculations, HBN-CAL-001 v0.4 (TRL 3, constructable design, HBN-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles paper estimates; nothing here is measured. The script reads the tank and
bench dimensions and the made parts' volumes from cad/src/model.py and the costs from bom/bom.csv.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, envelope, tank_cyl_len, tank_internal_volume_l, build_components  # noqa: E402

# ---------------------------------------------------------------- 1. Assumptions
F = 96485.0            # C/mol
R = 8.314              # J/(mol K)
T0 = 293.15            # K, 20 degC reference and lab temperature
P_ATM = 101.325        # kPa
VM = R * T0 / P_ATM    # L/mol at 20 degC and 101.325 kPa (24.05)
M_H2 = 2.016           # g/mol
HHV = 285.83           # kJ/mol
LHV = 241.83           # kJ/mol
GAMMA = 1.41           # hydrogen, near room temperature
Z_H2_400 = 1.0024      # compressibility of H2 at about 400 kPa, 20 degC (used as a correction only)

# Electrolyzer (HBN-PRC-001 v0.3)
N_ELY, V_CELL_ELY, I_ELY, ETA_F = 4, 1.95, 9.0, 0.95
V_CELL_ELY_AGED = 2.20           # end-of-life cell voltage for the supply check
PSU_V, PSU_I = 30.0, 10.0
V_TN = 1.481                     # V, thermoneutral voltage (HHV)

# Tank and pressures (kPa gauge unless noted)
V_TANK = tank_internal_volume_l()          # L, from the model (2.000)
V_LINES = 0.15                   # L, separator headspace, drier and lines at tank pressure
P_LOW, P_HIGH, P_RELIEF, P_KEEP = 70.0, 300.0, 325.0, 20.0
P_CUT = 310.0                    # kPa gauge, pressure switch cuts the electrolyzer supply (HBN-DDR-002)
RELIEF_ACCUM = 0.10              # relief valve overpressure at full lift, fraction of set
CRACK = 7.0                      # check valve cracking pressure
T_COLD = 288.15                  # K, 15 degC lab (coldest in HBN-PRB-001)
STORAGE_LOSS = 0.02              # fraction lost to leaks and line purges per cycle

# Fuel cell (Fuel Cell Store listing for the 12 W class; HBN-PRC-001 v0.3)
N_FC, V_CELL_FC, I_FC, UTIL, P_AUX = 13, 0.60, 1.5, 0.95, 0.9
FC_LISTED_FLOW = 0.18            # L/min at full output (listing)
P_FC_SUPPLY = 50.0               # kPa gauge

# Measurement (HBN-REQ-001 R1)
PT_FS, PT_ACC = 600.0, 0.0025    # kPa absolute full scale, accuracy fraction of FS
DT_THERM = 1.0                   # K, thermistor
DV_TANK = 0.01                   # tank volume calibrated by water fill
DP_POWER = 0.01                  # INA226 plus shunt, fraction of reading

# Room, hood and H2Guard (HGD-PRC-001 v0.2, HGD-REQ-001 v0.2)
ROOM_M3 = 30.0
LFL = 4.0                        # % vol
H2G_WARN, H2G_TRIP = 0.4, 1.0    # % vol (10 % and 25 % LFL)
Q_HOOD = 60.0                    # m3/h assumed through the canopy duct (H2Guard runs 150 m3/h room exhaust)
T_VENT_SET = 180.0               # s, vent needle valve setting, 300 to 20 kPa gauge
T_RELAY, T_VALVE = 0.1, 1.0      # s, H2Guard comparator and relay, solenoid closing (HGD-PRC-001)

# Water and drier
T_SEP = 298.15                   # K, gas leaving the separator
P_SAT_SEP = 3.17                 # kPa, water vapour pressure at 25 degC
GEL_G, GEL_CAP = 50.0, 0.10      # g silica gel, usable water uptake fraction at low humidity

# Mass estimates, kg. Made parts are weighed from their model volumes (HBN-DDR-003); bought
# parts use typical catalogue masses.
COMP = build_components()
RHO = {"al": 2.70e-6, "hdpe": 0.95e-6, "pc": 1.20e-6, "steel": 7.9e-6}   # kg/mm3
EXTRUSION_KG_M = 0.5            # 20 x 20 mm aluminium extrusion, hollow profile
BRACKET_KG = 0.02               # 20-series inside corner bracket with its screws and T-nuts


def vol(*keys):
    return sum(COMP[k].shape.volume for k in keys)


def bar_len_m(key):
    """Total length of 20 x 20 extrusion in a component, from its solid volume (mm3 / 400 mm2)."""
    return COMP[key].shape.volume / 400.0 / 1000.0


EXTRUSION_M = {"frame": sum(bar_len_m(k) for k in ("rail_front", "rail_back", "end_l", "end_r", "cross_l", "cross_r")),
               "posts": bar_len_m("posts"), "top": bar_len_m("top_rails"), "water_post": bar_len_m("water_post")}
MASS = [
    ("1 Frame (%.2f m of 20 x 20 extrusion) and 8 brackets" % EXTRUSION_M["frame"], EXTRUSION_M["frame"] * EXTRUSION_KG_M + 8 * BRACKET_KG),
    ("1 Deck, 12 mm HDPE, notched (model volume)", vol("deck") * RHO["hdpe"]),
    ("1 Drip lip, 10 x 10 x 1.5 aluminium angle", vol("lip") * RHO["al"]),
    ("2 Back panel, 3 mm ACM at 3.8 kg/m2", 0.9 * 0.55 * 3.8),
    ("3 Posts and top frame (%.2f m of extrusion) and 14 brackets" % (EXTRUSION_M["posts"] + EXTRUSION_M["top"]),
     (EXTRUSION_M["posts"] + EXTRUSION_M["top"]) * EXTRUSION_KG_M + 14 * BRACKET_KG),
    ("3 Canopy 3 mm PC (model volume), duct collar and hanger", vol("canopy") * RHO["pc"] + 0.2 + vol("hanger") * RHO["al"]),
    ("4 Bench power supply (switch-mode, 300 W)", 3.0),
    ("5 Reservoir (filled) and deionizer", 0.8),
    ("5 Reservoir stand, water post and band clips", vol("res_stand") * RHO["al"] + EXTRUSION_M["water_post"] * EXTRUSION_KG_M + 0.03),
    ("6 Electrolyzer stack, 4 cells, titanium plates", 3.0),
    ("6 Electrolyzer feet", vol("ely_feet") * RHO["al"]),
    ("7 Separator and drier", 0.4),
    ("7 Column bracket and pipe clips", vol("col_bracket") * RHO["al"] + 0.03),
    ("8 Check valve and flame arrestor, saddle and clip", 0.3 + vol("arr_saddle") * RHO["hdpe"] + 0.01),
    ("9 Tank shell (aluminium, from the model) ", None),   # filled below
    ("9 Cradle, guard rods, nuts and top plate", vol("cradle") * RHO["hdpe"] + vol("guard_rods") * RHO["steel"] * 0.85
     + 16 * 0.011 + vol("guard_plate") * RHO["al"]),
    ("10 Manifold with high-pressure cut switch", 0.7),
    ("11 Regulator and solenoid", 0.6),
    ("12 Fuel cell (275 g listed) with controller", 0.4),
    ("12 Fuel cell bridge", vol("fc_bridge") * RHO["al"]),
    ("13 Load and lamp", 0.4),
    ("14 Meters, logger, display and cut relay", 0.35),
    ("15 H2Guard parts on the bench (sensor, fan, controller)", 1.5),
    ("16 and 17 Tubing (gas and water lines), wiring, fasteners, T-nuts", 1.5),
]
MASS_LIMIT = 25.0

BUDGET = 885.0                   # budget_usd in project.yaml: a value-engineering target, not a limit (Amish, 2026-10-01)

rows = []


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def n_mol(p_gauge_kpa, v_l, t=T0):
    """Moles of ideal gas at a gauge pressure (kPa), volume (L) and temperature (K)."""
    return (p_gauge_kpa + P_ATM) * v_l / (R * t)


def vstd(n):
    return n * VM


out = []


def say(s=""):
    out.append(s)
    print(s)


# ---------------------------------------------------------------- 2. Electrolyzer and fill
say("== 2. Electrolyzer and fill ==")
p_ely = N_ELY * V_CELL_ELY * I_ELY
v_stack = N_ELY * V_CELL_ELY
ndot_ely = N_ELY * I_ELY / (2 * F) * ETA_F
q_ely = ndot_ely * 60 * VM * 1000
dn_fill = n_mol(P_HIGH, V_TANK) - n_mol(P_LOW, V_TANK)
t_fill = dn_fill / ndot_ely
e_in = p_ely * t_fill / 3600
e_h2 = dn_fill * HHV / 3.6
eta_ely = e_h2 / e_in
eta_v = V_TN / V_CELL_ELY
comp_mv = R * T0 / (2 * F) * math.log((P_HIGH + P_ATM) / P_ATM) * 1000
v_aged = N_ELY * V_CELL_ELY_AGED
say(f"stack {v_stack:.1f} V x {I_ELY:.1f} A = {p_ely:.1f} W; aged {v_aged:.1f} V, {v_aged * I_ELY:.0f} W; supply {PSU_V:.0f} V {PSU_I:.0f} A")
say(f"H2 rate {ndot_ely * 1e4:.3f}e-4 mol/s = {q_ely:.0f} mL/min at 20 C")
say(f"fill {P_LOW:.0f} to {P_HIGH:.0f} kPa g in {V_TANK:.3f} L: {dn_fill:.4f} mol, {vstd(dn_fill):.2f} L, {t_fill:.0f} s = {t_fill / 60:.1f} min")
say(f"energy in {e_in:.2f} Wh, H2 (HHV) {e_h2:.2f} Wh, electrolyzer efficiency {eta_ely * 100:.1f} % (voltage {eta_v * 100:.1f} %, Faraday {ETA_F * 100:.0f} %)")
say(f"compression term {comp_mv:.1f} mV per cell at {P_HIGH:.0f} kPa g ({comp_mv / 1000 / V_CELL_ELY * 100:.2f} % of cell voltage)")
dp_membrane = P_RELIEF * (1 + RELIEF_ACCUM) + CRACK
dp_membrane_set = P_RELIEF + CRACK
say(f"membrane differential: normal {P_HIGH + CRACK:.0f}, supply cut {P_CUT + CRACK:.0f}, relief set {dp_membrane_set:.0f}, relief full lift {dp_membrane:.0f} kPa")
heat_ely = (e_in - e_h2) / (t_fill / 3600)
say(f"electrolyzer heat {heat_ely:.1f} W")
res("R3", f"{p_ely:.1f} W ({v_aged * I_ELY:.0f} W with aged cells)", "100 W or less", "Met")
res("R10", f"Stack H2 side must hold {P_HIGH + CRACK:.0f} kPa in filling, {P_CUT + CRACK:.0f} kPa at the supply cut and {dp_membrane_set:.0f} kPa at relief set; no rating in hand",
    f"{dp_membrane_set:.0f} kPa or more over the O2 side", "At risk")

# ---------------------------------------------------------------- 3. Inventory and pressure
say("\n== 3. Inventory and pressure ==")
n_work = n_mol(P_HIGH, V_TANK)
n_work_all = n_mol(P_HIGH, V_TANK + V_LINES)
n_relief = n_mol(P_RELIEF, V_TANK + V_LINES)
n_relief_cold = n_mol(P_RELIEF, V_TANK + V_LINES, T_COLD)
n_lift_cold = n_mol(P_RELIEF * (1 + RELIEF_ACCUM), V_TANK + V_LINES, T_COLD)
say(f"tank at {P_HIGH:.0f} kPa g: {n_work:.4f} mol, {vstd(n_work):.2f} L, {n_work * M_H2:.3f} g")
say(f"tank and lines at {P_HIGH:.0f} kPa g: {vstd(n_work_all):.2f} L")
say(f"tank and lines at relief set {P_RELIEF:.0f} kPa g: {vstd(n_relief):.2f} L; at 15 C {vstd(n_relief_cold):.2f} L")
say(f"tank and lines at full relief lift ({P_RELIEF * (1 + RELIEF_ACCUM):.0f} kPa g) and 15 C: {vstd(n_lift_cold):.2f} L")
say(f"compressibility correction at {P_HIGH:.0f} kPa g: {(Z_H2_400 - 1) * 100:.2f} % fewer moles than ideal")
r_in = P["tank_od"] / 2 - P["tank_wall"]
say(f"tank from model: inner radius {r_in:.0f} mm, straight length {tank_cyl_len():.1f} mm, volume {V_TANK:.3f} L")


def e_expand(p_g, v_l):
    p1 = (p_g + P_ATM) * 1000
    return p1 * v_l / 1000 / (GAMMA - 1) * (1 - (P_ATM * 1000 / p1) ** ((GAMMA - 1) / GAMMA))


e_p_work = e_expand(P_HIGH, V_TANK)
e_p_relief = e_expand(P_RELIEF, V_TANK)
say(f"stored pressure energy {e_p_work:.0f} J at {P_HIGH:.0f} kPa g, {e_p_relief:.0f} J at {P_RELIEF:.0f} kPa g")
say(f"stored chemical energy {n_work * HHV:.0f} kJ HHV, {n_work * LHV:.0f} kJ LHV at {P_HIGH:.0f} kPa g")
t_w = P["tank_wall"]
for p_mpa in (1.0, 4.0):
    sigma = p_mpa * (P["tank_od"] / 2 - t_w / 2) / t_w
    say(f"hoop stress at {p_mpa:.0f} MPa, {t_w:.0f} mm wall: {sigma:.1f} MPa (6061-T6 yield 276 MPa)")
guard_gap = P["guard_offset"] * math.sqrt(2) - P["guard_rod_d"] / 2 - P["tank_od"] / 2   # rods stand at the corners
say(f"guard clearance rod to shell {guard_gap:.0f} mm (rods at the corners of a {2 * P['guard_offset']:.0f} mm square)")
conc_room = vstd(n_relief) / (ROOM_M3 * 1000) * 100
conc_room_lift = vstd(n_lift_cold) / (ROOM_M3 * 1000) * 100
say(f"total release into {ROOM_M3:.0f} m3: {conc_room:.3f} % vol = {conc_room / LFL * 100:.2f} % LFL (full lift, 15 C: {conc_room_lift:.3f} %)")
n_max = 10.0 / VM
p_lift_max = n_max * R * T_COLD / ((V_TANK + V_LINES) / 1000) / 1000 - P_ATM
say(f"relief set for 10 L at full lift and 15 C: {p_lift_max / (1 + RELIEF_ACCUM):.0f} kPa g or less (full lift {p_lift_max:.0f} kPa g)")
say(f"H2Guard inventory rule (1 % of room at 1 atm): {ROOM_M3 * 10:.0f} L; H2Bench {vstd(n_lift_cold):.1f} L")
res("R5", f"{vstd(n_work_all):.1f} L at {P_HIGH:.0f} kPa g; {vstd(n_relief):.1f} L at relief set; {vstd(n_lift_cold):.1f} L at full relief lift and 15 C",
    "10 L or less", "Met" if vstd(n_lift_cold) <= 10.0 else "At risk")
res("R6", f"{P_HIGH:.0f} kPa g working, relief {P_RELIEF:.0f} kPa g; hoop stress {1.0 * (P['tank_od'] / 2 - t_w / 2) / t_w:.0f} MPa at 1 MPa",
    "300 / 350 kPa g or less; vessel 1 MPa or more", "Met")
res("R7", f"{conc_room:.3f} % vol ({conc_room / LFL * 100:.1f} % LFL); {conc_room_lift:.3f} % worst case", "Below 25 % LFL in 30 m3", "Met")

# ---------------------------------------------------------------- 4. Fuel cell and discharge
say("\n== 4. Fuel cell and discharge ==")
p_fc_gross = N_FC * V_CELL_FC * I_FC
p_fc_net = p_fc_gross - P_AUX
ndot_fc_react = N_FC * I_FC / (2 * F)
ndot_fc = ndot_fc_react / UTIL
q_fc = ndot_fc * 60 * VM * 1000
n_avail = dn_fill * (1 - STORAGE_LOSS)
t_dis = n_avail / ndot_fc
e_out = p_fc_net * t_dis / 3600
e_store_loss = dn_fill * STORAGE_LOSS * HHV / 3.6
e_h2_avail = n_avail * HHV / 3.6
eta_fc_hhv = e_out / e_h2_avail
eta_fc_lhv = e_out / (n_avail * LHV / 3.6)
say(f"gross {p_fc_gross:.1f} W, net {p_fc_net:.1f} W; reacted {ndot_fc_react * 60 * VM * 1000:.0f} mL/min, supplied {q_fc:.0f} mL/min (listed max {FC_LISTED_FLOW * 1000:.0f})")
say(f"available {n_avail:.4f} mol; discharge {t_dis:.0f} s = {t_dis / 60:.1f} min; output {e_out:.2f} Wh")
say(f"fuel cell efficiency net {eta_fc_hhv * 100:.1f} % HHV, {eta_fc_lhv * 100:.1f} % LHV (listing: 40 % system at full load)")
fc_heat = (e_h2_avail - e_out) / (t_dis / 3600) - P_AUX
say(f"fuel cell heat and purge {fc_heat:.1f} W")
for v in (0.58, 0.55):
    say(f"net power at {v:.2f} V per cell: {N_FC * v * I_FC - P_AUX:.1f} W")
cycle = (t_fill + t_dis) / 60
say(f"cycle run time {cycle:.1f} min")
res("R4", f"{p_fc_net:.1f} W net ({p_fc_gross:.1f} W gross); 9.8 W if cells fall to 0.55 V", "10 to 50 W", "Met")
res("R2", f"{t_fill / 60:.1f} min fill + {t_dis / 60:.1f} min discharge = {cycle:.1f} min", "60 min or less", "Met")

# ---------------------------------------------------------------- 5. Energy balance
say("\n== 5. Energy balance ==")
rt = e_out / e_in
say(f"in {e_in:.1f} Wh -> H2 {e_h2:.1f} Wh -> after storage {e_h2_avail:.1f} Wh -> out {e_out:.1f} Wh")
say(f"losses: electrolyzer {e_in - e_h2:.1f} Wh, storage {e_store_loss:.1f} Wh, fuel cell {e_h2_avail - e_out:.1f} Wh")
say(f"round trip {rt * 100:.1f} % (HHV basis)")
say(f"oxygen vented {vstd(dn_fill / 2):.2f} L per fill")

# ---------------------------------------------------------------- 6. Measurement uncertainty
say("\n== 6. Measurement uncertainty (R1) ==")
dp = PT_ACC * PT_FS
n1, n2 = n_mol(P_LOW, V_TANK), n_mol(P_HIGH, V_TANK)
u_p = math.sqrt(2) * dp * V_TANK / (R * T0)
u_t = math.hypot(n2 * DT_THERM / T0, n1 * DT_THERM / T0)
u_v = dn_fill * DV_TANK
u_n = math.sqrt(u_p ** 2 + u_t ** 2 + u_v ** 2)
rel_n = u_n / dn_fill
say(f"pressure {dp:.1f} kPa per reading -> {u_p / dn_fill * 100:.2f} %; temperature -> {u_t / dn_fill * 100:.2f} %; volume -> {DV_TANK * 100:.1f} %")
say(f"hydrogen made per fill {rel_n * 100:.2f} % (k = 1 combined)")
# gas-to-wall lag during filling: flow work into the tank, natural convection inside
h_in, a_in = 5.0, (2 * math.pi * r_in * tank_cyl_len() + 3 * math.pi * r_in ** 2) / 1e6
q_flow_work = ndot_ely * R * T0
dt_gas = q_flow_work / (h_in * a_in)
tau = n2 * 20.8 / (h_in * a_in)
say(f"gas above wall during fill {dt_gas:.2f} K; time constant {tau:.0f} s; read 2 min after the fill ends")
rel_power = DP_POWER
u_ely = math.hypot(rel_n, rel_power)
u_storage = math.hypot(u_p, u_t * 0.5) / dn_fill      # hold test at nearly the same state
u_fc = math.hypot(rel_n, rel_power)
u_rt = math.hypot(rel_power, rel_power)
u_fe = math.hypot(rel_n, rel_power)
say(f"electrolyzer {u_ely * 100:.1f} %, storage {u_storage * 100:.1f} %, fuel cell {u_fc * 100:.1f} %, round trip {u_rt * 100:.1f} %, Faraday {u_fe * 100:.1f} %")
worst = max(u_ely, u_storage, u_fc, u_rt)
res("R1", f"Worst stage {worst * 100:.1f} % (hydrogen per fill {rel_n * 100:.1f} %, power {rel_power * 100:.0f} %)", "Each within 5 % relative", "Met")

# ---------------------------------------------------------------- 7. Hood, venting and interlock
say("\n== 7. Hood, venting and interlock ==")
q_hood_lpm = Q_HOOD * 1000 / 60
a_duct = math.pi * (P["duct_d"] / 2000) ** 2
v_duct = Q_HOOD / 3600 / a_duct
say(f"hood extraction {Q_HOOD:.0f} m3/h = {q_hood_lpm:.0f} L/min; duct velocity {v_duct:.2f} m/s")
leak_ely = q_ely / 1000
say(f"electrolyzer full output into the hood: {leak_ely / q_hood_lpm * 100:.3f} % vol at the duct")
say(f"leak needed to reach the H2Guard warning at the duct: {H2G_WARN / 100 * q_hood_lpm:.1f} L/min; trip {H2G_TRIP / 100 * q_hood_lpm:.1f} L/min")

# Blowdown of tank and lines through the vent needle valve (isothermal, orifice flow)
V_VENT = V_TANK + V_LINES


def mdot(cda, p0):
    """Mass flow (kg/s) through an orifice with effective area cda (m2), upstream p0 (Pa abs)."""
    pd = P_ATM * 1000
    rho0 = p0 * M_H2 / 1000 / (R * T0)
    crit = (2 / (GAMMA + 1)) ** (GAMMA / (GAMMA - 1))
    if pd / p0 <= crit:
        return cda * p0 * math.sqrt(GAMMA * M_H2 / 1000 / (R * T0)) * (2 / (GAMMA + 1)) ** ((GAMMA + 1) / (2 * (GAMMA - 1)))
    r_ = pd / p0
    return cda * math.sqrt(2 * rho0 * p0 * GAMMA / (GAMMA - 1) * (r_ ** (2 / GAMMA) - r_ ** ((GAMMA + 1) / GAMMA)))


def blowdown(cda, p_start, p_end, dt=0.05):
    p = (p_start + P_ATM) * 1000
    t, peak = 0.0, 0.0
    while p > (p_end + P_ATM) * 1000:
        m = mdot(cda, p)
        peak = max(peak, m)
        p -= m / (M_H2 / 1000) * R * T0 / (V_VENT / 1000) * dt
        t += dt
    return t, peak


lo, hi = 1e-10, 1e-6
for _ in range(60):
    mid = math.sqrt(lo * hi)
    t, _ = blowdown(mid, P_HIGH, P_KEEP, 0.1)
    lo, hi = (lo, mid) if t < T_VENT_SET else (mid, hi)
cda = math.sqrt(lo * hi)
t_vent, peak = blowdown(cda, P_HIGH, P_KEEP)
peak_lpm = peak / (M_H2 / 1000) * VM * 60
n_vent = n_mol(P_HIGH, V_VENT) - n_mol(P_KEEP, V_VENT)
d_eq = math.sqrt(4 * cda / math.pi) * 1000
say(f"vent {P_HIGH:.0f} to {P_KEEP:.0f} kPa g: {vstd(n_vent):.2f} L in {t_vent:.0f} s; effective orifice {d_eq:.2f} mm diameter (Cd A {cda * 1e6:.4f} mm2)")
say(f"peak vent flow {peak_lpm:.2f} L/min, peak at the duct {peak_lpm / (q_hood_lpm + peak_lpm) * 100:.2f} % vol ({peak_lpm / (q_hood_lpm + peak_lpm) * 100 / LFL * 100:.1f} % LFL)")
t_min_warn = vstd(n_vent) / (H2G_WARN / 100 * q_hood_lpm)
say(f"shortest vent (at constant flow) that stays under the H2Guard warning: {t_min_warn * 60:.0f} s")
n_eod = n_mol(P_LOW, V_VENT) - n_mol(P_KEEP, V_VENT)
say(f"end-of-day vent after a discharge ({P_LOW:.0f} to {P_KEEP:.0f} kPa g): {vstd(n_eod):.2f} L")
t_interlock = T_RELAY + T_VALVE
say(f"interlock alarm to solenoid closed and supply off: {t_interlock:.1f} s (H2Guard R4 allows 2 s)")
say(f"hydrogen made during that time: {ndot_ely * t_interlock * VM * 1000:.1f} mL")
res("R8", f"{t_interlock:.1f} s from trip to valve closed, from H2Guard TRL 2 figures; H2Guard valve is 24 V, H2Bench solenoid 12 V",
    "Trip cuts supply and closes solenoid within 2 s; fan runs", "At risk")
res("R16", f"Vent {t_vent / 60:.1f} min at the needle valve setting; setup time needs a walk-through with hardware",
    "Setup 15 min or less; safe in 5 min or less", "Not verifiable at TRL 3")
res("R15", f"Guard clearance {guard_gap:.0f} mm; relief and vent piped to the canopy in the model", "Guard, piped relief, no tool-free fitting", "Met")

# ---------------------------------------------------------------- 8. Water, drier and purity
say("\n== 8. Water, drier and purity ==")
water_g = dn_fill * 18.015
say(f"water split per fill {water_g:.2f} g; oxygen {dn_fill / 2:.4f} mol")
y_lo = P_SAT_SEP / (P_LOW + P_ATM)
y_hi = P_SAT_SEP / (P_HIGH + P_ATM)
y_avg = (y_lo + y_hi) / 2
vap_g = dn_fill * y_avg / (1 - y_avg) * 18.015
fills = GEL_G * GEL_CAP / vap_g
say(f"water vapour after the separator at 25 C: {y_hi * 100:.2f} to {y_lo * 100:.2f} % mol; {vap_g:.3f} g per fill")
say(f"drier: {GEL_G:.0f} g silica gel at {GEL_CAP * 100:.0f} % uptake lasts {fills:.0f} fills")
res("R9", "Water removed by the drier; oxygen crossover in the stack not known; no deoxidizer", "99.995 % or better (fuel cell listing)", "Not met")
res("R11", "Mixed-bed resin with conductivity check to 1 uS/cm; water use 3.4 g per fill", "1 uS/cm or less at the stack inlet", "Met")

# ---------------------------------------------------------------- 9. Envelope and mass
say("\n== 9. Envelope and mass ==")
l, d, h = envelope()
tank_shell_area = (2 * math.pi * P["tank_od"] / 2 * (tank_cyl_len() + t_w) + 2 * math.pi * (P["tank_od"] / 2) ** 2
                   + math.pi * (P["tank_od"] / 2) ** 2)
tank_shell_kg = tank_shell_area * t_w * 2.7e-6
mass = [(n, tank_shell_kg if m is None else m) for n, m in MASS]
m_total = sum(m for _, m in mass)
m_no_psu = m_total - 3.0
for n, m in mass:
    say(f"  {n.strip()}: {m:.2f} kg")
say(f"a 10 mm deck instead of 12 mm saves {0.9 * 0.45 * 0.002 * 950:.2f} kg")
say(f"envelope {l:.0f} x {d:.0f} x {h:.0f} mm; mass {m_total:.1f} kg ({m_no_psu:.1f} kg without the supply)")
res("R13", f"{l:.0f} x {d:.0f} mm, {h:.0f} mm tall; {m_total:.1f} kg with the supply ({m_no_psu:.1f} kg without)",
    "1000 x 500 mm, 800 mm, 25 kg or less", "At risk" if m_total > MASS_LIMIT else "Met")

# ---------------------------------------------------------------- 10. Cost
say("\n== 10. Cost ==")
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
cost = {r["item"].split()[0]: float(r["unit_cost_usd"]) * float(r["qty"]) for r in bom}
total = sum(cost.values())
no_psu = total - cost["4"]
minimum = no_psu - cost["18"]
say(f"BOM lines {len(bom)}; total ${total:.0f}; without the bench supply ${no_psu:.0f}; without supply and RCD ${minimum:.0f}")
def vs_target(c):
    return "on the target" if abs(c - BUDGET) < 0.5 else f"{'over' if c > BUDGET else 'under'} the target by ${abs(c - BUDGET):.0f}"


say(f"value-engineering target ${BUDGET:.0f} (budget_usd); full kit {vs_target(total)}; without supply {vs_target(no_psu)}; minimum kit {vs_target(minimum)}")
say(f"lines repriced for construction (HBN-DDR-003): 1, 3, 5, 6, 7, 8, 9, 12, 16, 17")
say(f"two stacks ${cost['6'] + cost['12']:.0f} ({(cost['6'] + cost['12']) / total * 100:.0f} % of total)")
res("R14", f"${total:.0f} full; ${no_psu:.0f} without supply; ${minimum:.0f} minimum (H2Guard excluded)",
    f"${BUDGET:.0f} value-engineering target (budget_usd, supply included)",
    "On the value-engineering target" if abs(total - BUDGET) < 0.5 else
    f"{'Over' if total > BUDGET else 'Under'} the value-engineering target by ${abs(total - BUDGET):.0f}")

# ---------------------------------------------------------------- 11. Logging
say("\n== 11. Logging ==")
n_rows = int(round(t_fill + t_dis))
chan = 10
size_kb = n_rows * chan * 8 / 1000
say(f"{n_rows} rows at 1 Hz per cycle, {chan} channels, about {size_kb:.0f} kB CSV")
res("R12", f"{n_rows} rows per cycle, about {size_kb:.0f} kB", "V, I, P, p, T at 1 Hz to CSV", "Met")

# ---------------------------------------------------------------- Results
order = [f"R{i}" for i in range(1, 17)]
rows.sort(key=lambda r: order.index(r[0]))
say("\n== Results ==")
for r in rows:
    say(" | ".join(r))
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
assert len(rows) == 16, "every requirement needs a row"
print("\nwrote docs/04-calcs/results.csv")
