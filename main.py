import subprocess
import sys
import os

def run_command(command):
   """Runs a shell command and prints the output. """
   try:
      # We use subprocess.run to excute the command inside the linux environement 
      result = subprocess.run(
         command,
         shell=True,
         check=True,
         stdout=subprocess.PIPE,
         stderr=subprocess.PIPE,
         text=True
      )
      print(f"✅ Success: '{command}'")
      return result.stdout
   
   except subprocess.CalledProcessError as e:
        print(f"❌ Error running '{command}':")
        print(e.stderr)
        sys.exit(1)

def run_if_missing(output_path, command, step_name):
    # Only run the command if the output file is mising.

    print(f"\n[{step_name}] Checking output...")

    # Python checks if the file exist inside the container
    if os.path.exists(output_path):
        print(f"    -> Output found: {output_path}")
        print(" -> Skipping step.")
    else:
        print(f"    -> Output NOT found. Running command...")
        run_command(command)

# ---------------------------------------------------------
# PIPELINE CONFIGURATION
# ---------------------------------------------------------

REF_FILE = "/data/reference/reference.fasta"
READS_1 = "/data/reads/reads_1.fastq.gz"
READS_2 = "/data/reads/reads_2.fastq.gz"

SAM_FILE = "/data/aligned.sam"
SORTED_BAM = "/data/aligned.sorted.bam"
VCF_FILE = "/data/variants.vcf"

print("--- Starting Pipeline ---")

# ---------------------------------------------------------
# Step 1: Indexing
# ---------------------------------------------------------
# BWA creates multiple files (.bwt, .pac), we check for one of them.
run_if_missing(
    output_path=f"{REF_FILE}.bwt",
    command=f"bwa index {REF_FILE}",
    step_name="Step 1: Indexing Genome"
)

# ---------------------------------------------------------
# Step 2: Alignment
# ---------------------------------------------------------
align_cmd = f"bwa mem -t 4 {REF_FILE} {READS_1} {READS_2} > {SAM_FILE}"

run_if_missing(
    output_path=SAM_FILE,
    command=align_cmd,
    step_name="Step 2: Alignment (BWA)"
)

# ---------------------------------------------------------
# Step 3: Processing (SAM -> BAM -> Sort)
# ---------------------------------------------------------
# We combine conversion and sorting into one pipeline
process_cmd = f"samtools view -S -b {SAM_FILE} | samtools sort -o {SORTED_BAM}"

run_if_missing(
    output_path=SORTED_BAM,
    command=process_cmd,
    step_name="Step 3: Sorting & Compression"
)

# ---------------------------------------------------------
# Step 3.5: Indexing the BAM
# ---------------------------------------------------------
# Samtools index creates a .bai file
run_if_missing(
    output_path=f"{SORTED_BAM}.bai",
    command=f"samtools index {SORTED_BAM}",
    step_name="Step 3.5: Indexing BAM"
)

# ---------------------------------------------------------
# Step 4: Variant Calling
# ---------------------------------------------------------
print("\n[Step 4] Calling Variants...")

vcf_cmd = f"bcftools mpileup -f {REF_FILE} {SORTED_BAM} | bcftools call -mv -O v -o {VCF_FILE}"

run_if_missing(
    output_path=VCF_FILE,
    command= vcf_cmd,
    step_name= "Step 4 Variant Calling"
)

print("\n--- Pipeline Complete ---")
