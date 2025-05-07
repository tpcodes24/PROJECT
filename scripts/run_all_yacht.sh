#!/bin/bash

# Define paths
CONFIG_JSON="/Users/tejasreeparasa/YACHT/scripts/gtdb_pretrained_0.95/gtdb-rs214-reps.k31_0.95_pretrained/gtdb-rs214-reps.k31_0.95_config.json"
SKETCH_DIR="/Users/tejasreeparasa/YACHT/Downloads/sketches"
RESULT_DIR="/Users/tejasreeparasa/YACHT/scripts/results"

# Make sure result directory exists
mkdir -p "$RESULT_DIR"

# Loop through all .sig.zip files in the sketch directory
for file in "$SKETCH_DIR"/*.sig.zip; do
    # Extract just the filename without extension for result naming
    base=$(basename "$file" .sig.zip)
    
    echo "Running YACHT for $base..."
    
    yacht run \
      --json "$CONFIG_JSON" \
      --sample_file "$file" \
      --significance 0.99 \
      --num_threads 4 \
      --keep_raw \
      --min_coverage_list 1 0.5 0.2 0.1 \
      --out "$RESULT_DIR/${base}_result.xlsx"
    
    echo "Done with $base"
done
