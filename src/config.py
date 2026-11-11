from pathlib import Path

SEED = 42
ROOT = Path(__file__).resolve().parents[1]
Q1_DIR = ROOT / "q1_maize_yield"
Q2_DIR = ROOT / "q2_own_scenario"

RAW_DIR = Q1_DIR / "data" / "raw"
INTERIM_DIR = Q1_DIR / "data" / "interim"
PROCESSED_DIR = Q1_DIR / "data" / "processed"
NOTEBOOK_DIR = Q1_DIR / "notebooks"
FIGURE_DIR = Q1_DIR / "figures"
DOCS_DIR = Q1_DIR / "docs"

RAW_FILE = RAW_DIR / "maize_yield_rwanda_raw.csv"
STANDIN_FILE = RAW_DIR / "maize_yield_rwanda_SYNTHETIC_STANDIN.csv"

TARGET_COL = "yield_kg_per_ha"
LEAKAGE_COLS = ["harvest_weight_kg"]
ID_COLS = ["farm_id", "cooperative_id"]

COLUMNS = [
    "farm_id", "province", "district", "cooperative_id", "altitude_m", "season", "planting_date",
    "farm_size", "farm_size_unit", "seed_variety", "fertilizer_kg", "rainfall_mm", "avg_temp_c",
    "soil_type", "soil_ph", "pest_incidence", "irrigation", "farmer_age", "harvest_weight_kg", "yield_kg_per_ha"
]

DISTRICT_TO_PROVINCE = {
    "gatsibo": "eastern", "kayonza": "eastern", "nyagatare": "eastern", "rwamagana": "eastern",
    "bugesera": "eastern", "ngoma": "eastern", "nyarugenge": "southern", "huye": "southern",
    "nyanza": "southern", "gisagara": "southern", "nyamagabe": "southern", "muhanga": "southern",
    "musanze": "northern", "gicumbi": "northern", "rubavu": "western", "rusizi": "western",
    "karongi": "western", "ngororero": "western",
}

SEASON_START_MONTH = {"a": 9, "b": 2, "c": 6}
