import pandas as pd

# Load a result file
xlsx_path = "/Users/tejasreeparasa/YACHT/scripts/results/sample_206534_result.xlsx"
df = pd.read_excel(xlsx_path, sheet_name="min_coverage0.2")

# Extract genome IDs from organism_name
df["genome_id"] = df["organism_name"].str.extract(r"(GCF_\d+\.\d+)")

# Load your genome_to_taxid
taxid_df = pd.read_csv("/Users/tejasreeparasa/YACHT/scripts/genome_to_taxid_final.tsv", sep="\t")

# Remove "_genomic" if present to normalize
taxid_df["genome_id_clean"] = taxid_df["genome_id"].str.replace("_genomic", "", regex=False)

# Compare which genome IDs are not in taxid file
unmatched = df[~df["genome_id"].isin(taxid_df["genome_id_clean"])]
print(f"🧬 Total unmatched genomes: {len(unmatched)} / {len(df)}")
print(unmatched[["organism_name", "genome_id"]].head(10))
