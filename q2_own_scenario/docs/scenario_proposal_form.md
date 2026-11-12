# Q2 Scenario Proposal Form

> **Implementation update (12 November 2026):** Public school-level data has been acquired, so the implemented workflow uses one row per school × A-level combination and the target `alevel_avg_pct_2023_24`. The student-level unit and `alevel_total_points` target below remain the plan once approved anonymised records are collected.

## 1. Scenario identification

- **Scenario title:** Predicting A-Level Performance to Recommend the Best-Fit School and Combination for Senior 3 Leavers
- **Location:** Huye District, Southern Province; students may select schools nationwide.
- **Stakeholder:** Student Pathways Advisory Unit (SPAU), Head of Guidance Mrs. Uwase.
- **Beneficiaries:** Senior 3 leavers and parents, schools, and district education offices.

## 2. Problem and decision

- **Problem:** Students and families often choose an A-level school and subject combination by reputation, distance, or fees rather than student-programme fit. Poor matching can contribute to dropout, repeated years, and poor A-level outcomes.
- **Decision supported:** For each student, rank and present the best 3 to 5 candidate school/combination options, including expected result, fees, boarding status, and distance.
- **Problem type:** Regression first; classification is secondary.

## 3. Target and unit of analysis

- **Current unit of analysis:** One school × one A-level subject combination (or TVET trade) offered in the 2023/24 NESA results. This is the level at which public data is available.
- **Current primary target:** `alevel_avg_pct_2023_24` (school-combination average A-level percentage, 0–100).
- **Planned student-level unit and target:** One anonymised student-school-combination record with `alevel_total_points` (A-level aggregate points), once approved survey records exist.
- **Optional secondary target:** `high_performer`, defined as the top third of outcomes using a training-set-only threshold (currently about 72.5).
- **Recommendation method:** Use the option-level benchmark to score each eligible candidate option, then rank the predictions with student eligibility and family constraints. The model will support guidance, not make an automatic final decision.

## 4. Proposed input variables

- **Student:** O-level/S3 subject grades, S3 aggregate, gender for fairness auditing, age, and coarse district or sector of origin.
- **School:** school type, boarding/day status, province, school size, student-teacher ratio, laboratories, library, previous-year pass rate, tuition fee, boarding fee, distance from home, and scholarship/support flag.
- **Choice:** intended subject combination, such as MPC, PCB, MCB, MEG, HEG, HEL, LEG, or TVET/teacher-training tracks.
- **Leakage exclusions:** university admission, A-level subject marks, repeat-year status, and any other information recorded after the A-level outcome.

## 5. Data sources and collection

- **Source 1:** Public Rwanda school-level data from NESA/REB examination results, MINEDUC education statistics yearbooks, and/or NISR/Rwanda Open Data.
- **Source 2:** Approved anonymised student-level records collected by the group through a Google Form or KoboToolbox survey of former Senior 3 completers.
- **Minimum planned size:** At least 1,000 records and 8 or more columns, with numeric and categorical variables.
- **Quality requirement:** Retain and document realistic raw-data issues such as missing values, duplicate records, inconsistent school-name spellings, and outliers.
- **Current status:** Public school-level data has been acquired: a merged NESA 2023/24 A-level/O-level extract with 1,278 school × combination offers, the long-format NESA ranking table, the WDA 2020/21 accredited TVET list, and a combination-to-ranking-section map. The Q2 notebook prepares 1,225 offers with a target. No approved student-level records have been collected yet.

## 6. Ethics, fairness, and limitations

- Remove direct identifiers and collect no names, phone numbers, or national IDs.
- Use coarse district-level location and protect access to any survey data.
- Record permission and licence conditions for every source.
- Audit results and recommendations by gender, district, and fee level.
- Test whether gender should be excluded and assess proxy variables such as school type and distance.
- Address selection bias because available records may over-represent students who stayed in school.
- Treat school pass rates cautiously because they may contain survivorship bias.

## 7. Honesty declaration

The group will not present simulated data as real. If real student-level outcomes cannot be obtained, every simulated portion will be labelled synthetic in the source log and data card, and the lecturer will be informed before results are presented.

## 8. Approval and implementation status

- **Approval needed before collection:** Confirm lecturer/stakeholder permission, survey consent wording, privacy controls, and source licences.
- **Implementation status:** The school-level preparation workflow is implemented, executed, and verified. Student-level acquisition and the recommendation interface remain deferred until approved anonymised records and student/family inputs (grades, fees, distance, boarding) are available.
