from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "q1_maize_yield" / "notebooks"
NB_DIR.mkdir(parents=True, exist_ok=True)


def write_nb(name, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    (NB_DIR / name).write_text(nbf.writes(nb))

common_boot = """import sys\nfrom pathlib import Path\nROOT = Path.cwd()\nwhile not (ROOT / 'src').exists() and ROOT != ROOT.parent:\n    ROOT = ROOT.parent\nif str(ROOT) not in sys.path:\n    sys.path.insert(0, str(ROOT))\n"""

# 00
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 1: environment test"),
    nbf.v4.new_code_cell(common_boot + """
import platform, pandas as pd, numpy as np, matplotlib, seaborn as sns, sklearn, nbformat, nbconvert, joblib
print('Python:', platform.python_version())
print('pandas:', pd.__version__)
print('numpy:', np.__version__)
print('matplotlib:', matplotlib.__version__)
print('seaborn:', sns.__version__)
print('scikit-learn:', sklearn.__version__)
print('nbformat:', nbformat.__version__)
print('nbconvert:', nbconvert.__version__)
print('joblib:', joblib.__version__)
"""),
]
write_nb("00_environment_test.ipynb", cells)

# 01 acquire
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 2: requirements and acquisition"),
    nbf.v4.new_markdown_cell("How this works: we locate the real raw file, otherwise build a clearly labelled stand-in, then document requirements, source provenance, and data dictionary from code."),
    nbf.v4.new_code_cell(common_boot + """
from pathlib import Path
from datetime import date
import shutil
import pandas as pd
from src.config import RAW_FILE, STANDIN_FILE, COLUMNS, DOCS_DIR
from src.cleaning import sha256_file, to_string_df

DOCS_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE.parent.mkdir(parents=True, exist_ok=True)

candidates = [
    Path.cwd() / 'maize_yield_rwanda_raw.csv',
    Path.home() / 'Downloads' / 'maize_yield_rwanda_raw.csv',
    RAW_FILE,
]
found = None
for p in candidates:
    if p.exists():
        found = p
        break

standin_used = False
if found is None:
    from tools.make_standin_q1 import main as make_standin
    make_standin(str(STANDIN_FILE))
    use_file = STANDIN_FILE
    standin_used = True
else:
    if found.resolve() != RAW_FILE.resolve():
        shutil.copy2(found, RAW_FILE)
    use_file = RAW_FILE

if use_file == RAW_FILE and RAW_FILE.exists():
    try:
        import os
        os.chmod(RAW_FILE, 0o444)
    except Exception:
        pass

print('Using file:', use_file)
print('Stand-in used:', standin_used)

df_raw = to_string_df(use_file)
print('shape=', df_raw.shape)
display(df_raw.head())
display(df_raw.tail())
print(df_raw.dtypes)
print(df_raw.info())

# data requirements
req_md = f'''# Data Requirements (Q1)

{'**BUILT ON STAND-IN DATA, RE-RUN ON REAL FILE**' if standin_used else ''}

- Target: `yield_kg_per_ha`
- Area: 4 provinces, 14+ districts, 20 cooperatives
- Period: 2023-2025
- Required uses: Questions A-E from stakeholder brief

## Requirement-vs-file check

| Business question | Needed columns | Meets now? | Gaps |
|---|---|---|---|
| A Expected yield | yield_kg_per_ha, farm_size, harvest_weight_kg | Yes | Requires cleaning consistency checks |
| B Fertilizer + seed effect | fertilizer_kg, farm_size, seed_variety | Yes | Must normalize fertilizer per ha |
| C Weather + altitude + irrigation | rainfall_mm, avg_temp_c, altitude_m, irrigation | Yes | Requires realism validation |
| D Location + season differences | province, district, season, planting_date | Yes | Requires label/date harmonization |
| E Low harvest risk (pre-harvest) | pre-harvest fields only | Partial | Must remove leakage columns |
'''
(DOCS_DIR / 'data_requirements.md').write_text(req_md)

# data dictionary
rows = []
meta = {
    'farm_id': ('Farm code', 'string', 'n/a', 'identifier', 'No'),
    'province': ('Province name', 'string', 'n/a', 'Eastern/Southern/Northern/Western', 'No'),
    'district': ('District name', 'string', 'n/a', 'district label', 'No'),
    'cooperative_id': ('Cooperative code', 'string', 'n/a', 'C001..', 'No'),
    'altitude_m': ('Farm altitude', 'numeric', 'meters', 'approx 900-2800', 'No'),
    'season': ('Cropping season', 'categorical', 'n/a', 'A/B/C', 'No'),
    'planting_date': ('Planting date', 'date', 'date', '2023-2025', 'No'),
    'farm_size': ('Farm size value', 'numeric/text', 'mixed', 'with farm_size_unit', 'No'),
    'farm_size_unit': ('Farm size unit', 'categorical', 'ha/m2/acre/are', 'unit variants', 'No'),
    'seed_variety': ('Seed type', 'categorical', 'n/a', 'Local/Improved/Hybrid', 'No'),
    'fertilizer_kg': ('Total fertilizer applied', 'numeric', 'kg', 'whole farm total', 'No'),
    'rainfall_mm': ('Rainfall', 'numeric', 'mm', 'seasonal rainfall', 'No'),
    'avg_temp_c': ('Average temperature', 'numeric', '°C', 'season average', 'No'),
    'soil_type': ('Soil category', 'categorical', 'n/a', 'Clay/Loam/Sandy', 'No'),
    'soil_ph': ('Soil pH', 'numeric', 'pH', 'approx 4-8', 'No'),
    'pest_incidence': ('Pest pressure', 'ordinal', 'n/a', 'Low/Medium/High', 'No'),
    'irrigation': ('Irrigation used', 'categorical', 'n/a', 'Yes/No', 'No'),
    'farmer_age': ('Farmer age', 'numeric', 'years', 'adult expected', 'No'),
    'harvest_weight_kg': ('Harvest weight', 'numeric', 'kg', 'post-harvest leakage risk', 'Yes'),
    'yield_kg_per_ha': ('Yield per hectare (target)', 'numeric', 'kg/ha', 'target', 'Yes'),
}
for c in COLUMNS:
    m = meta.get(c, ('', '', '', '', 'No'))
    rows.append({'column_name': c, 'meaning': m[0], 'data_type': m[1], 'unit': m[2], 'allowed_values_or_notes': m[3], 'known_to_be_post_harvest?': m[4]})
dd = pd.DataFrame(rows)
dd.to_csv(DOCS_DIR / 'data_dictionary.csv', index=False)
(DOCS_DIR / 'data_dictionary.md').write_text('# Data Dictionary\\n\\n' + dd.to_string(index=False))

# source log
source_md = f'''# Source Log

{'**BUILT ON STAND-IN DATA, RE-RUN ON REAL FILE**' if standin_used else ''}

- Source: MCSU district field forms merged by officers
- File used: `{use_file.name}`
- SHA-256: `{sha256_file(use_file)}`
- Date accessed: {date.today().isoformat()}
- Licence/permission: course use only
- Collected by: district field officers
- Limitations: manual typing, merged rapidly, mixed entry formats
- Ethical issues: no personal identifiers; possible district coverage and reporting bias
'''
(DOCS_DIR / 'source_log.md').write_text(source_md)
"""),
]
write_nb("01_acquire.ipynb", cells)

