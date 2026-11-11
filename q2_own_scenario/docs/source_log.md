# Q2 Source Log

## Development test file

- **File:** `q2_student_school_combination_SYNTHETIC_TEST.csv`
- **Source:** Generated locally by `tools/make_standin_q2.py` for pipeline development and testing only.
- **Status:** Synthetic; it is not Rwanda student data and must not be presented as real evidence.
- **Rows and columns:** 1,212 rows and 28 columns after deliberately adding duplicate records and quality issues.
- **Seed:** 42.
- **Contains:** Pre-A-level candidate features, the regression target `alevel_total_points`, and post-outcome columns included only to test leakage detection.
- **Limitations:** Simulated relationships, school coverage, distributions, and outcomes do not represent actual students, schools, or national results.
- **Replacement plan:** Replace this file with approved public and anonymised survey sources before reporting Q2 findings. Update this log with URLs, access dates, licences, permissions, collection method, and ethical controls.

## Required disclosure

Any Q2 notebook or report run against this file must state that the results are based on synthetic test data. The file is a development fixture, not a basis for recommendations about real students.