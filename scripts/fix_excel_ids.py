import pandas as pd

# Path to your result file
excel_path = "/Users/tejasreeparasa/YACHT/scripts/results/sample_206534_result.xlsx"
sheet = "min_coverage0.2"
fixed_excel_path = "/Users/tejasreeparasa/YACHT/scripts/results/sample_206534_result_FIXED.xlsx"

# Load Excel file
df = pd.read_excel(excel_path, sheet_name=sheet)

# Extract the first word (genome ID) and add _genomic
df["genome_id"] = df["organism_name"].str.extract(r"^(GCF_\d+\.\d+|GCA_\d+\.\d+)")[0] + "_genomic"

# Save the modified Excel file
with pd.ExcelWriter(fixed_excel_path) as writer:
    df.to_excel(writer, index=False, sheet_name=sheet)

print(f"✅ Saved fixed file to: {fixed_excel_path}")