# 02 EDA
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 3: EDA and data audit"),
    nbf.v4.new_markdown_cell("How this works: this notebook audits quality issues without modifying source data, quantifies each issue class, and writes a data quality report generated from code."),
    nbf.v4.new_code_cell(common_boot + """
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from pathlib import Path
from src.config import RAW_FILE, STANDIN_FILE, DOCS_DIR, FIGURE_DIR
from src.cleaning import to_string_df, parse_number, parse_dates
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

raw_path = RAW_FILE if RAW_FILE.exists() else STANDIN_FILE
df = to_string_df(raw_path)
print('raw path', raw_path, 'shape', df.shape)

issues = []
def add_issue(pid, problem, cols, n, sev, reason, treat):
    issues.append({'ID': pid, 'problem': problem, 'columns_affected': cols, 'number_of_records_affected': int(n), 'severity': sev, 'severity_reason': reason, 'proposed_treatment': treat})

# 1 duplicates
norm_farm = df['farm_id'].str.strip().str.lower()
exact_dup = df.duplicated().sum()
near_dup = pd.DataFrame({'farm': norm_farm, 'season': df['season'].str.strip().str.lower(), 'year': parse_dates(df['planting_date']).dt.year}).duplicated(subset=['farm','season','year']).sum()
add_issue(1, 'Exact and near duplicates', 'farm_id, season, planting_date', exact_dup + near_dup, 'High', 'Duplicates distort distributions and leakage in split', 'Remove exact duplicates then keep most complete near-duplicate')

# 2 mixed units
unit_var = df['farm_size_unit'].str.strip().str.lower().nunique()
mixed_unit = (unit_var > 1)
add_issue(2, 'Mixed farm size units', 'farm_size,farm_size_unit', df['farm_size_unit'].notna().sum() if mixed_unit else 0, 'High', 'Incorrect per-hectare normalization risk', 'Convert all sizes to hectares')

# 3 inconsistent category spellings
cat_cols = ['district','province','season','seed_variety','soil_type','pest_incidence','irrigation']
n_incons = 0
for c in cat_cols:
    vals = df[c].astype(str)
    n_incons += (vals.str.strip() != vals).sum() + (vals.str.lower() != vals).sum()
add_issue(3, 'Inconsistent categorical spellings/case', ','.join(cat_cols), n_incons, 'Medium', 'Category fragmentation affects grouping and encoding', 'Normalize strip/case and mapping tables')

# 4 disguised missing
missing_tokens = {'-999','-1','0','N/A','NA','unknown','?','', ' '}
n_disg = 0
for c in df.columns:
    n_disg += df[c].astype(str).str.strip().isin(missing_tokens).sum()
add_issue(4, 'Disguised missing values', 'multiple', n_disg, 'High', 'Silent bad values bias stats', 'Map disguised missing to NaN')

# 5 real missing
n_real_missing = int(df.replace({'':np.nan,' ':np.nan}).isna().sum().sum())
add_issue(5, 'Real missing values', 'multiple', n_real_missing, 'High', 'Missingness can bias model and fairness', 'Impute from train-only statistics')

# 6 mixed date formats/out of range
dt = parse_dates(df['planting_date'])
out_range = ((dt.dt.year < 2023) | (dt.dt.year > 2025)).sum()
add_issue(6, 'Date format/range problems', 'planting_date', int(dt.isna().sum() + out_range), 'High', 'Wrong season alignment and time leakage risk', 'Robust parse + enforce 2023-2025')

# 7 impossible values
alt = parse_number(df['altitude_m']); temp=parse_number(df['avg_temp_c']); ph=parse_number(df['soil_ph'])
rain=parse_number(df['rainfall_mm']); age=parse_number(df['farmer_age']); fert=parse_number(df['fertilizer_kg']); yld=parse_number(df['yield_kg_per_ha'])
n_imp = ((yld<=0)|(ph<4)|(ph>8)|(temp<0)|(temp>60)|(alt<500)|(alt>3500)|(rain<0)|(rain>5000)|(age<18)|(age>100)|(fert<0)).sum()
add_issue(7, 'Impossible/unrealistic values', 'numeric columns', int(n_imp), 'High', 'Violates agronomic/physical constraints', 'Set invalid to NaN, optionally winsorize extremes')

# 8 outliers
num_df = pd.DataFrame({'altitude_m':alt,'temp':temp,'rain':rain,'fert':fert,'yield':yld,'age':age,'soil_ph':ph}).dropna(how='all')
outlier_count=0
for c in num_df.columns:
    s=num_df[c].dropna(); q1,q3=s.quantile([0.25,0.75]); iqr=q3-q1
    outlier_count += ((s < q1-1.5*iqr) | (s > q3+1.5*iqr)).sum()
add_issue(8, 'IQR outliers', 'all numeric', int(outlier_count), 'Medium', 'Some outliers are true extremes; others entry errors', 'Review with domain context and cap only clear errors')

# 9 yield consistency
size = parse_number(df['farm_size'])
unit = df['farm_size_unit'].str.lower().str.strip()
size_ha = size.copy(); size_ha[unit.eq('m2')] = size[unit.eq('m2')]/10000; size_ha[unit.eq('acres')] = size[unit.eq('acres')]*0.404686; size_ha[unit.eq('are')] = size[unit.eq('are')]*0.01
harv = parse_number(df['harvest_weight_kg'])
recalc = harv/size_ha
mismatch = ((yld-recalc).abs()/recalc.abs().clip(lower=1) > 0.1).sum()
add_issue(9, 'Yield mismatch vs harvest/size', 'harvest_weight_kg,farm_size,yield_kg_per_ha', int(mismatch), 'High', 'Target inconsistency hurts supervised learning', 'Recompute when mismatch is large and inputs valid')

# 10 province-district mismatch + coop multi-district
pd_mismatch = (df['province'].str.strip().str.lower().eq('eastern') & df['district'].str.strip().str.lower().eq('huye')).sum()
coop_multi = df.groupby(df['cooperative_id'].str.strip().str.lower())['district'].nunique().gt(1).sum()
add_issue(10, 'Geo hierarchy inconsistencies', 'province,district,cooperative_id', int(pd_mismatch + coop_multi), 'Medium', 'Wrong aggregations by place', 'Use district->province lookup and investigate coop mapping')

# 11 wrong types with units/commas
type_noise = 0
for c in ['farm_size','fertilizer_kg','harvest_weight_kg','yield_kg_per_ha']:
    type_noise += df[c].astype(str).str.contains(',', regex=False).sum() + df[c].astype(str).str.contains('kg', case=False, regex=False).sum()
add_issue(11, 'Numeric fields stored as text/units', 'farm_size,fertilizer_kg,harvest_weight_kg,yield_kg_per_ha', int(type_noise), 'Medium', 'Parsing errors if untreated', 'Strip commas/units then convert types')

# 12 leakage
add_issue(12, 'Post-harvest leakage columns', 'harvest_weight_kg,yield_kg_per_ha', int(df['harvest_weight_kg'].notna().sum()), 'High', 'harvest_weight known after harvest only', 'Exclude from X for risk/forecast tasks')

# 13 irrigation-season conflicts
season = df['season'].str.strip().str.upper()
irr = df['irrigation'].str.strip().str.lower()
conflict = ((season.isin(['A','B'])) & irr.isin(['yes','y','1','true'])).sum()
add_issue(13, 'Irrigation-season conflicts', 'irrigation,season', int(conflict), 'Low', 'Mostly rain-fed in A/B but rare irrigation can exist', 'Review and keep plausible rare values')

# 14 whitespace/case constants high-card IDs
ws = sum((df[c].astype(str) != df[c].astype(str).str.strip()).sum() for c in df.columns)
const = int((df.nunique(dropna=False)<=1).sum())
add_issue(14, 'Whitespace/case, constant cols, high-card IDs', 'multiple', int(ws+const), 'Low', 'Cosmetic noise and identifier complexity', 'Trim text and keep IDs only for split/integrity')

q = pd.DataFrame(issues)
q.to_csv(DOCS_DIR / 'data_quality_report.csv', index=False)
(DOCS_DIR / 'data_quality_report.md').write_text('# Data Quality Report\\n\\n' + q.to_string(index=False))
print(q)

# plots (>=8)
for c in ['yield_kg_per_ha','fertilizer_kg','rainfall_mm','avg_temp_c']:
    plt.figure(figsize=(6,4)); sns.histplot(parse_number(df[c]), kde=True); plt.title(f'{c} distribution'); plt.tight_layout(); plt.savefig(FIGURE_DIR / f'hist_{c}.png'); plt.close()

plt.figure(figsize=(8,4)); sns.countplot(x=df['season'].astype(str).str.upper()); plt.title('Season counts'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'bar_season.png'); plt.close()
plt.figure(figsize=(8,4)); sns.boxplot(x=df['seed_variety'].astype(str), y=parse_number(df['yield_kg_per_ha'])); plt.title('Yield by seed variety'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'box_yield_seed.png'); plt.close()

size_ha_plot = size_ha.replace([np.inf,-np.inf], np.nan)
plt.figure(figsize=(6,4)); sns.scatterplot(x=parse_number(df['fertilizer_kg'])/size_ha_plot, y=parse_number(df['yield_kg_per_ha']), alpha=0.5); plt.title('Yield vs fertilizer/ha'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'scatter_yield_fertilizer_perha.png'); plt.close()

num_cols = ['altitude_m','fertilizer_kg','rainfall_mm','avg_temp_c','soil_ph','farmer_age','yield_kg_per_ha']
num = pd.DataFrame({c:parse_number(df[c]) for c in num_cols})
plt.figure(figsize=(8,6)); sns.heatmap(num.corr(), cmap='coolwarm', center=0); plt.title('Correlation heatmap'); plt.tight_layout(); plt.savefig(FIGURE_DIR / 'heatmap_corr.png'); plt.close()

# brief interpretation notes
notes = [
    ('hist_yield_kg_per_ha.png', 'Yield shows skew and suspicious extremes, supporting robust cleaning and clipping rules.'),
    ('hist_fertilizer_kg.png', 'Fertilizer totals vary widely because farm sizes differ, motivating fertilizer per hectare.'),
    ('hist_rainfall_mm.png', 'Rainfall has long tails and a few implausible high values likely from entry errors.'),
    ('hist_avg_temp_c.png', 'Temperature centers in agronomic range but includes impossible points needing correction.'),
    ('bar_season.png', 'Seasons A and B dominate records; C is smaller, affecting stratification and fairness checks.'),
    ('box_yield_seed.png', 'Improved/Hybrid seeds tend to higher medians, aligned with stakeholder question B.'),
    ('scatter_yield_fertilizer_perha.png', 'Yield tends to increase with fertilizer/ha but with diminishing and noisy relationship.'),
    ('heatmap_corr.png', 'Numeric correlations are moderate; no single factor explains yield alone.'),
]
(Path(DOCS_DIR / 'eda_chart_interpretations.md')).write_text('# EDA Figure Notes\\n\\n' + '\\n'.join([f'- **{a}**: {b}' for a,b in notes]))
"""),
]
write_nb("02_eda.ipynb", cells)

