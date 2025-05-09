# PROJECT

This project applies contrastive learning on microbiome data to identify latent patterns between microbe-disease linkages using the Metagenomic Knowledge Graph (MKG).

1. The microbiome samples are processed to extract organism data. Over 30 microbiome samples were used for organism detection.
   
2. The organism data is extracted from YACHT's result files and saved into `detected_organisms_by_sample.csv`.

3. The detected organisms (via TaxID) are mapped to corresponding nodes in the MKG using the script `overlay_by_accession_taxid.py`. This process results in the `overlay_by_taxid.tsv` file, which contains the mappings.

4. Subgraphs are constructed for individual microbiome samples, and contrastive learning is applied to distinguish between healthy and diseased samples. This task is handled by the `contrastive_model.py` script, which uses a Graph Convolutional Network (GCN) to process the data.

5. The graph is constructed with data from the MKG and the microbiome samples. The GCN model is trained on these subgraphs to classify them as either healthy or diseased.

6. The project has encountered challenges such as limited sample size, lack of reliable disease labels, and difficulty in mapping some organisms to MKG nodes. These issues restrict the model’s performance and generalization.

Files Overview:
- `contrastive_model.py`: Implements the contrastive learning model with a GCN to classify subgraphs as healthy or diseased.
- `final_model.py`: Contains the trained model, which is used for inference on new microbiome data.
- `detected_organisms_by_sample.csv`: Contains the list of detected organisms for each microbiome sample.
- `overlay_by_accession_taxid.py`: Used to map detected organisms to MKG nodes based on accession and TaxID.
- `overlay_by_taxid.tsv`: Output file containing the organism-to-MKG-node mappings.
- `overlay_debug_matches.tsv`: Debug file tracking the matches of organisms between YACHT results and MKG nodes.
- `overlay_detected_microbes.py`: Script for validating and debugging the overlay process.
- `sample_labels.py`: Script for labeling samples as healthy or diseased for use in contrastive learning.
