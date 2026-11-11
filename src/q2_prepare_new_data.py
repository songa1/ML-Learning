import joblib

from .q2_config import PROCESSED_DIR
from .q2_pipeline import add_features, clean_raw, transform


def prepare_new_data(raw_frame):
    """Apply the saved Q2 cleaning, feature, and train-fitted transform to new raw rows."""
    transformer = joblib.load(PROCESSED_DIR / "q2_preprocessor.joblib")
    prepared = add_features(clean_raw(raw_frame))
    feature_columns = list(transformer.feature_names_in_)
    return transform(transformer, prepared, feature_columns)