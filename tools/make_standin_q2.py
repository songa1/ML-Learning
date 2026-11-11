from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42

SCHOOLS = [
    ("Huye Science School", "Huye", "Southern", "public", "Boarding"),
    ("Groupe Scolaire Nyanza", "Nyanza", "Southern", "government-aided", "Day"),
    ("Gisagara College", "Gisagara", "Southern", "private", "Boarding"),
    ("Nyamagabe Secondary", "Nyamagabe", "Southern", "public", "Day"),
    ("Muhanga Academy", "Muhanga", "Southern", "private", "Boarding"),
    ("Kigali Scholars School", "Nyarugenge", "Kigali City", "private", "Boarding"),
    ("Musanze Technical School", "Musanze", "Northern", "government-aided", "Day"),
    ("Rubavu College", "Rubavu", "Western", "public", "Boarding"),
]

COMBINATIONS = ["MPC", "PCB", "MCB", "MEG", "HEG", "HEL", "LEG", "TVET"]


def make(n=1200, seed=SEED):
    rng = np.random.default_rng(seed)
    records = []
    for index in range(n):
        school_id, district, province, school_type, boarding = SCHOOLS[int(rng.integers(len(SCHOOLS)))]
        age = int(rng.integers(15, 20))
        gender = rng.choice(["Female", "Male"], p=[0.52, 0.48])
        aggregate = int(np.clip(rng.normal(48, 12), 20, 72))
        math = int(np.clip(rng.normal(aggregate / 7, 1.6), 1, 9))
        english = int(np.clip(rng.normal(aggregate / 7, 1.5), 1, 9))
        science = int(np.clip(rng.normal(aggregate / 7, 1.7), 1, 9))
        combination = rng.choice(COMBINATIONS)
        size = int(rng.integers(250, 1800))
        ratio = round(float(np.clip(rng.normal(34, 8), 15, 65)), 1)
        labs = rng.choice(["Yes", "No"], p=[0.72, 0.28], size=3)
        tuition = int(np.clip(rng.normal(115000, 55000), 25000, 300000))
        boarding_fee = int(np.clip(rng.normal(175000, 70000), 0, 400000)) if boarding == "Boarding" else 0
        distance = round(float(np.clip(rng.lognormal(2.0, 0.8), 1, 80)), 1)
        pass_rate = round(float(np.clip(rng.normal(0.68, 0.14), 0.25, 0.98)), 3)
        scholarship = rng.choice(["Yes", "No"], p=[0.18, 0.82])
        expected = 42 + (72 - aggregate) * 0.34 + (science == "Yes") * 2
        expected += (school_type == "private") * 2 + (boarding == "Boarding") * 1.5
        expected -= distance * 0.05 + (ratio - 30) * 0.15
        result = round(float(np.clip(expected + rng.normal(0, 7), 20, 80)), 1)
        records.append([
            f"S{index:05d}", school_id[:4].upper(), school_id, district, province, gender, age,
            aggregate, math, english, science, school_type, boarding, size, ratio,
            labs[0], labs[1], labs[2], tuition, boarding_fee, distance, combination,
            pass_rate, scholarship, result,
            round(float(np.clip(result + rng.normal(0, 3), 0, 100)), 1),
            rng.choice(["Admitted", "Not admitted"], p=[0.42, 0.58]),
            rng.choice(["Yes", "No"], p=[0.08, 0.92]),
        ])

    columns = [
        "student_record_id", "school_id", "school_name", "district", "province", "gender", "age",
        "s3_aggregate", "math_grade", "english_grade", "science_grade", "school_type", "boarding_day",
        "school_size", "student_teacher_ratio", "science_lab", "ict_lab", "library", "tuition_fee",
        "boarding_fee", "distance_km", "combination", "previous_year_pass_rate", "scholarship_flag",
        "alevel_total_points", "alevel_subject_points", "university_admission", "repeat_year",
    ]
    frame = pd.DataFrame(records, columns=columns)

    # Keep raw quality problems for the future Q2 audit and cleaning stages.
    issue_rows = rng.choice(frame.index, size=48, replace=False)
    for column in ["age", "tuition_fee", "distance_km"]:
        frame[column] = frame[column].astype(object)
    frame.loc[issue_rows[:8], "school_name"] = frame.loc[issue_rows[:8], "school_name"].str.lower() + " "
    frame.loc[issue_rows[8:16], "district"] = ["huye ", "HUYE", "Nyanza", "nyanza", "Gisagara ", "MUHANGA", "Rubavu ", "musanze"]
    frame.loc[issue_rows[16:24], "age"] = [14, 21, 99, -1, "N/A", 17, 120, "unknown"]
    frame.loc[issue_rows[24:32], "tuition_fee"] = ["120,000", "N/A", -1, "250000 RWF", 0, "unknown", 9999999, " "]
    frame.loc[issue_rows[32:40], "distance_km"] = [0, -3, 250, "N/A", "12 km", 999, "unknown", " "]
    frame.loc[issue_rows[40:48], "combination"] = ["Mpc", "pcb", "MEG ", "unknown", "TVET", "LEG", "HEG", "HEL"]
    frame = pd.concat([frame, frame.iloc[:12]], ignore_index=True)
    return frame


def main(output_path=None):
    output = Path(output_path or "q2_own_scenario/data/raw/q2_student_school_combination_SYNTHETIC_TEST.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    frame = make()
    frame.to_csv(output, index=False)
    print(f"Wrote synthetic Q2 test data: {output} | shape={frame.shape} | seed={SEED}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else None)