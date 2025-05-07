import pandas as pd
import ast

# === File Paths ===
YACHT_TSV = "detected_organisms_by_sample.tsv"
MKG_NODES = "data/merged_KG/MetagenomicKG/KG_nodes.tsv"
ASSEMBLY_SUMMARY = "assembly_summary_refseq.txt"
OUTPUT_TSV = "overlay_by_taxid.tsv"

# === Step 1: Load YACHT results ===
print("🔍 Loading YACHT results...")
yacht_df = pd.read_csv(YACHT_TSV, sep="\t")
yacht_df["accession"] = yacht_df["organism_name"].str.extract(r"(GCF_\d+\.\d+|GCA_\d+\.\d+)")
yacht_df["accession_base"] = yacht_df["accession"].str.replace(r"\.\d+", "", regex=True)
yacht_df = yacht_df.dropna(subset=["accession_base"])
print(f" Extracted {len(yacht_df)} accessions")

# === Step 2: Load assembly summary with auto-detected header ===
print("📄 Reading NCBI assembly summary...")
asm_df = pd.read_csv(ASSEMBLY_SUMMARY, sep="\t", skiprows=1, dtype=str, low_memory=False)
assembly_col = [col for col in asm_df.columns if "assembly_accession" in col.lower()][0]
taxid_col = [col for col in asm_df.columns if "taxid" in col.lower()][0]

asm_df["accession_base"] = asm_df[assembly_col].str.replace(r"\.\d+", "", regex=True)
asm_df = asm_df[["accession_base", taxid_col]].rename(columns={taxid_col: "taxid"})

# === Step 3: Join YACHT ↔ assembly summary by accession ===
yacht_df = yacht_df.merge(asm_df, on="accession_base", how="left")
yacht_df = yacht_df.dropna(subset=["taxid"])
yacht_df["taxid"] = yacht_df["taxid"].astype(str)
print(f" Mapped to {len(yacht_df)} taxids")

# === Step 4: Load MKG nodes ===
print("📦 Loading MKG node table...")
mkg_df = pd.read_csv(MKG_NODES, sep="\t", usecols=["node_id", "node_type", "description"])
mkg_df = mkg_df[mkg_df["node_type"] == "biolink:OrganismTaxon"]

def extract_taxid(desc):
    try:
        items = ast.literal_eval(desc)
        for k, v in items:
            if "taxid" in k.lower():
                return str(v)
    except:
        return None

mkg_df["taxid"] = mkg_df["description"].apply(extract_taxid)
mkg_df = mkg_df.dropna(subset=["taxid"])

# === Step 5: Match by taxid ===
matched = yacht_df.merge(mkg_df[["taxid", "node_id"]], on="taxid", how="inner")

# === Step 6: Save
matched[["sample_name", "organism_name", "accession", "taxid", "node_id"]].to_csv(OUTPUT_TSV, sep="\t", index=False)
print(f" Found {len(matched)} matches. Saved to {OUTPUT_TSV}")
