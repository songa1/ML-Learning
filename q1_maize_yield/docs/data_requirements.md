# Q1 Data Requirements

- Target: `yield_t_ha`, converted to `yield_kg_per_ha` for modelling.
- Pre-harvest predictors: weather, altitude, soil, seed, farming practice, fertiliser, density, area, irrigation and pest index.
- The revised file has no harvest-weight column; therefore no post-harvest harvest measure is used as a feature.
- The derived `low_yield_risk` label is created after the train split and excluded from model inputs.
- The source contains 1,426 records and 20 columns, with missing rainfall, soil pH and pest-index values handled during preprocessing.