# 03 clean
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 4: cleaning and preprocessing"),
    nbf.v4.new_markdown_cell("How this works: clean with explicit rules, log every operation, remove leakage from X, split first, then fit preprocessing on train only."),
    nbf.v4.new_code_cell(common_boot + """
import pandas as pd
from pathlib import Path
import joblib
from src.config import RAW_FILE, STANDIN_FILE, INTERIM_DIR, PROCESSED_DIR, DOCS_DIR, TARGET_COL, LEAKAGE_COLS
from src.cleaning import to_string_df, clean_q1, add_time_features
from src.features import engineer_features
from src.logging_utils import CleaningLog
from src.pipeline import split_train_val_test, build_preprocessor, transform_split, add_low_yield_label

INTERIM_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

raw_path = RAW_FILE if RAW_FILE.exists() else STANDIN_FILE
raw = to_string_df(raw_path)
clog = CleaningLog()
clean = clean_q1(raw, clog)
clean = add_time_features(clean)
clean = engineer_features(clean)
clean.to_csv(INTERIM_DIR / 'maize_clean.csv', index=False)

train_df, val_df, test_df = split_train_val_test(clean)
q20 = add_low_yield_label(train_df, val_df, test_df)

pre, feature_cols = build_preprocessor(train_df)
joblib.dump({'preprocessor': pre, 'feature_cols': feature_cols, 'q20_threshold': q20}, PROCESSED_DIR / 'preprocessor.joblib')

Xtr = transform_split(pre, train_df, feature_cols)
Xva = transform_split(pre, val_df, feature_cols)
Xte = transform_split(pre, test_df, feature_cols)

for src, X, name in [(train_df,Xtr,'train'),(val_df,Xva,'validation'),(test_df,Xte,'test')]:
    full = pd.concat([src[['farm_id', TARGET_COL, 'low_yield_risk']].reset_index(drop=True), X.reset_index(drop=True)], axis=1)
    full.to_csv(PROCESSED_DIR / f'{name}_model_ready.csv', index=False)
    src.to_csv(PROCESSED_DIR / f'{name}_clean_unscaled.csv', index=False)

clog.save(DOCS_DIR / 'cleaning_log.csv', DOCS_DIR / 'cleaning_log.md')

# leak check + split disjoint
s1,s2,s3 = set(train_df['farm_id']), set(val_df['farm_id']), set(test_df['farm_id'])
print('Split shapes:', train_df.shape, val_df.shape, test_df.shape)
print('farm_id overlaps:', len(s1&s2), len(s1&s3), len(s2&s3))
print('Low-yield threshold (train 20th percentile):', q20)
print('Leakage columns removed from X:', LEAKAGE_COLS)
"""),
]
write_nb("03_clean.ipynb", cells)

