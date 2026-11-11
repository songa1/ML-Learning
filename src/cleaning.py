import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from .config import DISTRICT_TO_PROVINCE, SEASON_START_MONTH, TARGET_COL

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
        "pest_incidence": {"low": "Low", "medium": "Medium", "high": "High"},
        "soil_type": {"clay": "Clay", "loam": "Loam", "sandy": "Sandy"},
        "seed_variety": {"local": "Local", "improved": "Improved", "hybrid": "Hybrid"},
    }
    for col, mp in mapping.items():
        if col in out.columns:
            out[col] = out[col].map(lambda v: mp.get(_norm(v), v))

    for col in ["district", "province", "farm_id", "cooperative_id"]:
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


def convert_farm_size_ha(df: pd.DataFrame) -> pd.Series:
    size = parse_number(df["farm_size"])
    unit = df["farm_size_unit"].astype(str).str.strip().str.lower()
    unit = unit.replace({"m2": "m2", "sqm": "m2", "m²": "m2", "square meter": "m2", "ha": "ha", "hectare": "ha", "hectares": "ha", "acre": "acre", "acres": "acre", "are": "are"})
    out = size.copy()
    out[unit == "m2"] = size[unit == "m2"] / 10000.0
    out[unit == "acre"] = size[unit == "acre"] * 0.404686
    out[unit == "are"] = size[unit == "are"] * 0.01
    return out


def parse_dates(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    serial = pd.to_numeric(s, errors="coerce")
    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
    excel_mask = serial.between(40000, 60000)
    dt.loc[excel_mask] = pd.to_datetime("1899-12-30") + pd.to_timedelta(serial.loc[excel_mask], unit="D")
    return dt


def expected_season(month: int) -> str:
    if month in [9, 10, 11, 12, 1]:
        return "A"
    if month in [2, 3, 4, 5, 6]:
        return "B"
    return "C"


def clean_q1(df_raw: pd.DataFrame, clog) -> pd.DataFrame:
    df = standardize_text(df_raw)
    before_shape = df.shape

    for col in ["altitude_m", "fertilizer_kg", "rainfall_mm", "avg_temp_c", "soil_ph", "farmer_age", "harvest_weight_kg", "yield_kg_per_ha"]:
        df[col] = parse_number(df[col])

    df["farm_size_ha"] = convert_farm_size_ha(df)
    df["planting_dt"] = parse_dates(df["planting_date"])
    df["year"] = df["planting_dt"].dt.year

    season_from_date = df["planting_dt"].dt.month.map(lambda m: expected_season(m) if pd.notna(m) else np.nan)
    season_conflict = (df["season"].isin(["A", "B", "C"])) & season_from_date.notna() & (df["season"] != season_from_date)
    n_conflict = int(season_conflict.sum())
    df.loc[season_conflict, "season"] = season_from_date[season_conflict]
    clog.add("season_fix", "season,planting_date", "align season with planting date month", n_conflict, before_shape, df.shape, "ensures one consistent season label")

    # Date range filter
    bad_date = (df["year"].notna()) & (~df["year"].between(2023, 2025))
    n_bad_date = int(bad_date.sum())
    df.loc[bad_date, ["planting_dt", "year"]] = np.nan
    clog.add("date_range", "planting_date", "outside 2023-2025 set to missing", n_bad_date, before_shape, df.shape, "assignment period constraint")

    # Duplicates
    n0 = len(df)
    df = df.drop_duplicates()
    n1 = len(df)
    clog.add("drop_exact_duplicates", "all", "remove exact duplicate rows", n0 - n1, n0, n1, "duplicate submissions")

    # Near duplicates: farm+season+year, keep most complete
    df["_completeness"] = df.notna().sum(axis=1)
    n_before = len(df)
    df = df.sort_values("_completeness", ascending=False).drop_duplicates(subset=["farm_id", "season", "year"], keep="first")
    n_after = len(df)
    df = df.drop(columns=["_completeness"])
    clog.add("dedupe_near", "farm_id,season,year", "keep most complete record", n_before - n_after, n_before, n_after, "resolve near-duplicate farm-season-year entries")

    # Impossible value handling
    rules = {
        "yield_kg_per_ha": lambda s: s <= 0,
        "farm_size_ha": lambda s: s <= 0,
        "fertilizer_kg": lambda s: s < 0,
        "rainfall_mm": lambda s: (s < 0) | (s > 5000),
        "avg_temp_c": lambda s: (s < 0) | (s > 60),
        "altitude_m": lambda s: (s < 500) | (s > 3500),
        "soil_ph": lambda s: (s < 4) | (s > 8),
        "farmer_age": lambda s: (s < 18) | (s > 100),
    }
    for col, fn in rules.items():
        bad = fn(df[col]) & df[col].notna()
        n_bad = int(bad.sum())
        df.loc[bad, col] = np.nan
        clog.add("set_invalid_nan", col, "apply agronomic plausibility rule", n_bad, "valid+invalid", "invalid->NaN", "protect data quality before imputation")

    # correct obvious temp typo (e.g. 250 -> 25.0)
    typo_temp = (df["avg_temp_c"] > 80) & (df["avg_temp_c"] < 400)
    n_typo = int(typo_temp.sum())
    df.loc[typo_temp, "avg_temp_c"] = df.loc[typo_temp, "avg_temp_c"] / 10
    clog.add("fix_temp_scale", "avg_temp_c", "divide by 10 for likely decimal shift", n_typo, "e.g.250", "25.0", "common data-entry typo")

    # Recompute yield using harvest and farm size when both are available and mismatch >10%
    recomputed = df["harvest_weight_kg"] / df["farm_size_ha"]
    mismatch = df[TARGET_COL].notna() & recomputed.notna() & ((df[TARGET_COL] - recomputed).abs() / recomputed.abs().clip(lower=1) > 0.1)
    n_mismatch = int(mismatch.sum())
    df.loc[mismatch, TARGET_COL] = recomputed[mismatch]
    clog.add("recompute_yield", "yield_kg_per_ha", "replace mismatched target with harvest/size", n_mismatch, "reported", "recomputed", "physical consistency of target")

    # Drop rows with missing target
    n_before = len(df)
    df = df[df[TARGET_COL].notna()]
    n_after = len(df)
    clog.add("drop_missing_target", TARGET_COL, "drop unusable target rows", n_before - n_after, n_before, n_after, "supervised dataset requires target")

    # Winsorize a few skewed numerics
    for col in ["fertilizer_kg", "rainfall_mm", "yield_kg_per_ha"]:
        s = df[col]
        lo, hi = s.quantile([0.01, 0.99])
        clipped = s.clip(lo, hi)
        n_clip = int((s != clipped).sum())
        df[col] = clipped
        clog.add("winsorize", col, "clip at 1st/99th percentiles", n_clip, f"[{s.min():.2f},{s.max():.2f}]", f"[{df[col].min():.2f},{df[col].max():.2f}]", "cap likely entry-error extremes while keeping records")

    return df.reset_index(drop=True)


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["planting_month"] = out["planting_dt"].dt.month
    out["planting_quarter"] = out["planting_dt"].dt.quarter
    start_month = out["season"].str.lower().map(SEASON_START_MONTH)
    start_dt = pd.to_datetime(dict(year=out["year"].fillna(2024).astype(int), month=start_month.fillna(1).astype(int), day=1), errors="coerce")
    out["days_from_season_start"] = (out["planting_dt"] - start_dt).dt.days
    return out
