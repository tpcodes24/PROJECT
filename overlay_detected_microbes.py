import pandas as pd
import ast

# Define paths
MKG_NODES = "data/merged_KG/MetagenomicKG/KG_nodes.tsv"
YACHT_FILE = "detected_organisms_by_sample.tsv"
OUTPUT_FILE = "overlay_by_taxid.tsv"

# Load MKG node data
print("🔍 Loading MKG node table...")
node_df = pd.read_csv(MKG_NODES, sep="\t", usecols=["node_id", "node_type", "description"])
node_df = node_df[node_df["node_type"] == "biolink:OrganismTaxon"]

# Extract taxid from the tuple-like description field
def extract_taxid(description):
    try:
        parsed = ast.literal_eval(description)
        for tup in parsed:
            if isinstance(tup, tuple) and "taxid" in tup[0].lower():
                return tup[1]
    except Exception:
        return None
    return None

node_df["taxid"] = node_df["description"].apply(extract_taxid)
node_df = node_df.dropna(subset=["taxid"])
node_df["taxid"] = node_df["taxid"].astype(str)

print(f"✅ MKG nodes with taxid: {len(node_df)}")

# Load detected microbes
print("🔍 Loading YACHT results...")
yacht_df = pd.read_csv(YACHT_FILE, sep="\t")

# Try to extract taxid from organism_name using regex (if embedded)
yacht_df["taxid"] = yacht_df["organism_name"].str.extract(r'taxid[ =:](\d+)')[0]
# If not, fallback to accession string (GCF/GCA)
yacht_df["accession"] = yacht_df["organism_name"].str.extract(r"(GCF|GCA)_\d+\.\d+")[0]

# Merge on taxid
matched_df = yacht_df.merge(node_df, on="taxid", how="inner")

# Save result
matched_df[["sample_name", "organism_name", "min_coverage", "taxid", "node_id"]].to_csv(OUTPUT_FILE, sep="\t", index=False)
print(f"Overlay complete. {len(matched_df)} matched rows written to {OUTPUT_FILE}")
