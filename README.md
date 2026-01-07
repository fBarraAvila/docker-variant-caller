# Docker Variant Caller Pipeline 🧬

A containerized bioinformatics pipeline that automates the alignment and variant calling of DNA sequencing data.

## 🏗 Architecture

This project runs a full standard pipeline using Docker to ensure reproducibility across any OS (Mac/Linux/Windows).

**Tools Used:**
- **BWA:** For aligning reads to the reference genome.
- **Samtools:** For processing, sorting, and indexing alignment files.
- **Bcftools:** For calling variants (SNP/Indel detection).
- **Python:** Orchestrates the pipeline logic with idempotency checks.

## 🚀 How to Run

### 1. Prerequisites
- Docker Desktop installed.
- Git.

### 2. Setup
Clone the repository:
```bash
git clone [https://github.com/fBarraAvila/docker-variant-caller.git](https://github.com/fBarraAvila/docker-variant-caller.git)
cd docker-variant-caller
```

### 3. Data Preparation
*Note: Genomic data is large and is not included in this repository. You must provide it.*

1. Create a `data` folder in the project root.
2. Inside `data`, create two subfolders: `reads` and `reference`.
3. Place your reference genome (`reference.fasta`) in `data/reference/`.
4. Place your FASTQ files (`reads_1.fastq.gz`, `reads_2.fastq.gz`) in `data/reads/`.

### 4. Build the Image
Build the Docker container with this command:
```bash
docker build -t variant-caller .
```

### 5. Run the Pipeline
This command mounts your local data folder into the container and executes the pipeline:

```bash
docker run --rm --platform=linux/amd64 \
  -v "$(pwd):/app" \
  -v "$(pwd)/data":/data \
  variant-caller:latest \
  python main.py
```

## 📂 Output
Results will appear in your local `data/` folder:
- `aligned.sorted.bam` (Aligned & sorted reads)
- `variants.vcf` (Final mutation calls)