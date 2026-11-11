from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .q2_config import ID_COLUMNS, LEAKAGE_COLUMNS, SEED, TARGET


MISSING = {"", " ", "n/a", "na", "unknown", "?", "null", "none", "-1"}


def load_raw(path):
    return pd.read_csv(path, dtype=str)


def clean_raw(raw):
    frame = raw.copy()
    for column in frame.columns:
        frame[column] = frame[column].map(lambda value: value.strip() if isinstance(value, str) else value)
    for column in frame.select_dtypes(include="object").columns:
        frame[column] = frame[column].map(
            lambda value: np.nan if isinstance(value, str) and value.lower() in MISSING else value
        )

    category_maps = {
        "gender": {"female": "Female", "male": "Male"},
        "school_type": {"public": "public", "government-aided": "government-aided", "private": "private"},
        "boarding_day": {"boarding": "Boarding", "day": "Day"},
        "scholarship_flag": {"yes": "Yes", "no": "No"},
        "science_lab": {"yes": "Yes", "no": "No"},
        "ict_lab": {"yes": "Yes", "no": "No"},
        "library": {"yes": "Yes", "no": "No"},
        "combination": {"mpc": "MPC", "pcb": "PCB", "mcb": "MCB", "meg": "MEG", "heg": "HEG", "hel": "HEL", "leg": "LEG", "tvet": "TVET"},
        "province": {"kigali city": "Kigali City", "southern": "Southern", "northern": "Northern", "western": "Western"},
    }
    for column, mapping in category_maps.items():
        if column in frame:
            frame[column] = frame[column].map(lambda value: mapping.get(str(value).lower(), value) if pd.notna(value) else value)
    if "district" in frame:
        frame["district"] = frame["district"].map(lambda value: str(value).title() if pd.notna(value) else value)
    if "school_name" in frame:
        frame["school_name"] = frame["school_name"].map(lambda value: str(value).strip().title() if pd.notna(value) else value)

    numeric_columns = [
        "age", "s3_aggregate", "math_grade", "english_grade", "science_grade", "school_size",
        "student_teacher_ratio", "tuition_fee", "boarding_fee", "distance_km",
        "previous_year_pass_rate", TARGET, *LEAKAGE_COLUMNS[:1],
    ]
    for column in numeric_columns:
        if column in frame:
            frame[column] = pd.to_numeric(frame[column].astype(str).str.replace(",", "", regex=False).str.extract(r"([-+]?\d*\.?\d+)")[0], errors="coerce")
    valid_ranges = {"age": (15, 25), "s3_aggregate": (1, 100), "distance_km": (0.1, 200), "tuition_fee": (0, 2000000), "boarding_fee": (0, 2000000), TARGET: (0, 100)}
    for column, (low, high) in valid_ranges.items():
        if column in frame:
            frame.loc[~frame[column].between(low, high), column] = np.nan

    frame = frame.drop_duplicates()
    if "student_record_id" in frame:
        frame = frame.sort_values("student_record_id").drop_duplicates("student_record_id", keep="first")
    frame = frame.dropna(subset=[TARGET, "student_record_id"]).reset_index(drop=True)
    return frame


def add_features(frame):
    data = frame.copy()
    data["fee_total"] = data["tuition_fee"].fillna(0) + data["boarding_fee"].fillna(0)
    data["is_boarding"] = data["boarding_day"].eq("Boarding").astype(int)
    data["science_facility_count"] = data[["science_lab", "ict_lab", "library"]].eq("Yes").sum(axis=1)
    data["academic_readiness"] = data[["math_grade", "english_grade", "science_grade"]].mean(axis=1)
    data["fee_per_school_place"] = data["fee_total"] / data["school_size"].replace(0, np.nan)
    data["distance_log1p"] = np.log1p(data["distance_km"])
    data["pass_rate_band"] = pd.cut(data["previous_year_pass_rate"], bins=[-np.inf, 0.5, 0.75, np.inf], labels=["lower", "middle", "higher"])
    return data


def split_data(frame):
    train, temporary = train_test_split(frame, test_size=0.30, random_state=SEED, stratify=frame["combination"])
    validation, test = train_test_split(temporary, test_size=0.50, random_state=SEED, stratify=temporary["combination"])
    return train.reset_index(drop=True), validation.reset_index(drop=True), test.reset_index(drop=True)


def build_preprocessor(train):
    excluded = set(ID_COLUMNS + LEAKAGE_COLUMNS + [TARGET])
    feature_columns = [column for column in train.columns if column not in excluded]
    numeric = train[feature_columns].select_dtypes(include=np.number).columns.tolist()
    categorical = [column for column in feature_columns if column not in numeric]
    numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    transformer = ColumnTransformer([("numeric", numeric_pipe, numeric), ("categorical", categorical_pipe, categorical)], remainder="drop")
    transformer.fit(train[feature_columns])
    return transformer, feature_columns


def transform(transformer, frame, feature_columns):
    values = transformer.transform(frame[feature_columns])
    names = transformer.get_feature_names_out()
    return pd.DataFrame(values, columns=names, index=frame.index)


def prepare_dataset(raw):
    cleaned = add_features(clean_raw(raw))
    train, validation, test = split_data(cleaned)
    transformer, feature_columns = build_preprocessor(train)
    encoded = {"train": transform(transformer, train, feature_columns), "validation": transform(transformer, validation, feature_columns), "test": transform(transformer, test, feature_columns)}
    labels = {name: data[[TARGET]].reset_index(drop=True) for name, data in {"train": train, "validation": validation, "test": test}.items()}
    threshold = train[TARGET].quantile(1 / 3)
    for name, data in {"train": train, "validation": validation, "test": test}.items():
        labels[name]["high_performer"] = (data[TARGET].to_numpy() >= threshold).astype(int)
    return cleaned, train, validation, test, encoded, labels, transformer
