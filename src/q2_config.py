from pathlib import Path

SEED = 42
ROOT = Path(__file__).resolve().parents[1]
Q2_DIR = ROOT / "q2_own_scenario"

RAW_DIR = Q2_DIR / "data" / "raw"
RAW_FILE = RAW_DIR / "rwanda_alevel_school_choice_dataset_RAW_MERGED.csv"
NESA_FILE = RAW_DIR / "nesa_rankings_2023_24_parsed_long.csv"
WDA_FILE = RAW_DIR / "wda_tvet_schools_2020_21_parsed.csv"
COMBINATION_MAP_FILE = RAW_DIR / "combination_to_ranking_category_map.csv"

INTERIM_DIR = Q2_DIR / "data" / "interim"
PROCESSED_DIR = Q2_DIR / "data" / "processed"
FIGURE_DIR = Q2_DIR / "figures"
DOCS_DIR = Q2_DIR / "docs"

# One row is a school x subject-combination offer, so the target is the school's
# average A-level percentage for that combination in 2023/24.
TARGET = "alevel_avg_pct_2023_24"

# Derived from the 2023/24 A-level results themselves, or identifiers/provenance
# fields that carry no generalisable signal. None of these may enter X.
LEAKAGE_COLUMNS = ["alevel_rank_in_category", "alevel_n_schools_in_category"]
ID_COLUMNS = [
    "school_code",
    "school_name",
    "district_code",
    "sector",
    "sector_code",
    "combination_name",
    "nesa_name_in_alevel_table",
    "wda_sn",
    "wda_match_score",
    "wda_match_method",
    "wda_school_name",
    "wda_province",
    "wda_district",
    "wda_sector",
    "wda_status",
    "wda_accredited_trades",
    "wda_accredited_levels",
    "wda_non_accredited",
    "boarding_note",
]

# Human-readable keys kept beside the encoded model inputs so every row stays traceable.
KEY_COLUMNS = [
    "school_code",
    "school_name",
    "combination_code",
    "combination_name",
    "district",
    "ranking_category",
    "school_category",
]

DISTRICT_TO_PROVINCE = {
    "Gasabo": "Kigali City",
    "Kicukiro": "Kigali City",
    "Nyarugenge": "Kigali City",
    "Huye": "Southern",
    "Gisagara": "Southern",
    "Nyanza": "Southern",
    "Nyamagabe": "Southern",
    "Nyaruguru": "Southern",
    "Muhanga": "Southern",
    "Kamonyi": "Southern",
    "Ruhango": "Southern",
    "Karongi": "Western",
    "Ngororero": "Western",
    "Nyabihu": "Western",
    "Nyamasheke": "Western",
    "Rubavu": "Western",
    "Rusizi": "Western",
    "Rutsiro": "Western",
    "Burera": "Northern",
    "Gakenke": "Northern",
    "Gicumbi": "Northern",
    "Musanze": "Northern",
    "Rulindo": "Northern",
    "Bugesera": "Eastern",
    "Gatsibo": "Eastern",
    "Kayonza": "Eastern",
    "Kirehe": "Eastern",
    "Ngoma": "Eastern",
    "Nyagatare": "Eastern",
    "Rwamagana": "Eastern",
}

WDA_STATUS_MAP = {
    "public": "Public",
    "gov. aided": "Public",
    "gov aided": "Public",
    "gov'aided": "Public",
    "gov't aided": "Public",
    "gov.aid": "Public",
    "gov.aided": "Public",
    "government aided": "Public",
    "gvnt aided": "Public",
    "private": "Private",
}

SCHOOL_CATEGORY_MAP = {
    "General Education": "General Education",
    "TVET": "TVET",
    "TTC": "TTC",
    "Professional Education": "Professional Education",
    "NINE_TWELVE_YBE_GS": "Nine-Twelve YBE (GS)",
    "NINE_TWELVE_YBE_ESI": "Nine-Twelve YBE (ESI)",
    "SPECIAL_NEEDS_EDUCATION_SCHOOL": "Special Needs Education",
}
