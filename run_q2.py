from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = [ROOT / "q2_own_scenario" / "notebooks" / "q2_student_pathways_workflow.ipynb"]

if not NOTEBOOKS:
    raise SystemExit("No Q2 notebooks found. Run tools/build_q2_notebooks.py first.")

for notebook in NOTEBOOKS:
    print(f"Executing {notebook.name} ...")
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", str(notebook)], check=True, cwd=ROOT)

subprocess.run([sys.executable, "tools/verify_q2.py"], check=True, cwd=ROOT)
print("Q2 notebooks and verification completed successfully.")