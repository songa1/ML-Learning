# Predicting A-Level Performance to Recommend Best-Fit School/Combination

(Verbatim brief from assignment Section 9.)

Title: Predicting A-Level Performance to Recommend the Best-Fit School and Combination for Senior 3 Leavers.
Location: Huye District, Southern Province, with choices nationwide.
Stakeholder: SPAU (Mrs. Uwase).
Problem: Recommend 3-5 best-fit A-level school/combination options and reduce mismatch risk.
Primary target: `alevel_total_points` (regression); optional secondary `high_performer`.
Features: pre-A-level only (exam performance, school context, cost, distance, etc.), no post-outcome leakage.
Data plan: combine Rwanda public school-level data + anonymized student-level collection; honesty rule on synthetic data.
Risks: privacy, bias/fairness, permissions/licence, missing outcomes, survivorship bias.
Problem type: regression primary, classification secondary.
