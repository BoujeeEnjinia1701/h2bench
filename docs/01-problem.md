---
doc_id: HBN-PRB-001
title: H2Bench problem statement
project: H2Bench
doc_type: Problem statement
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; record the first-user and storage choices adopted for TRL 3 (HBN-DDR-001), cost and inventory figures from HBN-CAL-001, MSE listing checked
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($885)
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget restated as a value-engineering target; cost of the constructable design (HBN-DDR-003)
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Curriculum and first use decided (HBN-DEC-001, 2026-10-02)"
---

# H2Bench problem statement

Students hear about the hydrogen economy but rarely measure it. Teaching kits are either toys that run a fan for a few minutes or lab systems priced for universities, and neither lets a class follow one quantity of energy from the wall socket, through hydrogen, and back to electricity while measuring every loss on the way.

## The problem

Governments and industry are committing large sums to hydrogen. The European Union aims to produce 10 Mt of renewable hydrogen a year by 2030 and import another 10 Mt ([European Commission](https://energy.ec.europa.eu/topics/eus-energy-system/hydrogen_en)); India targets 5 Mt a year under its National Green Hydrogen Mission ([PIB, Government of India](https://www.pib.gov.in/PressNoteDetails.aspx?id=155990&NoteId=155990&ModuleId=3)). Yet global demand was almost 100 Mt in 2024 and low-emissions hydrogen was still less than 1 % of production ([IEA, Global Hydrogen Review 2025](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)). Engineers, technicians and policy makers will be asked to judge where hydrogen makes sense, and the core fact they need is quantitative: turning electricity into hydrogen and back loses most of the energy. A 2025 review puts the round trip with fuel cells at 27.4 to 48 % ([Oxford Institute for Energy Studies, 2025](https://www.oxfordenergy.org/wpcms/wp-content/uploads/2025/07/ET48-Power-to-Hydrogen-to-Power.pdf)).

Schools and colleges struggle to teach this by measurement:

1. **Toy kits hide the numbers.** Sub-watt reversible cells (from about $60 to $70, [Horizon Educational](https://www.horizoneducational.com/8-types-of-fuel-cell-by-price-point/t1418?currency=usd)) show that the reaction works, but at milliwatt scale the losses in meters, leaks and wiring swamp the result, and nothing is measured by default.
2. **Real components are costly.** A branded 12 W fuel cell stack lists at $482 to $576 ([Fuel Cell Store](https://www.fuelcellstore.com/horizon-12-watt-pem-fuel-cell), [Fuel Cell Shop](https://www.fuelcellshop.com/7-types-of-small-fuel-cell-by-price-point/t1363?currency=usd)) and a 300 mL/min PEM electrolyzer stack near $1,400 ([MSE Supplies](https://www.msesupplies.com/products/mse-pro-ma-300-pem-water-electrolyzer-stack-max-flow-rate-300-ml-min)), before any storage, safety or instrumentation.
3. **Safety is the gatekeeper.** Hydrogen burns in air from about 4 to 74 % by volume and ignites with about 0.02 mJ ([US DOE](https://www1.eere.energy.gov/hydrogenandfuelcells/pdfs/h2_safety_fsheet.pdf)). Many schools will not host a hydrogen rig without detection, ventilation and a limit on how much gas is present.

H2Bench is an open teaching bench at a scale large enough to measure (tens of watts) and small enough to be safe in a classroom (under 10 L of hydrogen, low pressure, interlocked by the portfolio's H2Guard detector).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Vocational hydrogen technician trainees (first users; decided by Amish, 2026-09-25, HBN-DDR-002) | Safe-handling practice on real hardware and measured efficiencies | Supervised courses with trained instructors |
| Secondary and vocational students (about 15 to 19 years) | See and measure each energy conversion; calculate efficiencies from their own data | 60 to 90 min practical sessions, groups of 3 to 5, supervised |
| University engineering students | Polarization curves, Faraday efficiency, gas law measurements, uncertainty analysis | Teaching lab, longer sessions, spreadsheet or notebook analysis |
| Technical and vocational trainers | A rig that trains safe habits: purge, leak check, interlock test, lockout | Hydrogen technician courses in countries building hydrogen industries |
| Teachers and lab technicians | Set up in under 15 min, run without specialist support, store safely between lessons | Existing lab benches, shared rooms, limited budgets |
| School safety officers | Evidence that the gas inventory, pressure and ventilation are bounded | Risk assessment before first use |

### Operating environment

- **Room:** a school or college lab of about 30 to 150 m³ with mechanical or window ventilation, mains power and an existing bench about 750 mm high.
- **Ambient:** 15 to 30 °C, indoor humidity; the fuel cell class chosen is specified for 5 to 30 °C ambient ([Fuel Cell Store](https://www.fuelcellstore.com/horizon-12-watt-pem-fuel-cell)).
- **Water:** deionized or distilled water is needed; PEM stacks are damaged by other water ([MSE Supplies](https://www.msesupplies.com/products/mse-pro-ma-300-pem-water-electrolyzer-stack-max-flow-rate-300-ml-min)).
- **Use pattern:** one fill and one discharge per lesson, a few lessons a week, tank vented down to about 20 kPa gauge (never to atmospheric, so no air enters) at the end of each day, through a needle valve over 3 min or more (HBN-CAL-001).

## Constraints

- Garage-buildable prototype: hand tools only, no welding. Value-engineering target: USD 885 (`budget_usd`; raised from $450 to $850 on 2026-09-25 and to $885 on 2026-09-26, HBN-DDR-002; a hypothetical control target, not a limit), with the bench power supply in the kit and H2Guard costed in its own project. Estimated cost of the constructable design: USD 999 (USD 114 over the target), or USD 934 without the bench supply (HBN-CAL-001 v0.4).
- Hydrogen inventory under 10 L at 20 °C and 101.3 kPa, stored at 300 kPa gauge or less in a rigid tank, with a 310 kPa gauge supply cut and a 325 kPa gauge relief (decided, HBN-DDR-002). No compression beyond what the electrolyzer does itself.
- Electrolyzer under 100 W and fuel cell under 50 W, as the pitch states.
- Operates only when the H2Guard detector, extraction fan and interlock are active.
- Off-the-shelf gas components; no welding or pressure-vessel fabrication.
- Fits on a standard lab bench; carried by two people.
- Open design files (CERN-OHL-S-2.0) and open worksheets so teachers can adapt the lessons.

## Out of scope

- Hydrogen for heating, cooking or vehicles, and any storage above 1 MPa.
- Alkaline electrolysis with caustic electrolyte (excluded for student safety).
- Metal hydride storage in the first version (kept as an option, see HBN-PRC-001).
- Designing the hydrogen detector and interlock itself (that is H2Guard).
- Certification as laboratory equipment; this is a research and teaching prototype.

## Prior work

- **Educational fuel cell kits.** Horizon Educational and similar suppliers sell kits from sub-watt reversible cells to 12 to 30 W stacks ([Horizon Educational](https://www.horizoneducational.com/8-types-of-fuel-cell-by-price-point/t1418?currency=usd)). They prove the components work in schools; the larger stacks set the cost floor.
- **Laboratory PEM electrolyzers.** Small stacks such as MSE's 300 mL/min single-cell unit (56 cm², 45 A at about 2.3 V, 2.5 kg, $1,396.95) show the output class needed ([MSE Supplies](https://www.msesupplies.com/products/mse-pro-ma-300-pem-water-electrolyzer-stack-max-flow-rate-300-ml-min), checked 2026-09-25). That listing does not state an output pressure, so whether a stack can fill a low-pressure tank directly must be confirmed per stack (HBN-REQ-001 R10).
- **Hydrogen education programs.** The US DOE Hydrogen Program names teachers and students among its target audiences and notes "a general lack of awareness of hydrogen as an energy alternative" ([US DOE Hydrogen Program](https://www.hydrogen.energy.gov/program-areas/education)). EPRI's H2EDGE program develops hydrogen training for the workforce ([EPRI](https://hydrogen.epri.com/en/h2edge.html)).
- **Round-trip analysis.** Published studies of power-to-hydrogen-to-power give the efficiency range that students should be able to reproduce at small scale ([Oxford Institute for Energy Studies, 2025](https://www.oxfordenergy.org/wpcms/wp-content/uploads/2025/07/ET48-Power-to-Hydrogen-to-Power.pdf)).
- **H2Guard (this portfolio).** The hydrogen leak detector and ventilation interlock that H2Bench depends on. H2Bench adds no detection of its own.

## Open questions

- Which curricula to align with first? Decided by Amish, 2026-10-02 (HBN-DEC-001): post-16 vocational learners on hydrogen or renewable energy technician courses, aligned to the electrochemistry, gas safety and efficiency units of the first partner college's course.
- Will school safety officers accept a 300 kPa gauge buffer tank, or is a near-atmospheric gasbag with a small pump easier to approve?
- Is a class demonstration (teacher-run) or a group practical (student-run) the first use case? Decided by Amish, 2026-10-02 (HBN-DEC-001): an instructor-run class demonstration first; group practicals only after a recorded run of attended fills with H2Guard tested before each.
