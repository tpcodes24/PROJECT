import pandas as pd
import os
import re

RESULTS_DIR = "/Users/tejasreeparasa/YACHT/scripts/results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "detected_organisms_by_sample.tsv")

with open(OUTPUT_FILE, "w") as f_out:
    f_out.write("sample_name\torganism_name\tmin_coverage\n")

    for file in os.listdir(RESULTS_DIR):
        if file.endswith(".xlsx") and file.startswith("206"):
            sample_path = os.path.join(RESULTS_DIR, file)
            sample_name = file.replace("_result.xlsx", "")
            try:
                xls = pd.ExcelFile(sample_path)
                for sheet_name in xls.sheet_names:
                    if re.match(r"min_coverage[0-9.]+", sheet_name):
                        df = pd.read_excel(sample_path, sheet_name=sheet_name)
                        if "in_sample_est" in df.columns:
                            detected = df[df["in_sample_est"] == True]
                            for org in detected["organism_name"]:
                                f_out.write(f"{sample_name}\t{org}\t{sheet_name}\n")
            except Exception as e:
                print(f"⚠️ Could not process {sample_name}: {e}")
