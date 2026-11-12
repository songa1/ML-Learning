# Q2 Data Card

- **Purpose:** model-ready benchmark of A-level performance by school x subject combination for the Student Pathways Advisory Unit.
- **Data status:** public school-level NESA 2023/24 and WDA 2020/21 extracts. No synthetic or student-level records are used.
- **Rows:** 1225 school x combination offers after cleaning.
- **Split:** train=857, validation=184, test=184, stratified on programme family with seed 42.
- **Target:** `alevel_avg_pct_2023_24`, the school-combination average A-level percentage (0-100).
- **Secondary label:** `high_performer`, top third of the training target; threshold = 72.48.
- **Leakage excluded:** `alevel_rank_in_category` and `alevel_n_schools_in_category`.
- **Known issues:** 53 offers lack a target; O-level records are missing for TTCs and many TVET schools; WDA coverage is partial; boarding notes are almost absent; the WDA list is from 2020/21 while results are 2023/24.
- **Limitations:** the table has no student-level grades, fees, distance, boarding availability, or facilities. It supports an option-level benchmark, not a prediction for an individual student. School averages can hide within-school variation.
- **Prepared:** 2026-11-12.
- **Licence:** confirm NESA/REB and WDA publication terms and access dates with the lecturer before submission.
