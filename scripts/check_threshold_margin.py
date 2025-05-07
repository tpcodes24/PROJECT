import pandas as pd
import os

RESULTS_DIR = "/Users/tejasreeparasa/YACHT/scripts/results"
SHEET_NAME = "min_coverage0.2"

for file in os.listdir(RESULTS_DIR):
    if file.endswith(".xlsx") and file.startswith("sample_"):
        sample_path = os.path.join(RESULTS_DIR, file)
        sample_name = file.replace("_result.xlsx", "")
        print(f"\n🔍 Sample: {sample_name}")

        try:
            df = pd.read_excel(sample_path, sheet_name=SHEET_NAME)
            df["margin"] = df["num_matches"] - df["acceptance_threshold_wo_coverage"]
            df_sorted = df.sort_values(by="margin", ascending=False)

            close = df_sorted[df_sorted["margin"] > -10]  # adjust threshold
            if not close.empty:
                print(f"🧬 Closest organisms to being detected:")
                print(close[["organism_name", "num_matches", "acceptance_threshold_wo_coverage", "margin"]].head(5))
            else:
                print("❌ No organisms came close to detection.")
        except Exception as e:
            print(f"⚠️ Could not process {sample_name}: {e}")
