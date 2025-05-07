import pandas as pd
import os
import urllib.request

# ---- Step 1: Download updated IBDMDB metadata ----
metadata_url = "https://ibdmdb.org/tunnel/public/HMP2/metadata/hmp2_metadata.csv"
metadata_file = "hmp2_metadata.csv"

if not os.path.exists(metadata_file):
    print("📥 Downloading IBDMDB metadata...")
    urllib.request.urlretrieve(metadata_url, metadata_file)
    print("✅ Metadata downloaded.")

# ---- Step 2: Load your YACHT-detected microbes ----
print("🔍 Loading detected YACHT microbes...")
yacht_path = "detected_organisms_by_sample.tsv"
yacht_df = pd.read_csv(yacht_path, sep="\t")
sample_names = yacht_df["sample_name"].astype(str).unique()

# ---- Step 3: Load and match metadata ----
print("📊 Processing metadata and matching samples...")
meta_df = pd.read_csv(metadata_file, dtype=str)
meta_df.columns = meta_df.columns.str.strip()  # Ensure no hidden whitespace
meta_filtered = meta_df[meta_df["external_sample_id"].isin(sample_names)]

# ---- Step 4: Map diagnosis to healthy/diseased ----
label_map = {
    "nonIBD": "healthy",
    "UC": "diseased",
    "CD": "diseased"
}
meta_filtered["label"] = meta_filtered["diagnosis"].map(label_map)

# ---- Step 5: Save labels ----
output_file = "sample_labels.tsv"
meta_filtered[["external_sample_id", "diagnosis", "label"]].dropna().to_csv(output_file, sep="\t", index=False)
print(f"✅ Sample labels written to: {output_file}")
