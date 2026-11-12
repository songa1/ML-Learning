# Q1 Answers to the Cooperative Questions

These answers use the cleaned 1,426-record maize dataset. They are observational associations, not causal proof.

## A. How much maize can a farm expect per hectare?
Mean 2.57 t/ha and median 2.58 t/ha; the central 80% is 1.68-3.48 t/ha. Province means are 2.47-2.65 t/ha. Season means are A 2.86, B 2.51 and C 2.00 t/ha.

## B. Do fertiliser and improved seed increase yield?
Hybrid seed averages 2.76 t/ha versus 1.80 for local seed (+0.96, +53%). Improved practice averages 2.74 versus 2.37 t/ha (+0.37, +16%). The highest fertiliser tercile averages 2.70 versus 2.48 t/ha in the lowest (+0.22, +9%). Fertiliser is measured per hectare, and its correlation with farm size is about -0.02, so the comparison is not driven by farm size.

## C. How do rainfall, temperature, altitude and irrigation affect yield?
Rainfall has the strongest positive association (Spearman +0.35; 2.12 t/ha in the driest quartile to 2.80 in the wettest). Temperature (-0.02) and altitude (+0.05) are weak. Irrigation averages 2.53 t/ha versus 2.58 without it in these records, but only 128 farms are irrigated and the group is not randomised. Pest incidence (-0.20) and plant density (+0.28) are stronger correlates than temperature or altitude.

## D. Do results differ by province, district and season?
Season is the largest difference: A 2.86, B 2.51 and C 2.00 t/ha. Province means range from 2.47 (Eastern) to 2.65 (Southern). Districts with at least 20 records range from 2.34 (Gatsibo) to 2.83 (Muhanga). There are 30 consistent district labels, each mapped to one province, and only seasons A/B/C. Planting dates are not in the source, so date-level comparisons are not possible.

## E. Which farms are at high risk of a very low harvest?
The training-set 20th percentile is 1.95 t/ha; 19.8% of cleaned records are below it. Risk is 44.7% in season C, 64.4% for local seed versus 8.9% for hybrid, 22.3% in the low fertiliser tercile versus 14.3% in the high tercile, and 24.1% in Eastern and 22.1% in Western provinces. The harvest target and the derived risk label are excluded from model features, so the screening uses only pre-harvest information.

## Limitations
- The data are observational; the comparisons do not prove causal effects.
- The source has no planting-date column, so only season-level timing can be compared.
- Irrigation is recorded for only 128 farms and is not randomly assigned.
- Yield was winsorized at the 1st and 99th percentiles during cleaning.
