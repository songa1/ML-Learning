# Q2 Scenario Brief

> **Implementation update (12 November 2026):** The public data now available is school-level, so the implemented workflow uses one row per school × A-level combination and the target `alevel_avg_pct_2023_24`. The original student-level target (`alevel_total_points`) remains the plan once approved anonymised student records are collected. This notebook prepares the option-level benchmark that the future student-level recommender will use.

## Title

Predicting A-Level Performance to Recommend the Best-Fit School and Combination for Senior 3 Leavers

## Context

- **Location:** Huye District, Southern Province. Students may choose schools nationwide, including students from Huye, Nyanza, Gisagara, Nyamagabe, and Muhanga.
- **Stakeholder:** Student Pathways Advisory Unit (SPAU), led by Head of Guidance Mrs. Uwase.
- **Who benefits:** Senior 3 leavers and their parents, schools seeking better student-programme matches, and district education offices targeting support.

## Problem and decision

After the Senior 3 national examination, each student must choose an Advanced-level school and subject combination, such as MPC, PCB, MCB, MEG, HEG, HEL, LEG, or a TVET/teacher-training track. Families often choose by reputation, distance, or fees rather than fit. A poor match may increase dropout, repeated years, and weak A-level results.

SPAU needs a recommender that estimates the expected A-level result for each candidate school and combination, then ranks the best-fit options. The decision supported is which 3 to 5 school/combination options to recommend for a particular student, with fees, boarding status, and distance shown alongside the ranking.

## Prediction targets

- **Primary problem:** Regression.
- **Current unit of analysis:** one school × one A-level subject combination (or TVET trade) offered in the 2023/24 NESA results.
- **Current primary target:** `alevel_avg_pct_2023_24`, the school-combination average A-level percentage (0–100).
- **Planned student-level target:** `alevel_total_points`, the A-level aggregate points for one student-school-combination record, once approved anonymised survey records exist.
- **Secondary analysis:** `high_performer`, the top third of results. The threshold must be calculated from the training data only; the current notebook uses the training top third (about 72.5).
- Recommendation happens after prediction by ranking expected outcomes across candidate schools and combinations. It is not a claim that the model determines a student's future.

## Candidate features for the planned student-level model

- S3/O-level subject grades and aggregate.
- Gender, age, and coarse district or sector of origin.
- School type: public, government-aided, or private.
- Boarding or day status, province, and school size.
- Student-teacher ratio.
- Availability of a science laboratory, ICT laboratory, and library.
- Tuition fee, boarding fee, distance from home, and scholarship or support flag.
- Chosen subject combination.
- Previous-year school pass rate.

Post-outcome information must not be used as a feature. In the current data, `alevel_rank_in_category` and `alevel_n_schools_in_category` are computed from the same A-level results and are excluded. In a future student-level file, university admission, A-level subject marks, and repeat-year status must also be excluded.

**What the current public data supports:** district and province, school category, combination and programme family, intake policy, prior O-level average and national rank, WDA listing and accredited-trade breadth, and programme breadth. It does **not** contain student grades, fees, distance, boarding availability, or facilities; those must be joined before an individual recommendation is shown.

## Data plan

Use and compare at least two sources, in this order:

1. Public Rwanda data at school level from NESA/REB national examination results, MINEDUC education statistics yearbooks, and/or NISR/Rwanda Open Data.
2. Anonymised student-level records collected by the group through an approved Google Form or KoboToolbox survey of former Senior 3 completers.

The target is at least 1,000 records and 8 or more columns containing both numeric and categorical variables. Raw data should retain realistic quality problems, including missing values, duplicates, inconsistent school-name spellings, and outliers, so the preparation workflow can find and document them.

**Data actually used (current notebook):** the merged school-level extract of NESA 2023/24 A-level and O-level rankings and the WDA 2020/21 accredited TVET list, with 1,278 school × combination offers. Provenance, coverage, and licence caveats are recorded in `source_log.md`; the earlier synthetic student fixture is no longer used by the Q2 workflow. No student-level records have been acquired yet, so the current model-ready dataset supports an option benchmark only.

## Ethics, fairness, and data protection

- Do not collect names, phone numbers, national identification numbers, or other direct identifiers.
- Use coarse district-level location rather than precise home locations.
- Confirm permission and licence conditions for every public and survey source.
- Audit performance and recommendations by gender, district, and fee level.
- Check whether gender should be excluded as a feature and test proxy risks such as school type or distance.
- Watch for selection bias because students who remain in school are more visible than those who leave.
- Treat previous-year school pass rates carefully because they may reflect survivorship bias and unequal resources.
- Report missing student-level outcomes and coverage gaps instead of silently filling them with invented values.

## Planned Q2 workflow

When Q2 is implemented, it should follow the same reproducible pattern as Q1: acquire and log sources, audit quality without changing raw data, clean with every change logged, split before learning preprocessing parameters, engineer only pre-A-level features, evaluate leakage and fairness risks, and verify deterministic outputs. The fixed project seed remains 42 unless the assignment is amended.
