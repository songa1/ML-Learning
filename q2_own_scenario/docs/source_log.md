# Q2 Source Log

## Core analytic table

- **File:** `rwanda_alevel_school_choice_dataset_RAW_MERGED.csv`
- **Rows and columns:** 1278 offers and 31 columns, covering 339 schools.
- **Unit of analysis:** one school x one A-level subject combination (or TVET trade) in the 2023/24 NESA results.
- **Target:** `alevel_avg_pct_2023_24`, available for 1225 of 1278 offers.
- **Source description:** school-level NESA 2023/24 A-level and O-level rankings, merged with the WDA 2020/21 accredited TVET school list using the supplied school codes and names.
- **Provenance checks:** the target and O-level values match `nesa_rankings_2023_24_parsed_long.csv` exactly on `school_code` and NESA section (maximum absolute difference 0.00).
- **Access date used in this run:** 2026-11-12.

## Supporting tables

- `nesa_rankings_2023_24_parsed_long.csv`: long-format NESA 2023/24 rankings (O-level and 15 A-level sections).
- `wda_tvet_schools_2020_21_parsed.csv`: WDA 2020/21 accredited TVET schools and trades.
- `combination_to_ranking_category_map.csv`: maps combination codes to NESA ranking sections.

## Limits and disclosure

- The WDA list is from 2020/21 while the NESA results are from 2023/24; accreditation may have changed.
- No student-level records, names, phone numbers, national IDs, or precise home locations are present.
- This is public school-level evidence. It supports an option-level benchmark, not a guarantee about an individual student.
- Confirm the NESA/REB and WDA publication licence terms and access URLs with the lecturer before submission; this log records file-level provenance only.
