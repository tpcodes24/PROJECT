import os
import subprocess

# Path to your folder with FASTQ files
input_dir = "/Users/tejasreeparasa/YACHT/Downloads"
output_dir = os.path.join(input_dir, "sketches")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List all .fastq.gz files in the input directory
fastq_files = [f for f in os.listdir(input_dir) if f.endswith(".fastq.gz")]

# Sketch each sample
for fastq_file in fastq_files:
    input_path = os.path.join(input_dir, fastq_file)
    output_file = os.path.join(output_dir, f"sample_{fastq_file.replace('.fastq.gz', '')}.sig.zip")
    
    print(f"🧬 Sketching {fastq_file} ...")
    
    result = subprocess.run([
        "yacht", "sketch", "sample",
        "--infile", input_path,
        "--kmer", "31",
        "--scaled", "1000",
        "--outfile", output_file
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to sketch {fastq_file}:\n{result.stderr}")
    else:
        print(f"✅ Finished: {output_file}")
