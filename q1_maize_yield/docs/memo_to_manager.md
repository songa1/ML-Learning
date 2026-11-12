# Memo to Manager

## Dataset

- Source: `q1_maize_yield/data/raw/maize_yield_rwanda_rw.csv`
- Records: 1,426 farm records, 20 source columns
- Target: `yield_t_ha`, converted to `yield_kg_per_ha` for modelling
- Scope: dataset preparation and cooperative questions A-E. This repository does not train a production model.

## Problems found and how they were solved

| Problem | Evidence | Solution |
| --- | --- | --- |
| Missing values | 11 rainfall, 14 soil pH, 14 pest-index values (39 total) | Parsed to `NaN`; imputed with training-only median/most-frequent values in the preprocessor |
| Extreme / invalid values | Fertilizer, rainfall and yield had entry-error extremes | Agronomic plausibility rules set invalid values to `NaN`; winsorized fertilizer (30), rainfall (26) and yield (30) at the 1st/99th percentiles |
| Duplicate / repeated records | Checked exact duplicates and repeated `record_id` | Remove exact duplicates; keep the most complete record for repeated IDs |
| Inconsistent labels and casing | Season, irrigation, soil type, practice, district/province labels | `standardize_text` canonicalizes labels and maps each district to one province |
| Unit / schema mismatch | Yield in t/ha; fertilizer split across NPK, urea, manure | Derived `yield_kg_per_ha`, `fertilizer_kg`, `farm_size_ha`, and an ordinal pest-incidence band |
| Target leakage | `yield_t_ha` is the target; `low_yield_risk` was derived from it | Both are excluded from model inputs; the risk label is created only after the train split |
| Seed-flag encoding bug | `is_improved_seed` was derived from farming practice, not seed variety | Rebuilt from `seed_variety != "Local"`; removed redundant `seed_rank` |
| Fair fertiliser comparison | Total fertiliser would favour larger farms | Compared as kg/ha; fertiliser rate is not correlated with farm size (about -0.02) |
| Missing planting dates | Source has seasons A/B/C only | Documented as a limitation; season-level analysis only |
| Irrigation imbalance | 128 irrigated vs 1,298 non-irrigated farms | Recorded as a feature; irrigation comparisons are interpreted cautiously |
| Audit bug | Data-quality report showed 0 missing values because empty strings were not counted | Fixed the audit to parse columns first; it now reports 39 missing values |

## Where to find the cleaned data

- Interim cleaned data: `q1_maize_yield/data/interim/maize_clean.csv`
- Cleaned unscaled splits: `q1_maize_yield/data/processed/train_clean_unscaled.csv`, `validation_clean_unscaled.csv`, `test_clean_unscaled.csv`
- Model-ready splits: `q1_maize_yield/data/processed/train_model_ready.csv`, `validation_model_ready.csv`, `test_model_ready.csv`
- Fitted preprocessing pipeline: `q1_maize_yield/data/processed/preprocessor.joblib`
- Selected features: `q1_maize_yield/data/processed/selected_features.txt`
- Hash manifest: `q1_maize_yield/data/processed/hash_manifest.txt`
- Cooperative answers: `q1_maize_yield/docs/cooperative_answers.md` and `.csv`
- Charts: `q1_maize_yield/figures/`

## Cooperative questions A-E

- **A.** Mean 2.57 t/ha, median 2.58 t/ha; central 80% 1.68-3.48 t/ha; season A 2.86, B 2.51, C 2.00 t/ha.
- **B.** Hybrid seed +0.96 t/ha (+53%); improved practice +0.37 t/ha (+16%); high vs low fertiliser +0.22 t/ha (+9%).
- **C.** Rainfall +0.35; temperature -0.02; altitude +0.05; irrigation 2.53 vs 2.58 t/ha.
- **D.** Season matters more than province; province means 2.47-2.65 t/ha; districts 2.34-2.83 t/ha; labels consistent; no planting dates.
- **E.** Threshold 1.95 t/ha; 19.8% at risk; season C 44.7%; local seed 64.4% vs hybrid 8.9%.

## Limitations

- Observational data, not a controlled experiment.
- No planting-date column, so planting-date effects cannot be evaluated.
- Irrigation is rare and non-random.
- No production model is trained in this repository.