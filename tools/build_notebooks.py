from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "q1_maize_yield" / "notebooks"
NB_DIR.mkdir(parents=True, exist_ok=True)

BOOT = """import sys
from pathlib import Path
ROOT = Path.cwd()
while not (ROOT / 'src').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
"""


def write(name, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    (NB_DIR / name).write_text(nbf.writes(nb))


write("00_environment_test.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 1: environment test"),
    nbf.v4.new_code_cell(BOOT + """
import platform, pandas as pd, numpy as np, sklearn, joblib
print('Python:', platform.python_version())
print('pandas:', pd.__version__, 'numpy:', np.__version__, 'scikit-learn:', sklearn.__version__, 'joblib:', joblib.__version__)
"""),
])

write("01_acquire.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 2: requirements and acquisition"),
    nbf.v4.new_markdown_cell("This notebook documents the revised Rwanda maize source. The raw file is preserved unchanged; the cleaning stage derives model fields and converts tonnes/ha to kg/ha."),
    nbf.v4.new_code_cell(BOOT + """
from datetime import date
import pandas as pd
from src.config import RAW_FILE, DOCS_DIR, COLUMNS
from src.cleaning import sha256_file, to_string_df

DOCS_DIR.mkdir(parents=True, exist_ok=True)
if not RAW_FILE.exists():
    raise FileNotFoundError(f'Revised Q1 raw file not found: {RAW_FILE}')
df_raw = to_string_df(RAW_FILE)
print('Using file:', RAW_FILE)
print('SHA-256:', sha256_file(RAW_FILE))
print('shape:', df_raw.shape)
display(df_raw.head())
display(df_raw.dtypes.rename('dtype').to_frame())

meta = {
 'record_id': ('Observation identifier','string','unique record code','No'),
 'year': ('Observation year','integer','2015-2030','No'),
 'season': ('Cropping season','category','A/B/C','No'),
 'province': ('Province','category','Rwanda province','No'),
 'district': ('District','category','Rwanda district','No'),
 'altitude_m': ('Altitude','numeric','metres','No'),
 'rainfall_mm': ('Rainfall','numeric','millimetres','No'),
 'avg_temp_c': ('Average temperature','numeric','degrees Celsius','No'),
 'soil_ph': ('Soil acidity','numeric','pH','No'),
 'soil_type': ('Soil category','category','soil class','No'),
 'seed_variety': ('Seed variety','category','variety label','No'),
 'farming_practice': ('Farming practice','category','Traditional/Improved','No'),
 'npk_kg_ha': ('NPK fertiliser','numeric','kg/ha','No'),
 'urea_kg_ha': ('Urea fertiliser','numeric','kg/ha','No'),
 'manure_t_ha': ('Manure','numeric','tonnes/ha','No'),
 'plant_density_per_ha': ('Plant density','numeric','plants/ha','No'),
 'farm_area_ha': ('Farm area','numeric','hectares','No'),
 'irrigation': ('Irrigation','category','Yes/No','No'),
 'pest_incidence_index': ('Pest incidence index','numeric','0-1 index','No'),
 'yield_t_ha': ('Yield target','numeric','tonnes/ha; converted to kg/ha','Yes'),
}
dd = pd.DataFrame([{'column_name': c, 'meaning': meta.get(c, ('','','',''))[0],
                    'data_type': meta.get(c, ('','','',''))[1],
                    'unit': meta.get(c, ('','','',''))[2],
                    'post_harvest_or_target': meta.get(c, ('','','',''))[3]} for c in COLUMNS])
dd.to_csv(DOCS_DIR / 'data_dictionary.csv', index=False)
(DOCS_DIR / 'data_dictionary.md').write_text('# Q1 Data Dictionary\\n\\n' + dd.to_string(index=False))
(DOCS_DIR / 'data_requirements.md').write_text('''# Q1 Data Requirements

- Target: `yield_t_ha`, converted to `yield_kg_per_ha` for modelling.
- Pre-harvest predictors: weather, altitude, soil, seed, farming practice, fertiliser, density, area, irrigation and pest index.
- The revised file has no harvest-weight column; therefore no post-harvest harvest measure is used as a feature.
- The source contains 1,426 records and 20 columns, with missing rainfall, soil pH and pest-index values handled during preprocessing.
''')
(DOCS_DIR / 'source_log.md').write_text(f'''# Source Log

- File used: `{RAW_FILE.name}`
- SHA-256: `{sha256_file(RAW_FILE)}`
- Date accessed: {date.today().isoformat()}
- Source description: Rwanda maize yield records supplied for the revised Q1 dataset.
- Limitation: provenance and licence details should be completed from the dataset provider before submission.
''')
"""),
])

