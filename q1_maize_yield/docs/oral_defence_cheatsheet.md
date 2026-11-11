# Oral Defence Cheatsheet

- Why split before scaling/imputation? To avoid test leakage and preserve unbiased validation.
- Why train-only fitting? Model preprocessing must reflect only information available at training time.
- Why median imputation? Numeric fields were skewed and had outliers.
- Why one-hot vs ordinal? Ordinal used only for pest levels (Low<Medium<High); nominal categories one-hot encoded.
- Why remove harvest_weight from features? It is post-harvest and leaks outcome information.
- Why use fertilizer per hectare? Fertilizer totals are not comparable across different farm sizes.
- Why stratify by season? Preserves seasonal distribution across train/val/test.
- Why cap outliers? Limits data-entry error influence while retaining plausible extremes.
