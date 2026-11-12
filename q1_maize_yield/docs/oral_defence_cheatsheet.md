# Q1 Oral Defence Cheatsheet

- **Why convert `yield_t_ha` to `yield_kg_per_ha`?** The source target is in tonnes per hectare; converting to kg/ha gives a clear, consistent modelling unit.
- **Why combine NPK, urea and manure?** They are separate source fertiliser measures. NPK and urea are converted as kg/ha, while manure tonnes/ha are multiplied by 1,000 before combining.
- **Why split before imputation and scaling?** To prevent validation and test information from influencing training preprocessing.
- **Why median imputation?** Numeric fields can be skewed, so the median is less sensitive to extreme values than the mean.
- **Why one-hot encode categories?** Province, district, soil type, seed variety and practice are nominal categories without a natural numeric order.
- **Why ordinal-encode pest incidence?** The derived `Low`, `Medium`, `High` groups have an explicit order.
- **Why exclude `yield_t_ha` from features?** It is the source form of the target and would cause target leakage.
- **Why retain `record_id` only for integrity?** It identifies observations and checks split disjointness but is not used as a model feature.
- **What is the project result?** A reproducible model-ready dataset and preprocessing pipeline, not a trained production prediction model.