write("02_eda.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 3: EDA and data audit"),
    nbf.v4.new_markdown_cell("This notebook audits the revised schema without modifying the raw file, quantifies missingness and duplicates, and creates concise quality charts."),
    nbf.v4.new_code_cell(BOOT + """
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from src.config import RAW_FILE, DOCS_DIR, FIGURE_DIR
from src.cleaning import to_string_df, parse_number
DOCS_DIR.mkdir(parents=True, exist_ok=True); FIGURE_DIR.mkdir(parents=True, exist_ok=True)
df = to_string_df(RAW_FILE)
issues = []
def add(problem, columns, count, severity, treatment):
    issues.append({'problem': problem, 'columns_affected': columns, 'records_affected': int(count), 'severity': severity, 'proposed_treatment': treatment})
add('Exact duplicate rows', 'all', df.duplicated().sum(), 'High', 'Remove exact duplicates')
add('Repeated record identifiers', 'record_id', df['record_id'].duplicated().sum(), 'High', 'Keep the most complete record')
add('Missing values', 'rainfall_mm,soil_ph,pest_incidence_index', df.isna().sum().sum(), 'Medium', 'Fit training-only imputers')
add('Invalid target or area', 'yield_t_ha,farm_area_ha', ((parse_number(df['yield_t_ha']) <= 0) | (parse_number(df['farm_area_ha']) <= 0)).sum(), 'High', 'Set invalid values missing and drop missing targets')
add('Out-of-range pest index', 'pest_incidence_index', ((parse_number(df['pest_incidence_index']) < 0) | (parse_number(df['pest_incidence_index']) > 1)).sum(), 'Medium', 'Set invalid values missing')
add('Potential target leakage', 'yield_t_ha', df['yield_t_ha'].notna().sum(), 'High', 'Keep only as target; never include it in X')
quality = pd.DataFrame(issues)
quality.to_csv(DOCS_DIR / 'data_quality_report.csv', index=False)
(DOCS_DIR / 'data_quality_report.md').write_text('# Q1 Data Quality Report\\n\\n' + quality.to_string(index=False))
display(quality)
for col in ['yield_t_ha','rainfall_mm','avg_temp_c','npk_kg_ha']:
    plt.figure(figsize=(6,4)); sns.histplot(parse_number(df[col]), kde=True); plt.title(col); plt.tight_layout(); plt.savefig(FIGURE_DIR / f'hist_{col}.png'); plt.close()
plt.figure(figsize=(8,4)); sns.boxplot(data=df, x='season', y=parse_number(df['yield_t_ha'])); plt.title('Yield by season'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'box_yield_season.png'); plt.close()
numeric = pd.DataFrame({c: parse_number(df[c]) for c in ['year','altitude_m','rainfall_mm','avg_temp_c','soil_ph','npk_kg_ha','urea_kg_ha','manure_t_ha','plant_density_per_ha','farm_area_ha','pest_incidence_index','yield_t_ha']})
plt.figure(figsize=(8,6)); sns.heatmap(numeric.corr(), cmap='coolwarm', center=0); plt.title('Numeric correlation heatmap'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'heatmap_corr.png'); plt.close()
"""),
])

