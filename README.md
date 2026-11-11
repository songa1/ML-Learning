# ML-Learning (Group XX)

This repository contains Question 1 (maize yield dataset preparation) and a scaffold for Question 2.

## Tool/library choices
- **Python, pandas, numpy**: reliable tabular cleaning and reproducible transformations.
- **matplotlib, seaborn**: EDA figures required by the assignment.
- **scikit-learn**: train-only preprocessing, splitting, encoders, scalers, and feature selection.
- **jupyter + nbformat + nbconvert**: notebook authoring and executable reproducible workflow.
- **joblib**: persist fitted preprocessing objects.

## Reproduce
```bash
python run_all.py
```

If `maize_yield_rwanda_raw.csv` is unavailable, the pipeline automatically builds and uses a clearly labelled stand-in file.
