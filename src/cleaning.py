import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from .config import DISTRICT_TO_PROVINCE, TARGET_COL

MISSING_TOKENS = {"", " ", "na", "n/a", "none", "null", "unknown", "?", "-999", "-1"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def to_string_df(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _norm(x):
    return str(x).strip().lower()


def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if out[c].dtype == object:
            out[c] = out[c].astype(str).str.strip()

    mapping = {
        "season": {"season a": "A", "a": "A", "season-a": "A", "season b": "B", "b": "B", "season-b": "B", "season c": "C", "c": "C", "season-c": "C"},
        "irrigation": {"yes": "Yes", "y": "Yes", "1": "Yes", "true": "Yes", "no": "No", "n": "No", "0": "No", "false": "No"},
        "soil_type": {"clay": "Clay", "clay loam": "Clay loam", "loam": "Loam", "sandy loam": "Sandy loam", "volcanic": "Volcanic"},
        "farming_practice": {"traditional": "Traditional", "improved": "Improved"},
    }
    for col, mp in mapping.items():
        if col in out.columns:
            out[col] = out[col].map(lambda v: mp.get(_norm(v), v))

    for col in ["district", "province", "record_id"]:
        if col in out.columns:
            out[col] = out[col].astype(str).str.strip().str.lower()

    if "province" in out.columns and "district" in out.columns:
        mapped = out["district"].map(DISTRICT_TO_PROVINCE)
        fill_mask = mapped.notna()
        out.loc[fill_mask, "province"] = mapped[fill_mask]
        out["province"] = out["province"].str.title()
        out["district"] = out["district"].str.title()

    return out


def parse_number(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.replace(",", "", regex=False)
    s = s.str.replace("kg", "", regex=False).str.replace("ha", "", regex=False).str.strip()
    s = s.replace(list(MISSING_TOKENS), np.nan)
    return pd.to_numeric(s, errors="coerce")


def clean_q1(df_raw: pd.DataFrame, clog) -> pd.DataFrame:
    df = standardize_text(df_raw)
    before_shape = df.shape

    for col in ["year", "altitude_m", "rainfall_mm", "avg_temp_c", "soil_ph", "npk_kg_ha",
                "urea_kg_ha", "manure_t_ha", "plant_density_per_ha", "farm_area_ha",
                "pest_incidence_index", "yield_t_ha"]:
        df[col] = parse_number(df[col])

    df["fertilizer_kg"] = df["npk_kg_ha"] + df["urea_kg_ha"] + (df["manure_t_ha"] * 1000)
    df["farm_size_ha"] = df["farm_area_ha"]
    df[TARGET_COL] = df["yield_t_ha"] * 1000
    df["pest_incidence"] = pd.cut(df["pest_incidence_index"], [-np.inf, 0.33, 0.66, np.inf], labels=["Low", "Medium", "High"])
    clog.add("derive_canonical_fields", "fertilizer_kg,farm_size_ha,yield_kg_per_ha,pest_incidence", "derive model fields from source columns", len(df), before_shape, df.shape, "map the revised source schema to consistent Q1 model units")

    bad_year = (df["year"].notna()) & (~df["year"].between(2015, 2030))
    n_bad_year = int(bad_year.sum())
    df.loc[bad_year, "year"] = np.nan
    clog.add("year_range", "year", "outside 2015-2030 set to missing", n_bad_year, before_shape, df.shape, "remove impossible source years")

    # Duplicates
    n0 = len(df)
    df = df.drop_duplicates()
    n1 = len(df)
    clog.add("drop_exact_duplicates", "all", "remove exact duplicate rows", n0 - n1, n0, n1, "duplicate submissions")

    # Near duplicates: record_id should identify one observation.
    df["_completeness"] = df.notna().sum(axis=1)
    n_before = len(df)
    df = df.sort_values("_completeness", ascending=False).drop_duplicates(subset=["record_id"], keep="first")
    n_after = len(df)
    df = df.drop(columns=["_completeness"])
    clog.add("dedupe_near", "record_id", "keep most complete record", n_before - n_after, n_before, n_after, "resolve repeated source identifiers")

    # Impossible value handling
    rules = {
        TARGET_COL: lambda s: s <= 0,
        "farm_size_ha": lambda s: s <= 0,
        "fertilizer_kg": lambda s: s < 0,
        "rainfall_mm": lambda s: (s < 0) | (s > 5000),
        "avg_temp_c": lambda s: (s < 0) | (s > 60),
        "altitude_m": lambda s: (s < 500) | (s > 3500),
        "soil_ph": lambda s: (s < 4) | (s > 8),
        "plant_density_per_ha": lambda s: s <= 0,
    }
    for col, fn in rules.items():
        bad = fn(df[col]) & df[col].notna()
        n_bad = int(bad.sum())
        df.loc[bad, col] = np.nan
        clog.add("set_invalid_nan", col, "apply agronomic plausibility rule", n_bad, "valid+invalid", "invalid->NaN", "protect data quality before imputation")

    # Drop rows with missing target
    n_before = len(df)
    df = df[df[TARGET_COL].notna()]
    n_after = len(df)
    clog.add("drop_missing_target", TARGET_COL, "drop unusable target rows", n_before - n_after, n_before, n_after, "supervised dataset requires target")

    # Winsorize a few skewed numerics
    for col in ["fertilizer_kg", "rainfall_mm", TARGET_COL]:
        s = df[col]
        lo, hi = s.quantile([0.01, 0.99])
        clipped = s.clip(lo, hi)
        n_clip = int((s != clipped).sum())
        df[col] = clipped
        clog.add("winsorize", col, "clip at 1st/99th percentiles", n_clip, f"[{s.min():.2f},{s.max():.2f}]", f"[{df[col].min():.2f},{df[col].max():.2f}]", "cap likely entry-error extremes while keeping records")

    return df.reset_index(drop=True)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["year_season"] = out["year"].astype("Int64").astype(str) + "_" + out["season"].astype(str)
    out["rainfall_per_temp"] = out["rainfall_mm"] / out["avg_temp_c"].replace(0, np.nan)
    return out
