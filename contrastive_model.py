import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, roc_auc_score

# Load trimmed MKG data
edges_df = pd.read_csv("/Users/tejasreeparasa/MetagenomicKG-1/data/merged_KG/MetagenomicKG/KG_edges.tsv", sep='\t', nrows=1000)
nodes_df = pd.read_csv("/Users/tejasreeparasa/MetagenomicKG-1/data/merged_KG/MetagenomicKG/KG_nodes.tsv", sep='\t')

# Create node index mapping
unique_nodes = pd.unique(edges_df[['source_node', 'target_node']].values.ravel())
node_to_idx = {node: i for i, node in enumerate(unique_nodes)}

# Convert edges to indices
edge_index = torch.tensor([
    [node_to_idx[src] for src in edges_df['source_node']],
    [node_to_idx[tgt] for tgt in edges_df['target_node']]
], dtype=torch.long)

# Create dummy features (one-hot encoding)
x = torch.eye(len(node_to_idx))  # One-hot vector for each node

# Assign dummy labels based on node type
labels = torch.full((len(node_to_idx),), -1, dtype=torch.long)
healthy_indices = []
diseased_indices = []

for _, row in nodes_df.iterrows():
    node = row["node_id"]
    if node not in node_to_idx:
        continue
    idx = node_to_idx[node]
    if "OrganismTaxon" in row["node_type"]:
        labels[idx] = 0
        healthy_indices.append(idx)
    elif "Disease" in row["node_type"]:
        labels[idx] = 1
        diseased_indices.append(idx)

# Use only the first 10 of each type for a balanced mini-dataset
healthy_indices = healthy_indices[:10]
diseased_indices = diseased_indices[:10]
train_indices = healthy_indices + diseased_indices
labels = labels.clone()
train_labels = labels[train_indices]

# Create PyG Data object
data = Data(x=x, edge_index=edge_index)

# Define GCN model
class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

model = GCN(in_channels=data.num_features, hidden_channels=32, out_channels=2)

# Train the model
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
model.train()
for epoch in range(50):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = F.cross_entropy(out[train_indices], train_labels)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 10 == 0 or epoch == 0:
        print(f"Epoch {epoch+1:2d} | Loss: {loss.item():.4f}")

# Evaluate
model.eval()
with torch.no_grad():
    logits = model(data.x, data.edge_index)[train_indices]
    preds = torch.argmax(logits, dim=1)
    acc = accuracy_score(train_labels.numpy(), preds.numpy())
    probs = F.softmax(logits, dim=1)[:, 1].numpy()
    auc = roc_auc_score(train_labels.numpy(), probs)
    print("\nEvaluation:")
    print(f"Accuracy: {acc:.4f}")
    print(f"AUC: {auc:.4f}")
    print("Predictions:", preds.numpy())
    print("True labels:", train_labels.numpy())
