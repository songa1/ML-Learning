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

RAW_FILE = RAW_DIR / "maize_yield_rwanda_rw.csv"
STANDIN_FILE = RAW_DIR / "maize_yield_rwanda_SYNTHETIC_STANDIN.csv"

TARGET_COL = "yield_kg_per_ha"
# Derived from the target after the split; it is a label for risk reporting, never a feature.
LEAKAGE_COLS = ["low_yield_risk"]
ID_COLS = ["record_id"]

COLUMNS = [
    "record_id", "year", "season", "province", "district", "altitude_m", "rainfall_mm",
    "avg_temp_c", "soil_ph", "soil_type", "seed_variety", "farming_practice",
    "npk_kg_ha", "urea_kg_ha", "manure_t_ha", "plant_density_per_ha", "farm_area_ha",
    "irrigation", "pest_incidence_index", "yield_t_ha"
]

DISTRICT_TO_PROVINCE = {
    "gatsibo": "eastern", "kayonza": "eastern", "nyagatare": "eastern", "rwamagana": "eastern",
    "bugesera": "eastern", "ngoma": "eastern", "nyarugenge": "southern", "huye": "southern",
    "nyanza": "southern", "gisagara": "southern", "nyamagabe": "southern", "muhanga": "southern",
    "musanze": "northern", "gicumbi": "northern", "rubavu": "western", "rusizi": "western",
    "karongi": "western", "ngororero": "western",
}

SEASON_START_MONTH = {"a": 9, "b": 2, "c": 6}
