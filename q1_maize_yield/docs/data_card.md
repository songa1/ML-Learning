# Data Card (Q1 Maize)

- Purpose: prepare a machine-learning-ready maize dataset for questions A-E.
- Source: MCSU merged district forms (or stand-in when source unavailable).
- Size (usable): 1192 rows across train/validation/test.
- Target: `yield_kg_per_ha`.
- Key cleaning: text normalization, unit conversion to hectares, date parsing, deduplication, impossible value handling, leakage control.
- Key features: fertilizer per hectare, planting timing, seed and irrigation indicators, climate interactions.
- Limitations: data-entry noise, potential district/cooperative reporting bias, stand-in usage if real file missing.
- Reproducibility: `python run_all.py`.
