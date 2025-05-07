#!/bin/bash

FASTQ_DIR="/Users/tejasreeparasa/YACHT/Downloads"
SKETCH_DIR="/Users/tejasreeparasa/YACHT/Downloads/sketches_resketched"
REF_JSON="/Users/tejasreeparasa/YACHT/scripts/gtdb_pretrained_0.95/gtdb-rs214-reps.k31_0.95_pretrained/gtdb-rs214-reps.k31_0.95_config.json"
RESULTS_DIR="/Users/tejasreeparasa/YACHT/scripts/results"

mkdir -p "$SKETCH_DIR"
mkdir -p "$RESULTS_DIR"

for fq in "$FASTQ_DIR"/*.fastq.gz; do
    sample=$(basename "$fq" .fastq.gz)
    sig_file="$SKETCH_DIR/${sample}.sig.zip"
    result_file="$RESULTS_DIR/${sample}_result.xlsx"

    # Remove existing sketch and result to avoid duplication issues
    rm -f "$sig_file"
    rm -f "$result_file"

    echo "🧬 Sketching $fq ..."
    yacht sketch sample \
        --infile "$fq" \
        --kmer 31 \
        --scaled 1000 \
        --outfile "$sig_file"

    echo "🧪 Running YACHT for $sample ..."
    yacht run \
        --json "$REF_JSON" \
        --sample_file "$sig_file" \
        --num_threads 4 \
        --keep_raw \
        --significance 0.95 \
        --min_coverage_list 0.05 0.01 0.005 \
        --out "$result_file"
done

echo "✅ Done resketching and running YACHT for all samples with scaled=100."
