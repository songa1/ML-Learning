"""Preparation pipeline for the Q2 school/combination option dataset.

The unit of analysis is one school x subject-combination offer in the 2023/24
NESA A-level results. The pipeline is deliberately split into small functions so
the notebook can show each decision separately and the raw extract is never edited.
"""

import re

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .q2_config import (
    DISTRICT_TO_PROVINCE,
    ID_COLUMNS,
    KEY_COLUMNS,
    LEAKAGE_COLUMNS,
    SCHOOL_CATEGORY_MAP,
    SEED,
    TARGET,
    WDA_STATUS_MAP,
)

MISSING = {"", " ", "n/a", "na", "unknown", "?", "null", "none", "-1"}

NUMERIC_COLUMNS = [
    "alevel_avg_pct_2023_24",
    "alevel_rank_in_category",
    "alevel_n_schools_in_category",
    "olevel_avg_pct_2023_24",
    "olevel_rank_national",
    "olevel_n_schools_ranked",
    "wda_n_accredited_trades",
    "wda_match_score",
]

VALID_RANGES = {
    "alevel_avg_pct_2023_24": (0, 100),
    "olevel_avg_pct_2023_24": (0, 100),
    "alevel_rank_in_category": (1, np.inf),
    "olevel_rank_national": (1, np.inf),
    "wda_n_accredited_trades": (0, np.inf),
}


