import pandas as pd

file = "/Users/tejasreeparasa/YACHT/scripts/results/sample_206534_result.xlsx"
sheet = "min_coverage0.2"

df = pd.read_excel(file, sheet_name=sheet)
print(df[['organism_name', 'num_matches', 'acceptance_threshold_with_coverage', 'in_sample_est']].head(20))
