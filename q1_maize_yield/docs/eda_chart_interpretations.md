# EDA Figure Notes

- **hist_yield_kg_per_ha.png**: Yield shows skew and suspicious extremes, supporting robust cleaning and clipping rules.
- **hist_fertilizer_kg.png**: Fertilizer totals vary widely because farm sizes differ, motivating fertilizer per hectare.
- **hist_rainfall_mm.png**: Rainfall has long tails and a few implausible high values likely from entry errors.
- **hist_avg_temp_c.png**: Temperature centers in agronomic range but includes impossible points needing correction.
- **bar_season.png**: Seasons A and B dominate records; C is smaller, affecting stratification and fairness checks.
- **box_yield_seed.png**: Improved/Hybrid seeds tend to higher medians, aligned with stakeholder question B.
- **scatter_yield_fertilizer_perha.png**: Yield tends to increase with fertilizer/ha but with diminishing and noisy relationship.
- **heatmap_corr.png**: Numeric correlations are moderate; no single factor explains yield alone.