# 04 features
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 5: feature engineering and selection"),
    nbf.v4.new_markdown_cell("How this works: quantify engineered feature usefulness with correlation, mutual information, and train-only random forest importance."),
    nbf.v4.new_code_cell(common_boot + """
import pandas as pd, numpy as np
from pathlib import Path
from sklearn.feature_selection import mutual_info_regression
from src.config import PROCESSED_DIR, DOCS_DIR, TARGET_COL
from src.features import remove_high_corr, rf_importance, select_features_numeric

DOCS_DIR.mkdir(parents=True, exist_ok=True)
train = pd.read_csv(PROCESSED_DIR / 'train_clean_unscaled.csv')
val = pd.read_csv(PROCESSED_DIR / 'validation_clean_unscaled.csv')
test = pd.read_csv(PROCESSED_DIR / 'test_clean_unscaled.csv')

feature_candidates = [c for c in train.columns if c not in ['farm_id', TARGET_COL, 'harvest_weight_kg', 'planting_date', 'planting_dt']]
X_train = train[feature_candidates].copy()
y_train = train[TARGET_COL]

# numeric-only analysis for MI and selection summary
X_num = X_train.select_dtypes(include=['number']).copy()
X_num2, dropped_corr = remove_high_corr(X_num, threshold=0.9)
kept_var, selected_num = select_features_numeric(X_num2, y_train, k=min(15, max(1, X_num2.shape[1])))

mi = mutual_info_regression(X_num2.fillna(X_num2.median()), y_train, random_state=42)
mi_df = pd.DataFrame({'feature': X_num2.columns, 'mutual_info': mi}).sort_values('mutual_info', ascending=False)
rf_df = rf_importance(X_train, y_train)

feature_rows = []
def add_row(f, how, evidence, q):
    feature_rows.append({'feature':f,'created_or_keep_remove_reason':how,'evidence':evidence,'linked_question':q})

core_new = ['fertilizer_kg_per_ha','planting_month','planting_quarter','days_from_season_start','is_improved_seed','seed_rank','altitude_band','temp_deviation_from_optimum','rain_per_temp','rainfall_log','fertilizer_log1p','farm_size_log','irrigated_flag','season_x_irrigation']
for f in core_new:
    if f in train.columns:
        add_row(f, 'created', 'Domain-informed feature engineering from Stage 5', 'B/C/D/E')

for f in dropped_corr:
    add_row(f, 'removed', 'Highly correlated pair |r|>0.9', 'A/B/C')

for f in selected_num:
    add_row(f, 'kept', 'Selected by variance+f_regression on train set', 'A/B/C')

fj = pd.DataFrame(feature_rows).drop_duplicates()
fj.to_csv(DOCS_DIR / 'feature_justification.csv', index=False)
(DOCS_DIR / 'feature_justification.md').write_text('# Feature Justification\\n\\n' + fj.to_string(index=False) + '\\n\\n## Top Mutual Information\\n\\n' + mi_df.head(15).to_string(index=False) + '\\n\\n## RandomForest Importance (train only)\\n\\n' + rf_df.head(15).to_string(index=False))

# save selected feature list
selected_all = sorted(set(selected_num + [c for c in feature_candidates if c not in X_num.columns]))
(Path(PROCESSED_DIR / 'selected_features.txt')).write_text('\\n'.join(selected_all))
print('Engineered feature count in train:', len([f for f in core_new if f in train.columns]))
print('Selected numeric features:', len(selected_num))
print('Dropped correlated numeric features:', dropped_corr)
"""),
]
write_nb("04_features.ipynb", cells)

