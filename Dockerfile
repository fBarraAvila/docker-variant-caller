# 1. Base Image
FROM --platform=linux/amd64 continuumio/miniconda3:4.12.0

# 2. Set the working directory
WORKDIR /app

# 3. Install the tools
# -c bioconda: Look in the biology channel
# -c conda-forge: Look in the community channel (for dependencies)
# We pin versions (e.g., =0.7.17) to ensure this works forever.
RUN conda install -y -c bioconda -c conda-forge \
    bwa=0.7.17 \
    samtools=1.14 \
    bcftools=1.14 \
    && conda clean -a -y

# 4. Default command
CMD ["bash"]