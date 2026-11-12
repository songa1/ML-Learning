# Q1 Data Card

- Target: `yield_kg_per_ha` (derived from source `yield_t_ha` by multiplying by 1,000).
- Records: train=998, validation=214, test=214.
- Revised source fields: record ID, year, season, geography, weather, soil, seed, farming practice, fertiliser, density, area, irrigation and pest index.
- Leakage control: `yield_t_ha` is excluded from model features; no harvest-weight field is present in the revised source.
- Prepared: 2026-11-12.
- Limitation: this is a prepared dataset, not a trained or deployed prediction model.