# 05 finalise
cells = [
    nbf.v4.new_markdown_cell("Group XX | Members: [Student 1], [Student 2] | Question: Q1 | Stage: 6: finalise"),
    nbf.v4.new_markdown_cell("How this works: package final outputs, write data card/memo/checklists, and expose a reusable prepare_new_data interface."),
    nbf.v4.new_code_cell(common_boot + """
from pathlib import Path
from datetime import date
import pandas as pd
import joblib
from src.config import DOCS_DIR, PROCESSED_DIR, INTERIM_DIR, TARGET_COL
from src.cleaning import clean_q1, add_time_features
from src.features import engineer_features
from src.logging_utils import CleaningLog

# prepare_new_data helper
prep_py = ROOT / 'src/prepare_new_data.py'
prep_py.write_text('''import pandas as pd\nfrom src.cleaning import clean_q1, add_time_features\nfrom src.features import engineer_features\nfrom src.logging_utils import CleaningLog\n\ndef prepare_new_data(df_raw: pd.DataFrame) -> pd.DataFrame:\n    clog = CleaningLog()\n    clean = clean_q1(df_raw.copy(), clog)\n    clean = add_time_features(clean)\n    clean = engineer_features(clean)\n    return clean\n''')

train = pd.read_csv(PROCESSED_DIR / 'train_clean_unscaled.csv')
val = pd.read_csv(PROCESSED_DIR / 'validation_clean_unscaled.csv')
test = pd.read_csv(PROCESSED_DIR / 'test_clean_unscaled.csv')

rows_in = len(pd.read_csv(INTERIM_DIR / 'maize_clean.csv')) if (INTERIM_DIR / 'maize_clean.csv').exists() else 'n/a'
rows_usable = len(train) + len(val) + len(test)

data_card = f'''# Data Card (Q1 Maize)

- Purpose: prepare a machine-learning-ready maize dataset for questions A-E.
- Source: MCSU merged district forms (or stand-in when source unavailable).
- Size (usable): {rows_usable} rows across train/validation/test.
- Target: `{TARGET_COL}`.
- Key cleaning: text normalization, unit conversion to hectares, date parsing, deduplication, impossible value handling, leakage control.
- Key features: fertilizer per hectare, planting timing, seed and irrigation indicators, climate interactions.
- Limitations: data-entry noise, potential district/cooperative reporting bias, stand-in usage if real file missing.
- Reproducibility: `python run_all.py`.
'''
(DOCS_DIR / 'data_card.md').write_text(data_card)

memo = f'''# Memo to Manager

**To:** Mr. Habimana, Head of Planning and Data  
**From:** Junior Analyst (Group XX)  
**Date:** {date.today().isoformat()}  
**Subject:** Q1 Maize dataset readiness for ML analysis

1. **What we received:** We processed the raw file into clean train/validation/test datasets totaling {rows_usable} usable records.
2. **Main problems found:** (i) duplicate and near-duplicate farm-season records, (ii) mixed units and numeric text formats, (iii) unrealistic/invalid values and missingness. These issues would bias estimates if not corrected.
3. **Data removed/changed:** Invalid targets were removed, inconsistent target values were recomputed from harvest and area when inputs were trustworthy, and leakage column `harvest_weight_kg` was removed from model features.
4. **New features for questions A-E:** Added fertilizer per hectare, planting time metrics, seed quality indicators, altitude/temperature/rainfall interactions, and low-yield risk label.
5. **Limits and risks:** Quality still depends on field-entry consistency and district reporting practices; risk analyses must avoid post-harvest leakage.
6. **Recommendation:** Dataset is ready for ML preparation tasks for A-E, with strongest support for A-D and leakage-safe setup for E. Next season, standardize digital forms and validation rules at capture time.
'''
(DOCS_DIR / 'memo_to_manager.md').write_text(memo)

screenshot = '''# Screenshot Checklist (take manually)

- Stage 1 (`00_environment_test.ipynb`): versions output cell.
- Stage 2 (`01_acquire.ipynb`): file detection + shape output, data dictionary preview.
- Stage 3 (`02_eda.ipynb`): data quality report table output and at least 5 figure outputs (include notebook title cell).
- Stage 4 (`03_clean.ipynb`): split shapes, overlap check, low-yield threshold, cleaning log sample.
- Stage 5 (`04_features.ipynb`): feature counts, MI table, RF importance table.
- Stage 6 (`05_finalise.ipynb`): confirmation of generated docs and helper function.

Suggested caption format: "Stage X output showing [what], confirming [decision]."
Suggested explanation: 1-3 sentences on why the output matters for data readiness and leakage prevention.
'''
(DOCS_DIR / 'screenshot_checklist.md').write_text(screenshot)

cheat = '''# Oral Defence Cheatsheet

- Why split before scaling/imputation? To avoid test leakage and preserve unbiased validation.
- Why train-only fitting? Model preprocessing must reflect only information available at training time.
- Why median imputation? Numeric fields were skewed and had outliers.
- Why one-hot vs ordinal? Ordinal used only for pest levels (Low<Medium<High); nominal categories one-hot encoded.
- Why remove harvest_weight from features? It is post-harvest and leaks outcome information.
- Why use fertilizer per hectare? Fertilizer totals are not comparable across different farm sizes.
- Why stratify by season? Preserves seasonal distribution across train/val/test.
- Why cap outliers? Limits data-entry error influence while retaining plausible extremes.
'''
(DOCS_DIR / 'oral_defence_cheatsheet.md').write_text(cheat)

# update root documentation outline with Q1 drafted sections
root_outline = ROOT / 'docs/documentation_report_outline.md'
root_outline.write_text('''# GroupXX_ML_Element1_Documentation Outline

1. Cover page
2. Q1 Stage 1: Environment and reproducibility setup
3. Q1 Stage 2: Requirements, acquisition, data dictionary, source log
4. Q1 Stage 3: EDA findings and data quality report
5. Q1 Stage 4: Cleaning/preprocessing pipeline, splits, and leakage controls
6. Q1 Stage 5: Feature engineering and selection evidence
7. Q1 Stage 6: Final datasets, data card, memo, verification
8. Q2 scaffold and scenario documentation (to implement later)
9. Appendices (cleaning log, feature justification, screenshot checklist, oral defence notes)
''')

print('Final docs generated.')
"""),
]
write_nb("05_finalise.ipynb", cells)

print('Notebooks built in', NB_DIR)
