import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === Load Knowledge Graph Data ===
print("Loading MKG...")

edges_path = "data/merged_KG/MetagenomicKG/KG_edges.tsv"
nodes_path = "data/merged_KG/MetagenomicKG/KG_nodes.tsv"

edges_df = pd.read_csv(edges_path, sep='\t')
nodes_df = pd.read_csv(nodes_path, sep='\t')

print("Columns in edges file:", edges_df.columns.tolist())
print("Columns in nodes file:", nodes_df.columns.tolist())

# === Build Graph ===
print("Building graph...")
G = nx.from_pandas_edgelist(
    edges_df,
    source="source_node",
    target="target_node",
    edge_attr="predicate",
    create_using=nx.MultiDiGraph()
)

# === Attach Node Attributes ===
if "node_id" in nodes_df.columns and "node_type" in nodes_df.columns:

    node_types = dict(zip(nodes_df["node_id"], nodes_df["node_type"]))

    nx.set_node_attributes(G, node_types, "category")
else:
    print("Error: Cannot find 'node_id' and 'category' columns in node file.")

# === Basic Graph Stats ===
print(f"Graph has {G.number_of_nodes():,} nodes and {G.number_of_edges():,} edges")

# === Node Type Counts ===
node_type_counts = pd.Series(nx.get_node_attributes(G, "category")).value_counts()
print("\nNode type counts:")
print(node_type_counts)

# === Optional Visualization of Top 10 Node Types ===
plt.figure(figsize=(10, 5))
node_type_counts = pd.Series(list(node_types.values())).value_counts()

plt.title("Top 10 Node Types in MetagenomicKG")
plt.xlabel("Node Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("node_type_distribution.png")
print("\nSaved bar chart of top 10 node types as 'node_type_distribution.png'")