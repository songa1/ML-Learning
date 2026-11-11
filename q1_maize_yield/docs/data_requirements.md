# Data Requirements (Q1)

**BUILT ON STAND-IN DATA, RE-RUN ON REAL FILE**

- Target: `yield_kg_per_ha`
- Area: 4 provinces, 14+ districts, 20 cooperatives
- Period: 2023-2025
- Required uses: Questions A-E from stakeholder brief

## Requirement-vs-file check

| Business question | Needed columns | Meets now? | Gaps |
|---|---|---|---|
| A Expected yield | yield_kg_per_ha, farm_size, harvest_weight_kg | Yes | Requires cleaning consistency checks |
| B Fertilizer + seed effect | fertilizer_kg, farm_size, seed_variety | Yes | Must normalize fertilizer per ha |
| C Weather + altitude + irrigation | rainfall_mm, avg_temp_c, altitude_m, irrigation | Yes | Requires realism validation |
| D Location + season differences | province, district, season, planting_date | Yes | Requires label/date harmonization |
| E Low harvest risk (pre-harvest) | pre-harvest fields only | Partial | Must remove leakage columns |
