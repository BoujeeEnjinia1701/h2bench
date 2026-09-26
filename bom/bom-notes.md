# BOM notes

- Rows 1 to 15 are numbered to match the callouts in `media/exploded.png`. Rows 16 to 18 are not numbered in the exploded view; the gas lines of row 16 are modelled as 6 mm tubes.
- Every line is priced. All prices are indicative USD figures for a single prototype in 2026, not quotes. Items 6, 9 and 12 are estimates for generic parts and carry the largest uncertainty. The branded 12 W fuel cell list price ($576) and the MSE 300 mL/min single-cell stack price ($1,396.95) were checked on 2026-09-25.
- Totals (checked by `docs/04-calcs/sizing.py`, HBN-CAL-001 section 10): **$865** for all 18 lines; $800 if the school supplies the bench power supply (line 4); $780 if the bench socket is also already RCD protected (line 18).
- Against the $450 `budget_usd` in `project.yaml` the kit is over in every case. Against the about $850 recommended at TRL 2 (awaiting Amish, HBN-DDR-001 item 9) the full kit is $15 over and the kit without the supply is $50 under. `budget_usd` is unchanged.
- The H2Guard detector, fan and interlock (line 15) is costed in the H2Guard project and is **not** included in the total. The bench must not run without it.
- Line 10's vent valve is a needle valve set so that venting 300 to 20 kPa gauge takes 3 min or more (HBN-CAL-001 section 7).
- Line 18 (plug-in 30 mA RCD) was added at TRL 3 because the safety sections require RCD protection and no line covered it.
- The existing lab table shown in the renders is not part of the BOM.
