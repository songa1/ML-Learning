from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
NBS = [
    ROOT / "q1_maize_yield/notebooks/00_environment_test.ipynb",
    ROOT / "q1_maize_yield/notebooks/01_acquire.ipynb",
    ROOT / "q1_maize_yield/notebooks/02_eda.ipynb",
    ROOT / "q1_maize_yield/notebooks/03_clean.ipynb",
    ROOT / "q1_maize_yield/notebooks/04_features.ipynb",
    ROOT / "q1_maize_yield/notebooks/05_finalise.ipynb",
]

for nb in NBS:
    print(f"Executing {nb.name} ...")
    subprocess.run([
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(nb)
    ], check=True, cwd=ROOT)

print("Running verification ...")
subprocess.run([sys.executable, "tools/verify.py"], check=True, cwd=ROOT)
print("All notebooks and verification completed successfully.")