write("03_clean.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 4: cleaning and preprocessing"),
    nbf.v4.new_markdown_cell("Clean source values, derive canonical units, split by season, and fit preprocessing only on the training partition."),
    nbf.v4.new_code_cell(BOOT + """
import pandas as pd, joblib
from src.config import RAW_FILE, INTERIM_DIR, PROCESSED_DIR, DOCS_DIR, TARGET_COL
from src.cleaning import to_string_df, clean_q1, add_time_features
from src.features import engineer_features
from src.logging_utils import CleaningLog
from src.pipeline import split_train_val_test, build_preprocessor, transform_split, add_low_yield_label
for p in [INTERIM_DIR, PROCESSED_DIR, DOCS_DIR]: p.mkdir(parents=True, exist_ok=True)
clog = CleaningLog()
clean = engineer_features(add_time_features(clean_q1(to_string_df(RAW_FILE), clog)))
clean.to_csv(INTERIM_DIR / 'maize_clean.csv', index=False)
train_df, val_df, test_df = split_train_val_test(clean)
q20 = add_low_yield_label(train_df, val_df, test_df)
pre, feature_cols = build_preprocessor(train_df)
joblib.dump({'preprocessor': pre, 'feature_cols': feature_cols, 'q20_threshold': q20}, PROCESSED_DIR / 'preprocessor.joblib')
for src, name in [(train_df,'train'), (val_df,'validation'), (test_df,'test')]:
    X = transform_split(pre, src, feature_cols)
    pd.concat([src[['record_id', TARGET_COL, 'low_yield_risk']].reset_index(drop=True), X.reset_index(drop=True)], axis=1).to_csv(PROCESSED_DIR / f'{name}_model_ready.csv', index=False)
    src.to_csv(PROCESSED_DIR / f'{name}_clean_unscaled.csv', index=False)
clog.save(DOCS_DIR / 'cleaning_log.csv', DOCS_DIR / 'cleaning_log.md')
print('Split shapes:', train_df.shape, val_df.shape, test_df.shape)
"""),
])

write("04_features.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 5: feature engineering and selection"),
    nbf.v4.new_markdown_cell("Review revised-dataset features using training data only; the target and source target column never enter the candidate inputs."),
    nbf.v4.new_code_cell(BOOT + """
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from src.config import PROCESSED_DIR, DOCS_DIR, TARGET_COL
from src.features import remove_high_corr, rf_importance, select_features_numeric
DOCS_DIR.mkdir(parents=True, exist_ok=True)
train = pd.read_csv(PROCESSED_DIR / 'train_clean_unscaled.csv')
excluded = {'record_id', TARGET_COL, 'yield_t_ha'}
X = train[[c for c in train.columns if c not in excluded]]
num = X.select_dtypes(include='number')
kept, selected = select_features_numeric(num, train[TARGET_COL], k=15)
mi = mutual_info_regression(num.fillna(num.median()), train[TARGET_COL], random_state=42)
mi_df = pd.DataFrame({'feature': num.columns, 'mutual_info': mi}).sort_values('mutual_info', ascending=False)
mi_df.to_csv(DOCS_DIR / 'mutual_information.csv', index=False)
rf_importance(X, train[TARGET_COL]).to_csv(DOCS_DIR / 'rf_importance.csv', index=False)
pd.DataFrame({'variance_kept': pd.Series(kept), 'selected_by_f_regression': pd.Series(selected)}).to_csv(DOCS_DIR / 'feature_selection.csv', index=False)
display(mi_df.head(15))
"""),
])

