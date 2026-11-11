from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

COLUMNS = [
    "farm_id", "province", "district", "cooperative_id", "altitude_m", "season", "planting_date",
    "farm_size", "farm_size_unit", "seed_variety", "fertilizer_kg", "rainfall_mm", "avg_temp_c",
    "soil_type", "soil_ph", "pest_incidence", "irrigation", "farmer_age", "harvest_weight_kg", "yield_kg_per_ha"
]

PROVINCES = {
    "Eastern": ["Gatsibo", "Kayonza", "Nyagatare", "Rwamagana", "Bugesera", "Ngoma"],
    "Southern": ["Huye", "Nyanza", "Gisagara", "Nyamagabe", "Muhanga"],
    "Northern": ["Musanze", "Gicumbi"],
    "Western": ["Rubavu", "Rusizi", "Karongi", "Ngororero"],
}


def make(n=1200):
    districts = [d for ds in PROVINCES.values() for d in ds]
    rows = []
    for i in range(n):
        district = rng.choice(districts)
        province = [k for k, v in PROVINCES.items() if district in v][0]
        season = rng.choice(["A", "B", "C"], p=[0.45, 0.45, 0.10])
        year = int(rng.choice([2023, 2024, 2025]))
        month_pool = {"A": [9,10,11,12,1], "B": [2,3,4,5,6], "C": [6,7,8,9]}[season]
        month = int(rng.choice(month_pool))
        day = int(rng.integers(1, 28))
        farm_size_ha = float(np.clip(rng.normal(1.2, 0.7), 0.15, 6.0))
        unit = rng.choice(["ha", "m2", "acres", "are"], p=[0.8, 0.1, 0.08, 0.02])
        if unit == "ha":
            farm_size = farm_size_ha
        elif unit == "m2":
            farm_size = farm_size_ha * 10000
        elif unit == "acres":
            farm_size = farm_size_ha / 0.404686
        else:
            farm_size = farm_size_ha / 0.01

        fertilizer = max(0, rng.normal(120, 45)) * farm_size_ha
        altitude = float(np.clip(rng.normal(1750, 350), 900, 2800))
        temp = float(np.clip(30 - (altitude - 900) / 200 + rng.normal(0, 1.8), 12, 33))
        rainfall = float(np.clip(rng.normal(900, 250), 300, 1700))
        soil = rng.choice(["Clay", "Loam", "Sandy"], p=[0.35, 0.45, 0.20])
        ph = float(np.clip(rng.normal(6.1, 0.7), 4.2, 7.8))
        seed = rng.choice(["Local", "Improved", "Hybrid"], p=[0.35, 0.45, 0.20])
        pest = rng.choice(["Low", "Medium", "High"], p=[0.4, 0.4, 0.2])
        irr = "Yes" if (season == "C" and rng.random() < 0.65) or (season != "C" and rng.random() < 0.08) else "No"
        age = int(rng.integers(18, 75))

        base_yield = 1500 + (200 if seed != "Local" else 0) + (350 if seed == "Hybrid" else 0) + 1.4 * fertilizer / max(farm_size_ha, 0.2)
        base_yield += (100 if irr == "Yes" else 0) - 180 * (pest == "High") + rng.normal(0, 350)
        yield_ha = float(np.clip(base_yield, 500, 7000))
        harvest = yield_ha * farm_size_ha

        rows.append([
            f"F{i:04d}", province, district, f"C{rng.integers(1,21):03d}", round(altitude, 1), season, f"{year}-{month:02d}-{day:02d}",
            round(farm_size, 3), unit, seed, round(fertilizer, 2), round(rainfall, 1), round(temp, 1),
            soil, round(ph, 2), pest, irr, age, round(harvest, 2), round(yield_ha, 2)
        ])

    df = pd.DataFrame(rows, columns=COLUMNS)
    for c in ["yield_kg_per_ha", "farm_size", "fertilizer_kg", "rainfall_mm", "avg_temp_c", "soil_ph", "farmer_age"]:
        df[c] = df[c].astype(object)

    # Inject issues
    idx = rng.choice(df.index, size=80, replace=False)
    df.loc[idx[:10], "yield_kg_per_ha"] = [0, -50, "-999", " ", "?", 90000, -1, 0, "N/A", 3]
    df.loc[idx[10:20], "farm_size_unit"] = rng.choice(["Ha", "hectares", "M²", "sqm", "acre", "Acres"], size=10)
    df.loc[idx[20:30], "season"] = rng.choice(["a", "Season A", "SEASON-A", "b", "Season B", "season c"], size=10)
    df.loc[idx[30:35], "planting_date"] = ["12/10/2024", "March 3, 2025", "45210", "31/13/2024", "2099-01-01"]
    df.loc[idx[35:40], "soil_ph"] = [0, 14, 55, -3, "unknown"]
    df.loc[idx[40:45], "avg_temp_c"] = [250, -12, 70, "N/A", 42]
    df.loc[idx[45:50], "rainfall_mm"] = [-10, 99999, " ", "NA", 4200]
    df.loc[idx[50:55], "irrigation"] = ["y", "1", "true", "n", "0"]
    df.loc[idx[55:60], "district"] = ["Huye ", "huye", "HUYE", " Nyagatare", "NYAGATARE"]
    df.loc[idx[60:65], "province"] = ["Eastern", "Southern", "Western", "Northern", "Eastern"]
    df.loc[idx[65:70], "farm_size"] = ["1,200", "2.5 ha", "30000", "-1", "0"]
    df.loc[idx[70:75], "fertilizer_kg"] = ["1,200 kg", "-20", "unknown", 0, 9999]
    df.loc[idx[75:80], "farmer_age"] = [15, 120, "-1", "N/A", 17]

    # duplicates and near duplicates
    df = pd.concat([df, df.iloc[:12]], ignore_index=True)
    d2 = df.iloc[20:28].copy()
    d2["farm_id"] = d2["farm_id"].str.lower() + " "
    d2["yield_kg_per_ha"] = pd.to_numeric(d2["yield_kg_per_ha"], errors="coerce").fillna(0) + 40
    df = pd.concat([df, d2], ignore_index=True)

    return df


def main(output_path):
    df = make()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Wrote stand-in dataset: {output_path} | shape={df.shape}")


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "q1_maize_yield/data/raw/maize_yield_rwanda_SYNTHETIC_STANDIN.csv"
    main(out)
