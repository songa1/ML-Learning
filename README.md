# ML-Learning (Group Achille-Sylvie)

This repository contains the dataset-preparation work for the TVET/ICT practical task **Two Rwandan Scenarios: Build Machine-Learning-Ready Datasets**.

- **Question 1:** maize yield preparation for the Maize Cooperative Support Unit (MCSU).
- **Question 2:** A-level performance and school/combination recommendation for the Student Pathways Advisory Unit (SPAU).

Replace `Group Achille-Sylvie` and the student placeholders in the notebooks and documentation with the group number and names before submission.

## Environment Setup

The declared environment uses Python 3.10+ and the libraries in [environment.yml](environment.yml): pandas, numpy, matplotlib, seaborn, scikit-learn, Jupyter, nbformat, nbconvert, joblib, and pyarrow.

### Conda

From the repository root:

```bash
conda env create -f environment.yml
conda activate ml-project
```

If the environment already exists:

```bash
conda env update -f environment.yml --prune
conda activate ml-project
```

### Python virtual environment

Use this when Conda is unavailable:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pandas numpy matplotlib seaborn scikit-learn jupyter nbformat nbconvert joblib pyarrow
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. On Linux or macOS, use `source .venv/bin/activate`.

The project requires network access to install packages. If the operating system reports an externally managed Python, use the virtual environment or Conda; do not install into the system interpreter with an override.

## Running Question 1

Question 1 is the maize-yield workflow. From the repository root, after activating the environment:

```bash
python run_all.py
```

`run_all.py` executes the combined [Q1 workflow notebook](q1_maize_yield/notebooks/q1_maize_yield_workflow.ipynb) from top to bottom and then runs [verify.py](tools/verify.py):

1. Environment test
2. Requirements and acquisition
3. EDA and data-quality audit
4. Cleaning and preprocessing
5. Feature engineering and selection
6. Finalisation and verification
7. Answers to the cooperative questions A–E

The revised Q1 source is `maize_yield_rwanda_rw.csv`. The acquisition notebook preserves this file unchanged. Its target is `yield_t_ha`, which the cleaning workflow converts to the model target `yield_kg_per_ha`; NPK, urea, and manure are combined into a comparable fertiliser-per-hectare measure. The old synthetic stand-in is no longer used by the Q1 notebooks.

The final step answers the five cooperative questions with tables and charts: expected yield per hectare (A), fertiliser and improved-seed comparisons at a fair per-hectare rate (B), rainfall/temperature/altitude/irrigation effects (C), province, district and season differences (D), and high-risk farms (E). The detailed write-up is in [cooperative_answers.md](q1_maize_yield/docs/cooperative_answers.md). The derived `low_yield_risk` label is excluded from model features so the risk answer does not leak the harvest result.

Important Q1 outputs are written to:

- `q1_maize_yield/data/interim/`: cleaned audit data.
- `q1_maize_yield/data/processed/`: train, validation, and test files plus the fitted preprocessing pipeline.
- `q1_maize_yield/figures/`: EDA charts.
- `q1_maize_yield/docs/`: requirements, data dictionary, source log, quality report, cleaning log, feature justification, data card, manager memo, and verification notes.

## Running Question 2

Question 2 prepares a school × subject-combination benchmark from public Rwanda school-level data. The unit of analysis is one school × one A-level combination (or TVET trade) offered in the 2023/24 NESA results, not one student. The target is `alevel_avg_pct_2023_24`, the school-combination average A-level percentage.

Build or rebuild the JSON notebooks:

```bash
python tools/build_q2_notebooks.py
```

Execute the combined Q2 workflow notebook and verification:

```bash
python run_q2.py
```

The Q2 stages, presented as sections in [q2_student_pathways_workflow.ipynb](q2_own_scenario/notebooks/q2_student_pathways_workflow.ipynb), are:

1. Environment and raw-file inventory
2. Acquisition and schema documentation
3. EDA, coverage, and quality audit
4. Cleaning and logged decisions
5. Feature engineering and leakage control
6. Splitting, encoding, and final verification

The raw sources in `q2_own_scenario/data/raw/` are:

- `rwanda_alevel_school_choice_dataset_RAW_MERGED.csv`: 1,278 school × combination offers and 31 columns.
- `nesa_rankings_2023_24_parsed_long.csv`: 4,470 NESA O-level and A-level ranking rows.
- `wda_tvet_schools_2020_21_parsed.csv`: 192 WDA-accredited TVET schools.
- `combination_to_ranking_category_map.csv`: 51 combination-to-ranking-section mappings.

The workflow cleans 1,278 offers to 1,225 with a target, splits them 857/184/184, and writes the model-ready files, preprocessor, dictionaries, quality report, cleaning log, feature justification, data card, and EDA figures. The earlier synthetic student fixture (`q2_student_school_combination_SYNTHETIC_TEST.csv`) and [make_standin_q2.py](tools/make_standin_q2.py) are no longer read by the Q2 workflow.

## Q2 Data and Leakage Rules

The Q2 target is `alevel_avg_pct_2023_24`, measured at school × combination level. Candidate features must be known before A-level results are published: school type and location, programme family, intake policy, prior O-level performance and rank, WDA accreditation coverage and trade breadth, and programme breadth.

The following columns are derived from the 2023/24 A-level results and are leakage, so they must not be model features:

- `alevel_rank_in_category`
- `alevel_n_schools_in_category`

School identifiers, WDA record-linkage fields, `sector` (finer than the approved coarse district), and free-text fields are also excluded. Do not collect or store names, phone numbers, national IDs, or precise home locations. Fairness checks should compare performance and recommendations by gender, district, and school type.

This dataset has no student-level grades, fees, distance, boarding availability, or facilities. It supports an option-level benchmark; a student-level recommendation also needs those inputs and must not treat the benchmark as a guarantee.

## Repository Structure

```text
src/                         Shared Q1 and Q2 preparation code
tools/                       Data generators, notebook builders, and verifiers
q1_maize_yield/              Q1 data, notebooks, figures, and documentation
q2_own_scenario/             Q2 data, notebooks, figures, and documentation
docs/                        Contribution and final documentation outlines
run_all.py                   Execute and verify Q1
run_q2.py                   Execute and verify Q2
environment.yml              Conda environment specification
```

## Reproducibility and Good Practice

- The fixed random seed is 42.
- Raw data is loaded without editing the source file.
- Train/validation/test splits are made before fitting imputers, scalers, encoders, or thresholds.
- Leakage columns are excluded from model inputs.
- Cleaning and feature decisions are recorded in the relevant logs.
- Do not use test data to choose transformations or features.
- Run notebooks from a clean kernel in the documented order when preparing screenshots.
- Keep screenshots showing the notebook name and the group-number cell, as required by the assignment.
- Both students must make genuine commits for the contribution requirement; do not fake authorship.

## Troubleshooting

`No module named jupyter` means the active interpreter is not the project environment. Activate `ml-project` or `.venv`, then check:

```bash
python -c "import jupyter, pandas, sklearn; print('environment ready')"
```

If package installation fails with a DNS or network error, restore network access or use an existing approved Conda mirror, then rerun the installation. Do not claim that `run_all.py` or `run_q2.py` passed until the command has completed successfully.

The project does not train a production prediction model. Q1 stops at a model-ready dataset, and Q2 stops at a model-ready school-level option benchmark; student-level recommendation remains future work.
