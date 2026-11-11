import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "q2_own_scenario" / "notebooks"


def markdown(text):
    return {"cell_type": "markdown", "metadata": {"language": "markdown"}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {"language": "python"}, "outputs": [], "source": text.splitlines(True)}


BOOT = """import sys\nfrom pathlib import Path\nROOT = Path.cwd()\nwhile not (ROOT / 'src').exists() and ROOT != ROOT.parent:\n    ROOT = ROOT.parent\nif str(ROOT) not in sys.path:\n    sys.path.insert(0, str(ROOT))\n"""

NOTEBOOKS = {
    "00_environment_test.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 1: environment test"),
        markdown("How this works: confirm the runtime before any Q2 data work. The fixture used later is synthetic development data."),
        code(BOOT + """import platform\nimport pandas as pd\nimport numpy as np\nimport sklearn\nprint('Python:', platform.python_version())\nprint('pandas:', pd.__version__)\nprint('numpy:', np.__version__)\nprint('scikit-learn:', sklearn.__version__)\n"""),
    ],
    "01_acquire.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 2: acquisition and requirements"),
        markdown("How this works: load the labelled synthetic fixture as strings, inspect its shape and columns, and make the source disclosure visible before analysis."),
        code(BOOT + """from src.q2_config import RAW_FILE\nfrom src.q2_pipeline import load_raw\nraw = load_raw(RAW_FILE)\nprint('SYNTHETIC TEST DATA ONLY')\nprint('path:', RAW_FILE)\nprint('shape:', raw.shape)\nprint('columns:', raw.columns.tolist())\ndisplay(raw.head())\n"""),
    ],
    "02_eda.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 3: EDA and quality audit"),
        markdown("How this works: quantify missingness, duplicate records, inconsistent labels, invalid numeric values, and post-outcome leakage without changing the raw fixture."),
        code(BOOT + """import pandas as pd\nfrom src.q2_config import RAW_FILE, DOCS_DIR\nfrom src.q2_pipeline import load_raw\nraw = load_raw(RAW_FILE)\nreport = pd.DataFrame({\n    'check': ['duplicate rows', 'missing cells', 'post-outcome columns', 'inconsistent combination labels'],\n    'count': [int(raw.duplicated().sum()), int(raw.isna().sum().sum()), 3, int((raw['combination'].str.strip() != raw['combination']).sum())],\n    'treatment': ['remove after audit', 'train-only imputation', 'exclude from features', 'standardise labels'],\n})\nreport.to_csv(DOCS_DIR / 'q2_data_quality_report.csv', index=False)\nreport\n"""),
    ],
    "03_clean.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 4: cleaning and preprocessing"),
        markdown("How this works: clean categories and numeric fields, remove duplicate identifiers, and preserve the raw fixture unchanged. Every later transformation is fitted using training data only."),
        code(BOOT + """from src.q2_config import RAW_FILE, INTERIM_DIR\nfrom src.q2_pipeline import load_raw, clean_raw\nraw = load_raw(RAW_FILE)\ncleaned = clean_raw(raw)\nINTERIM_DIR.mkdir(parents=True, exist_ok=True)\ncleaned.to_csv(INTERIM_DIR / 'q2_clean.csv', index=False)\nprint('raw shape:', raw.shape)\nprint('clean shape:', cleaned.shape)\ndisplay(cleaned.head())\n"""),
    ],
    "04_features.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 5: feature engineering and selection"),
        markdown("How this works: create interpretable pre-A-level features for affordability, facilities, readiness, distance, and school context. Targets and post-outcome columns never enter X."),
        code(BOOT + """from src.q2_config import RAW_FILE\nfrom src.q2_pipeline import load_raw, clean_raw, add_features\nfeatures = add_features(clean_raw(load_raw(RAW_FILE)))\ncreated = ['fee_total', 'is_boarding', 'science_facility_count', 'academic_readiness', 'fee_per_school_place', 'distance_log1p', 'pass_rate_band']\nprint('created features:', created)\nprint('leakage excluded from model features: alevel_subject_points, university_admission, repeat_year')\ndisplay(features[created].head())\n"""),
    ],
    "05_finalise.ipynb": [
        markdown("Group XX | Members: [Student 1], [Student 2] | Question: Q2 | Stage: 6: finalise and verify"),
        markdown("How this works: split the cleaned data, fit preprocessing on train only, save encoded splits and the fitted transformer, and verify that leakage columns are absent from model inputs."),
        code(BOOT + """import joblib\nfrom src.q2_config import RAW_FILE, PROCESSED_DIR, TARGET, LEAKAGE_COLUMNS\nfrom src.q2_pipeline import load_raw, prepare_dataset\ncleaned, train, validation, test, encoded, labels, transformer = prepare_dataset(load_raw(RAW_FILE))\nPROCESSED_DIR.mkdir(parents=True, exist_ok=True)\nfor name, data in encoded.items():\n    output = data.copy()\n    output[TARGET] = labels[name][TARGET].to_numpy()\n    output['high_performer'] = labels[name]['high_performer'].to_numpy()\n    output.to_csv(PROCESSED_DIR / f'q2_{name}_model_ready.csv', index=False)\njoblib.dump(transformer, PROCESSED_DIR / 'q2_preprocessor.joblib')\nprint('split sizes:', len(train), len(validation), len(test))\nprint('train-only high performer threshold:', train[TARGET].quantile(1 / 3))\nprint('leakage columns excluded:', LEAKAGE_COLUMNS)\nprint('saved model-ready files and preprocessor')\n"""),
    ],
}


def main():
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    for filename, cells in NOTEBOOKS.items():
        notebook = {"cells": cells, "metadata": {"language": "python"}, "nbformat": 4, "nbformat_minor": 5}
        (NOTEBOOK_DIR / filename).write_text(json.dumps(notebook, indent=2) + "\n")
        print(f"wrote {filename}")


if __name__ == "__main__":
    main()