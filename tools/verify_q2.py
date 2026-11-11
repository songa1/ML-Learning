from pathlib import Path
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.q2_config import LEAKAGE_COLUMNS, PROCESSED_DIR, RAW_FILE


def main():
    notebooks = sorted((RAW_FILE.parents[2] / "notebooks").glob("0*.ipynb"))
    assert len(notebooks) == 6, "Q2 requires six notebooks"
    for path in notebooks:
        document = json.loads(path.read_text())
        assert document["cells"][0]["cell_type"] == "markdown"
        assert document["cells"][0]["metadata"]["language"] == "markdown"

    outputs = [PROCESSED_DIR / f"q2_{name}_model_ready.csv" for name in ["train", "validation", "test"]]
    if not all(path.exists() for path in outputs):
        print("Q2 notebook structure verified; model-ready outputs are not present until run_q2.py executes.")
        return
    frames = [pd.read_csv(path) for path in outputs]
    assert all(not set(LEAKAGE_COLUMNS).intersection(frame.columns) for frame in frames)
    assert frames[0].columns.tolist() == frames[1].columns.tolist() == frames[2].columns.tolist()
    assert all(not frame.isna().any().any() for frame in frames)
    print("Q2 verification passed:", [frame.shape for frame in frames])


if __name__ == "__main__":
    main()