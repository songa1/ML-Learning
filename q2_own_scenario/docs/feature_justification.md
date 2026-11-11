# Q2 Feature Justification

This document describes the development fixture workflow. Results must be replaced or rerun when approved public and anonymised student data is collected.

| Feature                  | Creation or decision                                                | Linked use                          |
| ------------------------ | ------------------------------------------------------------------- | ----------------------------------- |
| `academic_readiness`     | Mean of S3 mathematics, English, and science grades                 | Student-programme fit               |
| `fee_total`              | Tuition plus boarding fee                                           | Affordability comparison            |
| `is_boarding`            | Binary encoding of boarding/day status                              | School option context               |
| `science_facility_count` | Count of science lab, ICT lab, and library availability             | School resources                    |
| `fee_per_school_place`   | Total fee divided by school size                                    | Contextual affordability            |
| `distance_log1p`         | Log transform of distance from home                                 | Travel burden and skew control      |
| `pass_rate_band`         | Lower, middle, or higher previous pass-rate band                    | School context                      |
| Leakage columns          | Excluded: A-level subject points, university admission, repeat year | Recorded after the prediction point |
