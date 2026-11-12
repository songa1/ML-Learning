from pathlib import Path
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.q2_config import (  # noqa: E402
    INTERIM_DIR,
    KEY_COLUMNS,
    LEAKAGE_COLUMNS,
    PROCESSED_DIR,
    RAW_FILE,
    TARGET,
)


def main():
    notebook = RAW_FILE.parents[2] / "notebooks" / "q2_student_pathways_workflow.ipynb"
    assert notebook.exists(), "Q2 combined notebook is missing"
    document = json.loads(notebook.read_text())
    assert document["cells"][0]["cell_type"] == "markdown"
    assert "alevel_avg_pct_2023_24" in "".join(document["cells"][0]["source"])

    outputs = [PROCESSED_DIR / f"q2_{name}_model_ready.csv" for name in ["train", "validation", "test"]]
    if not all(path.exists() for path in outputs):
        print("Q2 notebook structure verified; model-ready outputs are not present until run_q2.py executes.")
        return

    frames = [pd.read_csv(path) for path in outputs]
    assert all(not set(LEAKAGE_COLUMNS).intersection(frame.columns) for frame in frames)
    assert all(set(KEY_COLUMNS).issubset(frame.columns) for frame in frames)
    assert frames[0].columns.tolist() == frames[1].columns.tolist() == frames[2].columns.tolist()
    assert all(not frame.isna().any().any() for frame in frames)
    assert all(frame[TARGET].between(0, 100).all() for frame in frames)
    assert all(set(frame["high_performer"].unique()) <= {0, 1} for frame in frames)

    cleaned = pd.read_csv(INTERIM_DIR / "q2_clean.csv")
    assert sum(len(frame) for frame in frames) == len(cleaned), "splits do not cover the cleaned table"
    assert not cleaned.duplicated(["school_code", "combination_code"]).any()

    print("Q2 verification passed:", [frame.shape for frame in frames])


if __name__ == "__main__":
    main()
