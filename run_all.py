from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
NBS = [ROOT / "q1_maize_yield/notebooks/q1_maize_yield_workflow.ipynb"]

for nb in NBS:
    print(f"Executing {nb.name} ...")
    subprocess.run([
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(nb)
    ], check=True, cwd=ROOT)

print("Running verification ...")
subprocess.run([sys.executable, "tools/verify.py"], check=True, cwd=ROOT)
print("All notebooks and verification completed successfully.")
