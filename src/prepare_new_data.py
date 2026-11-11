import pandas as pd
from src.cleaning import clean_q1, add_time_features
from src.features import engineer_features
from src.logging_utils import CleaningLog

def prepare_new_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    clog = CleaningLog()
    clean = clean_q1(df_raw.copy(), clog)
    clean = add_time_features(clean)
    clean = engineer_features(clean)
    return clean
