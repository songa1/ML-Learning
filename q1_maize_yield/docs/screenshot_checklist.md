# Screenshot Checklist (take manually)

- Stage 1 (`00_environment_test.ipynb`): versions output cell.
- Stage 2 (`01_acquire.ipynb`): file detection + shape output, data dictionary preview.
- Stage 3 (`02_eda.ipynb`): data quality report table output and at least 5 figure outputs (include notebook title cell).
- Stage 4 (`03_clean.ipynb`): split shapes, overlap check, low-yield threshold, cleaning log sample.
- Stage 5 (`04_features.ipynb`): feature counts, MI table, RF importance table.
- Stage 6 (`05_finalise.ipynb`): confirmation of generated docs and helper function.

Suggested caption format: "Stage X output showing [what], confirming [decision]."
Suggested explanation: 1-3 sentences on why the output matters for data readiness and leakage prevention.
