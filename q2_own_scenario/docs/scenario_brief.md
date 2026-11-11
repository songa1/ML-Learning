# Q2 Scenario Brief

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
- **Primary target:** `alevel_total_points`, the A-level aggregate points for one student-school-combination record.
- **Secondary analysis:** `high_performer`, optionally derived as the top third of results. The threshold must be calculated from the training data only.
- Recommendation happens after prediction by ranking expected outcomes across candidate schools and combinations. It is not a claim that the model determines a student's future.

## Candidate features known before A-level starts

- S3/O-level subject grades and aggregate.
- Gender, age, and coarse district or sector of origin.
- School type: public, government-aided, or private.
- Boarding or day status, province, and school size.
- Student-teacher ratio.
- Availability of a science laboratory, ICT laboratory, and library.
- Tuition fee, boarding fee, distance from home, and scholarship or support flag.
- Chosen subject combination.
- Previous-year school pass rate.

Post-outcome information must not be used as a feature. Examples include university admission, A-level subject marks, and whether the student repeated a year.

## Data plan

Use and compare at least two sources, in this order:

1. Public Rwanda data at school level from NESA/REB national examination results, MINEDUC education statistics yearbooks, and/or NISR/Rwanda Open Data.
2. Anonymised student-level records collected by the group through an approved Google Form or KoboToolbox survey of former Senior 3 completers.

The target is at least 1,000 records and 8 or more columns containing both numeric and categorical variables. Raw data should retain realistic quality problems, including missing values, duplicates, inconsistent school-name spellings, and outliers, so the preparation workflow can find and document them.

No Q2 data is being downloaded or generated in this scaffold phase. If real student-level data cannot be obtained in time, any simulated portion must be labelled synthetic in the source log and data card, and the lecturer must be informed. Synthetic data must never be presented as real Rwanda student records.

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
