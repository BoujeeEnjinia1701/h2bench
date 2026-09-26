# BOM notes

- Rows 1 to 15 are numbered to match the callouts in `media/exploded.png`. Rows 16 to 18 are not numbered in the exploded view; the gas lines of row 16 are modelled as 6 mm tubes.
- Every line is priced. All prices are indicative USD figures for a single prototype in 2026, not quotes. Items 6, 9 and 12 are estimates for generic parts and carry the largest uncertainty. The branded 12 W fuel cell list price ($576) and the MSE 300 mL/min single-cell stack price ($1,396.95) were checked on 2026-09-25.
- Totals (checked by `docs/04-calcs/sizing.py`, HBN-CAL-001 v0.3 section 10): **$885** for all 18 lines; $820 if the school supplies the bench power supply (line 4); $800 if the bench socket is also already RCD protected (line 18).
- `budget_usd` is $885 (raised from $450 to $850 by Amish's decision of 2026-09-25, and to $885 on 2026-09-26 to cover the priced BOM, HBN-DDR-002), with the bench supply in the kit. The full kit meets it with no margin; without the supply it is $65 under.
- The H2Guard detector, fan and interlock (line 15) is costed in the H2Guard project and is **not** included in the total. The bench must not run without it.
- Line 10's vent valve is a needle valve set so that venting 300 to 20 kPa gauge takes 3 min or more (HBN-CAL-001 section 7). Its relief valve is set to 325 kPa gauge, and it carries a pressure switch that opens at 310 kPa gauge; the switch drives the relay in line 14, which breaks the electrolyzer supply (HBN-DDR-002). These added $20 to lines 10 and 14.
- Line 18 (plug-in 30 mA RCD) was added at TRL 3 because the safety sections require RCD protection and no line covered it.
- The existing lab table shown in the renders is not part of the BOM.