write("05_finalise.ipynb", [
    nbf.v4.new_markdown_cell("Group Achille-Sylvie | Members: Cishahayo Songa Achille, Umwiza Sylvie | Question: Q1 | Stage: 6: finalise"),
    nbf.v4.new_markdown_cell("Package the revised Q1 outputs and document the new target, source fields, cleaning decisions, and limitations."),
    nbf.v4.new_code_cell(BOOT + """
from datetime import date
from src.config import DOCS_DIR, PROCESSED_DIR, TARGET_COL
from src.cleaning import to_string_df
import pandas as pd
train = pd.read_csv(PROCESSED_DIR / 'train_model_ready.csv')
val = pd.read_csv(PROCESSED_DIR / 'validation_model_ready.csv')
test = pd.read_csv(PROCESSED_DIR / 'test_model_ready.csv')
summary = f'''# Q1 Data Card

- Target: `{TARGET_COL}` (derived from source `yield_t_ha` by multiplying by 1,000).
- Records: train={len(train)}, validation={len(val)}, test={len(test)}.
- Revised source fields: record ID, year, season, geography, weather, soil, seed, farming practice, fertiliser, density, area, irrigation and pest index.
- Leakage control: `yield_t_ha` is excluded from model features; no harvest-weight field is present in the revised source.
- Prepared: {date.today().isoformat()}.
- Limitation: this is a prepared dataset, not a trained or deployed prediction model.
'''
(DOCS_DIR / 'data_card.md').write_text(summary)
(DOCS_DIR / 'memo_to_manager.md').write_text('''# Memo to Manager

The revised Rwanda maize dataset contains 1,426 observations and 20 source columns. The Q1 workflow now uses `yield_t_ha` as the target and converts it to `yield_kg_per_ha`. It derives total fertiliser from NPK, urea and manure, uses `farm_area_ha`, and maps the pest index into an ordinal category. Missing values are handled by training-fitted preprocessing, and the source target is excluded from model inputs. The outputs are ready for later model evaluation, but this repository still does not train a production model.
''')
print(summary)
"""),
])

def build_combined():
    combined = nbf.v4.new_notebook()
    combined.cells = [
        nbf.v4.new_markdown_cell(
            "# Q1 Maize Yield Preparation\n\n"
            "This notebook contains the complete workflow. Each stage begins with an explanation "
            "before its code. Run the stages from top to bottom in a clean kernel."
        )
    ]
    for number, title in [
        ("00", "Step 1 — Verify the environment"),
        ("01", "Step 2 — Acquire and document the revised dataset"),
        ("02", "Step 3 — Explore and audit data quality"),
        ("03", "Step 4 — Clean and preprocess"),
        ("04", "Step 5 — Engineer and select features"),
        ("05", "Step 6 — Finalise and verify outputs"),
    ]:
        path = NB_DIR / f"{number}_{'environment_test' if number == '00' else 'acquire' if number == '01' else 'eda' if number == '02' else 'clean' if number == '03' else 'features' if number == '04' else 'finalise'}.ipynb"
        source = nbf.read(path, as_version=4)
        combined.cells.append(nbf.v4.new_markdown_cell(f"## {title}\n\nThe explanation below describes this step before the code runs."))
        for cell in source.cells:
            if cell.cell_type == "code":
                cell.source = cell.source.replace("plt.savefig(FIGURE_DIR / f'hist_{col}.png'); plt.close()", "plt.savefig(FIGURE_DIR / f'hist_{col}.png'); display(plt.gcf()); plt.close()")
                cell.source = cell.source.replace("plt.savefig(FIGURE_DIR / 'box_yield_season.png'); plt.close()", "plt.savefig(FIGURE_DIR / 'box_yield_season.png'); display(plt.gcf()); plt.close()")
                cell.source = cell.source.replace("plt.savefig(FIGURE_DIR / 'heatmap_corr.png'); plt.close()", "plt.savefig(FIGURE_DIR / 'heatmap_corr.png'); display(plt.gcf()); plt.close()")
            combined.cells.append(cell)
    nbf.write(combined, NB_DIR / "q1_maize_yield_workflow.ipynb")
    for path in NB_DIR.glob("0*.ipynb"):
        path.unlink()

build_combined()
print(f"Built combined Q1 notebook in {NB_DIR}")
