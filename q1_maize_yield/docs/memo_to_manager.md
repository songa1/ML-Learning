# Memo to Manager

**To:** Mr. Habimana, Head of Planning and Data  
**From:** Junior Analyst (Group XX)  
**Date:** 2026-11-11  
**Subject:** Q1 Maize dataset readiness for ML analysis

1. **What we received:** We processed the raw file into clean train/validation/test datasets totaling 1192 usable records.
2. **Main problems found:** (i) duplicate and near-duplicate farm-season records, (ii) mixed units and numeric text formats, (iii) unrealistic/invalid values and missingness. These issues would bias estimates if not corrected.
3. **Data removed/changed:** Invalid targets were removed, inconsistent target values were recomputed from harvest and area when inputs were trustworthy, and leakage column `harvest_weight_kg` was removed from model features.
4. **New features for questions A-E:** Added fertilizer per hectare, planting time metrics, seed quality indicators, altitude/temperature/rainfall interactions, and low-yield risk label.
5. **Limits and risks:** Quality still depends on field-entry consistency and district reporting practices; risk analyses must avoid post-harvest leakage.
6. **Recommendation:** Dataset is ready for ML preparation tasks for A-E, with strongest support for A-D and leakage-safe setup for E. Next season, standardize digital forms and validation rules at capture time.
