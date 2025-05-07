import os
import subprocess

# Paths
sample_sketch_dir = "/Users/tejasreeparasa/YACHT/sample_sketches"
ref_json = "/Users/tejasreeparasa/YACHT/ref_pretrained/gtdb_rs214_k31_ani_0.9995_config.json"
output_dir = "/Users/tejasreeparasa/YACHT/yacht_results"
threads = "8"  # Adjust 

os.makedirs(output_dir, exist_ok=True)

# Loop through all sample signatures
for filename in os.listdir(sample_sketch_dir):
    if filename.endswith(".sig.zip"):
        sample_path = os.path.join(sample_sketch_dir, filename)
        sample_id = os.path.splitext(os.path.basename(filename))[0]
        output_file = os.path.join(output_dir, f"{sample_id}_result.xlsx")

        cmd = [
            "yacht", "run",
            "--json", ref_json,
            "--sample_file", sample_path,
            "--num_threads", threads,
            "--keep_raw",
            "--significance", "0.99",
            "--min_coverage_list", "1", "0.6", "0.2", "0.1",
            "--out", output_file
        ]

        print(f"🔬 Running YACHT on {sample_id}...")
        subprocess.run(cmd, check=True)

print(" All samples processed. Results saved to:", output_dir)
