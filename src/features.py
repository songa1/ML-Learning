import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression, VarianceThreshold
from sklearn.ensemble import RandomForestRegressor
from .config import SEED


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["fertilizer_kg_per_ha"] = out["fertilizer_kg"] / out["farm_size_ha"].replace(0, np.nan)
    out["is_improved_seed"] = out["seed_variety"].isin(["Improved", "Hybrid"]).astype(int)
    out["seed_rank"] = out["seed_variety"].map({"Local": 0, "Improved": 1, "Hybrid": 2})
    out["altitude_band"] = pd.cut(out["altitude_m"], bins=[-np.inf, 1400, 2000, np.inf], labels=["lowland", "mid", "highland"])
    t = out["avg_temp_c"]
    out["temp_deviation_from_optimum"] = np.where(t < 18, 18 - t, np.where(t > 27, t - 27, 0))
    out["rain_per_temp"] = out["rainfall_mm"] / (out["avg_temp_c"].replace(0, np.nan))
    out["rainfall_log"] = np.log1p(out["rainfall_mm"].clip(lower=0))
    out["fertilizer_log1p"] = np.log1p(out["fertilizer_kg"].clip(lower=0))
    out["farm_size_log"] = np.log1p(out["farm_size_ha"].clip(lower=0))
    out["irrigated_flag"] = out["irrigation"].eq("Yes").astype(int)
    out["season_x_irrigation"] = out["season"].astype(str) + "_" + out["irrigation"].astype(str)
    return out


def remove_high_corr(df: pd.DataFrame, threshold=0.9):
    num = df.select_dtypes(include=["number"])
    corr = num.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    drop_cols = [c for c in upper.columns if any(upper[c] > threshold)]
    return df.drop(columns=drop_cols, errors="ignore"), drop_cols


def select_features_numeric(X_num: pd.DataFrame, y: pd.Series, k=15):
    vt = VarianceThreshold(threshold=0.0)
    X_vt = vt.fit_transform(X_num.fillna(X_num.median()))
    kept = X_num.columns[vt.get_support()]
    k = min(k, len(kept)) if len(kept) else 0
    if k == 0:
        return list(kept), []
    skb = SelectKBest(score_func=f_regression, k=k)
    skb.fit(X_num[kept].fillna(X_num[kept].median()), y)
    selected = list(kept[skb.get_support()])
    return list(kept), selected


def rf_importance(X: pd.DataFrame, y: pd.Series):
    x_num = X.select_dtypes(include=["number"]).fillna(0)
    if x_num.shape[1] == 0:
        return pd.DataFrame(columns=["feature", "importance"])
    rf = RandomForestRegressor(n_estimators=200, random_state=SEED)
    rf.fit(x_num, y)
    imp = pd.DataFrame({"feature": x_num.columns, "importance": rf.feature_importances_}).sort_values("importance", ascending=False)
    return imp
