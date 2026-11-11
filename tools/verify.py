from pathlib import Path
import hashlib
import sys
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import PROCESSED_DIR, TARGET_COL


def fhash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    train = pd.read_csv(PROCESSED_DIR / "train_model_ready.csv")
    val = pd.read_csv(PROCESSED_DIR / "validation_model_ready.csv")
    test = pd.read_csv(PROCESSED_DIR / "test_model_ready.csv")

    for df, name in [(train, "train"), (val, "val"), (test, "test")]:
        assert_true(TARGET_COL in df.columns, f"{name} missing target")
        assert_true(df.columns.tolist() == train.columns.tolist(), f"{name} columns mismatch")

    # no leakage columns
    leak_cols = [c for c in train.columns if "harvest_weight" in c]
    assert_true(len(leak_cols) == 0, "Leakage columns detected")

    # check NaNs (allow in raw id columns only not expected here)
    for df, name in [(train, "train"), (val, "val"), (test, "test")]:
        assert_true(df.drop(columns=["farm_id"], errors="ignore").isna().sum().sum() == 0, f"NaN found in {name}")

    # disjoint farm_id
    if "farm_id" in train.columns:
        tr, va, te = set(train["farm_id"].astype(str)), set(val["farm_id"].astype(str)), set(test["farm_id"].astype(str))
        assert_true(len(tr & va) == 0 and len(tr & te) == 0 and len(va & te) == 0, "farm_id overlap across splits")

    # train scaling mean approx zero for numeric transformed features
    num_cols = [c for c in train.columns if c.startswith("num__")]
    if num_cols:
        mean_abs = train[num_cols].mean().abs().mean()
        assert_true(mean_abs < 0.25, f"Scaled train numeric means too far from 0 ({mean_abs:.3f})")

    hashes = {
        "train_model_ready.csv": fhash(PROCESSED_DIR / "train_model_ready.csv"),
        "validation_model_ready.csv": fhash(PROCESSED_DIR / "validation_model_ready.csv"),
        "test_model_ready.csv": fhash(PROCESSED_DIR / "test_model_ready.csv"),
    }
    manifest = PROCESSED_DIR / "hash_manifest.txt"
    if manifest.exists():
        old = dict(line.strip().split(",", 1) for line in manifest.read_text().splitlines() if line.strip())
        for k, v in hashes.items():
            assert_true(old.get(k) == v, f"Non-deterministic output hash for {k}")
    manifest.write_text("\n".join([f"{k},{v}" for k, v in hashes.items()]))

    print("Verification checks passed.")


if __name__ == "__main__":
    main()