def load_raw(path):
    """Read the raw CSV as text so codes keep leading zeros and quality issues stay visible."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _log(log, step, columns, rule, n_affected, before, after, justification):
    if log is not None:
        log.add(step, columns, rule, n_affected, before, after, justification)


def _to_number(series):
    text = series.astype(str).str.replace(",", "", regex=False)
    text = text.str.extract(r"([-+]?\d*\.?\d+)")[0]
    return pd.to_numeric(text, errors="coerce")


def clean_raw(raw, log=None):
    """Apply documented cleaning rules and return a typed analysis table.

    Rules are logged (when a CleaningLog is supplied) and are limited to fixing
    representation, ranges, duplicates, and unusable target rows. Missing O-level
    or WDA records are intentionally preserved so their information is not lost.
    """
    frame = raw.copy()
    before_shape = frame.shape

    # 1. Whitespace only. Keeps original casing, which protects acronyms in school names.
    changed = 0
    for column in frame.columns:
        original = frame[column]
        stripped = original.map(lambda value: value.strip() if isinstance(value, str) else value)
        changed += int((stripped != original).sum())
        frame[column] = stripped
    _log(log, "strip_whitespace", "all text columns", "trim leading and trailing spaces",
         changed, before_shape, frame.shape, "avoid false label variants caused by stray spaces")

    # 2. Collapse repeated internal spaces in the school name and normalise district casing.
    name_changes = 0
    if "school_name" in frame:
        cleaned_names = frame["school_name"].map(
            lambda value: re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else value
        )
        name_changes = int((cleaned_names != frame["school_name"]).sum())
        frame["school_name"] = cleaned_names
    if "district" in frame:
        frame["district"] = frame["district"].map(
            lambda value: value.strip().title() if isinstance(value, str) and value.strip() else value
        )
    _log(log, "normalise_names", "school_name,district", "collapse internal spaces; title-case district",
         name_changes, before_shape, frame.shape, "one consistent label per school and district")

    # 3. Convert placeholders to missing values.
    missing_before = int(frame.isna().sum().sum())
    for column in frame.select_dtypes(include="object").columns:
        frame[column] = frame[column].map(
            lambda value: np.nan if isinstance(value, str) and value.strip().lower() in MISSING else value
        )
    _log(log, "set_missing_tokens", "all text columns", "empty and placeholder text -> missing",
         int(frame.isna().sum().sum()) - missing_before, before_shape, frame.shape,
         "distinguish genuinely absent values from text placeholders")

    # 4. Parse numeric fields; the target is a percentage, ranks and counts are integers.
    parse_changes = 0
    for column in NUMERIC_COLUMNS:
        if column in frame:
            direct = pd.to_numeric(frame[column], errors="coerce")
            parse_changes += int((frame[column].notna() & direct.isna()).sum())
            frame[column] = _to_number(frame[column])
    _log(log, "parse_numeric", ",".join(NUMERIC_COLUMNS), "extract numbers from text",
         parse_changes, before_shape, frame.shape, "allow arithmetic and range checks")

    # 5. Implausible values become missing rather than silently entering the model.
    for column, (low, high) in VALID_RANGES.items():
        if column in frame:
            invalid = frame[column].notna() & ~frame[column].between(low, high)
            frame.loc[invalid, column] = np.nan
            _log(log, "invalid_range", column, f"values outside [{low}, {high}] -> missing",
                 int(invalid.sum()), before_shape, frame.shape,
                 "remove impossible percentages, ranks, or counts")

    # 6. Canonicalise the WDA ownership spellings (13 raw variants -> 2 labels).
    if "wda_status" in frame:
        raw_status = frame["wda_status"].copy()
        frame["wda_status"] = frame["wda_status"].map(
            lambda value: WDA_STATUS_MAP.get(value.strip().lower(), value) if isinstance(value, str) else value
        )
        status_changes = int((frame["wda_status"].fillna("") != raw_status.fillna("")).sum())
        _log(log, "normalize_wda_status", "wda_status", "map ownership spellings to Public/Private",
             status_changes, before_shape, frame.shape, "one label per ownership meaning")

    # 7. Canonical programme and school labels.
    label_changes = 0
    if "gender_intake" in frame:
        before = frame["gender_intake"].copy()
        frame["gender_intake"] = frame["gender_intake"].map(
            lambda value: {"MIXED": "Mixed", "FEMALE": "Female", "MALE": "Male"}.get(value, value)
            if isinstance(value, str) else value
        )
        label_changes += int((frame["gender_intake"].fillna("") != before.fillna("")).sum())
    if "school_category" in frame:
        before = frame["school_category"].copy()
        frame["school_category"] = frame["school_category"].map(
            lambda value: SCHOOL_CATEGORY_MAP.get(value, value) if isinstance(value, str) else value
        )
        label_changes += int((frame["school_category"].fillna("") != before.fillna("")).sum())
    _log(log, "normalize_labels", "gender_intake,school_category", "map source labels to readable categories",
         label_changes, before_shape, frame.shape, "consistent categories for encoding and reporting")

    # 8. Duplicates. Exact duplicates are a data-entry problem; school_code + combination_code
    #    is the natural key of an offer row.
    n_before = len(frame)
    frame = frame.drop_duplicates()
    _log(log, "drop_exact_duplicates", "all columns", "remove identical rows",
         n_before - len(frame), n_before, len(frame), "duplicate extracts inflate the same offer")

    n_before = len(frame)
    frame = frame.sort_values(["school_code", "combination_code"]).drop_duplicates(
        ["school_code", "combination_code"], keep="first"
    )
    _log(log, "dedupe_offer_key", "school_code,combination_code", "keep one row per school x combination",
         n_before - len(frame), n_before, len(frame), "the unit of analysis is one offer")

    # 9. A supervised dataset needs the outcome; the 53 unmatched offers cannot train a model.
    n_before = len(frame)
    frame = frame.dropna(subset=[TARGET, "school_code", "combination_code"])
    _log(log, "drop_missing_target", f"{TARGET},school_code,combination_code",
         "drop rows without a usable target or key", n_before - len(frame),
         n_before, len(frame), "no outcome means the record cannot be supervised")

    frame = frame.reset_index(drop=True)
    return frame


def add_features(frame):
    """Create decision-time features and remove columns that are constant or unusable."""
    data = frame.copy()

    data["province"] = data["district"].map(DISTRICT_TO_PROVINCE)

    # Missing O-level information is structural: TTCs and many TVET schools are not
    # in the O-level ranking table. The flag preserves that signal instead of hiding it.
    data["has_olevel_record"] = data["olevel_avg_pct_2023_24"].notna().astype(int)
    data["olevel_rank_pct"] = (
        data["olevel_rank_national"] / data["olevel_n_schools_ranked"].replace(0, np.nan)
    )

    data["has_wda_record"] = data["wda_sn"].notna().astype(int)
    data["wda_n_accredited_trades"] = data["wda_n_accredited_trades"].fillna(0)
    data["wda_ownership"] = data["wda_status"].fillna("Not listed")

    # Programme breadth: a school offering many combinations is a different option
    # from a single-track school. Computed from the offers table, not from outcomes.
    data["n_combinations_at_school"] = data.groupby("school_code")["combination_code"].transform("nunique")

    # Used only to derive olevel_rank_pct; it is the same 1,871 for every row.
    data = data.drop(columns=["olevel_n_schools_ranked"])
    return data


def _stratum(frame, min_count=15):
    """Keep stratification stable by pooling rank categories with very few offers."""
    counts = frame["ranking_category"].value_counts()
    rare = counts[counts < min_count].index
    return frame["ranking_category"].where(~frame["ranking_category"].isin(rare), "OTHER_RARE")


def split_data(frame):
    """70/15/15 split, stratified on programme family so each split keeps the mix."""
    stratum = _stratum(frame)
    train, temporary = train_test_split(
        frame, test_size=0.30, random_state=SEED, stratify=stratum
    )
    temporary_stratum = _stratum(temporary)
    validation, test = train_test_split(
        temporary, test_size=0.50, random_state=SEED, stratify=temporary_stratum
    )
    return train.reset_index(drop=True), validation.reset_index(drop=True), test.reset_index(drop=True)


def build_preprocessor(train):
    """Fit imputers, scaler, and one-hot encoder on the training split only."""
    excluded = set(ID_COLUMNS + LEAKAGE_COLUMNS + [TARGET])
    feature_columns = [column for column in train.columns if column not in excluded]
    numeric = train[feature_columns].select_dtypes(include=np.number).columns.tolist()
    categorical = [column for column in feature_columns if column not in numeric]

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    transformer = ColumnTransformer([
        ("numeric", numeric_pipe, numeric),
        ("categorical", categorical_pipe, categorical),
    ], remainder="drop")
    transformer.fit(train[feature_columns])
    return transformer, feature_columns


def transform(transformer, frame, feature_columns):
    values = transformer.transform(frame[feature_columns])
    names = transformer.get_feature_names_out()
    return pd.DataFrame(values, columns=names, index=frame.index)


def prepare_dataset(raw):
    """Clean, feature-engineer, split, encode, and label the Q2 offers.

    Returns the cleaned table, the three unscaled splits, the encoded splits
    (identifiers + model inputs), labels, and the fitted transformer.
    """
    cleaned = add_features(clean_raw(raw))
    train, validation, test = split_data(cleaned)
    transformer, feature_columns = build_preprocessor(train)

    frames = {"train": train, "validation": validation, "test": test}
    encoded = {}
    for name, frame in frames.items():
        values = transform(transformer, frame, feature_columns).reset_index(drop=True)
        keys = frame[KEY_COLUMNS].reset_index(drop=True)
        encoded[name] = pd.concat([keys, values], axis=1)

    threshold = train[TARGET].quantile(2 / 3)
    labels = {}
    for name, frame in frames.items():
        labels[name] = pd.DataFrame({
            TARGET: frame[TARGET].to_numpy(),
            "high_performer": (frame[TARGET].to_numpy() >= threshold).astype(int),
        })

    return cleaned, train, validation, test, encoded, labels, transformer
