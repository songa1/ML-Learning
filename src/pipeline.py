import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from .config import SEED, TARGET_COL, LEAKAGE_COLS


def split_train_val_test(df: pd.DataFrame):
    train_df, tmp_df = train_test_split(df, test_size=0.30, random_state=SEED, stratify=df["season"])
    val_df, test_df = train_test_split(tmp_df, test_size=0.50, random_state=SEED, stratify=tmp_df["season"])
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)


def build_preprocessor(train_df: pd.DataFrame):
    feature_cols = [c for c in train_df.columns if c not in [TARGET_COL] + LEAKAGE_COLS + ["yield_t_ha", "record_id"]]
    X_train = train_df[feature_cols].copy()

    numeric_cols = list(X_train.select_dtypes(include=["number"]).columns)
    ordinal_cols = [c for c in ["pest_incidence"] if c in X_train.columns]
    cat_cols = [c for c in X_train.columns if c not in numeric_cols + ordinal_cols]

    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    ord_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ord", OrdinalEncoder(categories=[["Low", "Medium", "High"]], handle_unknown="use_encoded_value", unknown_value=-1)),
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    pre = ColumnTransformer([
        ("num", num_pipe, numeric_cols),
        ("ord", ord_pipe, ordinal_cols),
        ("cat", cat_pipe, cat_cols),
    ], remainder="drop")

    pre.fit(X_train)
    return pre, feature_cols


def transform_split(preprocessor, df: pd.DataFrame, feature_cols):
    X = df[feature_cols].copy()
    X_t = preprocessor.transform(X)
    if hasattr(X_t, "toarray"):
        X_t = X_t.toarray()
    names = preprocessor.get_feature_names_out()
    X_df = pd.DataFrame(X_t, columns=names, index=df.index)
    return X_df


def add_low_yield_label(train_df, val_df, test_df):
    q20 = train_df[TARGET_COL].quantile(0.20)
    for d in [train_df, val_df, test_df]:
        d["low_yield_risk"] = (d[TARGET_COL] < q20).astype(int)
    return q20
