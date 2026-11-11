# Q2 Data Card

- **Purpose:** Development test of a pre-A-level school and combination recommendation dataset.
- **Data status:** Synthetic fixture; not real Rwanda student data.
- **Rows and columns:** 1,212 rows and 28 raw columns.
- **Target:** `alevel_total_points`.
- **Excluded leakage:** `alevel_subject_points`, `university_admission`, and `repeat_year`.
- **Known issues:** Duplicate records, missing values, inconsistent labels, malformed numeric text, and outliers are deliberately present.
- **Limitations:** Simulated relationships and distributions cannot support real student recommendations.
- **Replacement:** Acquire approved public school-level data and anonymised student-level records before reporting findings.