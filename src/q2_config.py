from pathlib import Path

SEED = 42
ROOT = Path(__file__).resolve().parents[1]
Q2_DIR = ROOT / "q2_own_scenario"
RAW_FILE = Q2_DIR / "data" / "raw" / "q2_student_school_combination_SYNTHETIC_TEST.csv"
INTERIM_DIR = Q2_DIR / "data" / "interim"
PROCESSED_DIR = Q2_DIR / "data" / "processed"
FIGURE_DIR = Q2_DIR / "figures"
DOCS_DIR = Q2_DIR / "docs"
TARGET = "alevel_total_points"
LEAKAGE_COLUMNS = ["alevel_subject_points", "university_admission", "repeat_year"]
ID_COLUMNS = ["student_record_id"]
