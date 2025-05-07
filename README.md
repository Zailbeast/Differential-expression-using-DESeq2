# This module is for people who want or are begining to work on RNASeq data. These tools and scripts will help you achive the desired results.

Please note that these scripts will be updated as I keep making chanmges and improving the scripts to give the best of the best.

Beginner-Friendly Guide: Setting Up an RNA-Seq Workflow with DESeq2
This guide is designed for the GitHub front page of an RNA-Seq workflow repository. It aims to help beginners install and run a complete RNA-Seq analysis pipeline, including differential expression analysis with DESeq2. The steps below are based on best practices and widely used tools in the bioinformatics community

This workflow covers:

Installing all required software using Conda

Organizing your project files

Running each analysis step: quality control, trimming, alignment, quantification, and differential expression analysis with DESeq2

1. Prerequisites
Operating System: Linux (Ubuntu 16.04+ recommended)

Admin Rights: May need sudo privileges for some installations

Command Line Skills: Basic familiarity with terminal commands

2. Installation Using Conda
Install Miniconda (if not already installed):

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Create and activate an RNA-Seq environment:

```bash
conda create -n rnaseq -c bioconda -c conda-forge fastqc trimmomatic star subread samtools multiqc salmon htseq
conda activate rnaseq
```

Install R and DESeq2:

```bash
conda create -n deseq2_env -c conda-forge -c bioconda r-base r-essentials bioconductor-deseq2
conda activate deseq2_env
#You can install all tools in a single environment, but using separate environments is recommended for clarity.
```

3. Project Directory Structure
Organize your files as follows:

```text
project_root/
├── annotation/        # Genome annotation files (.GTF/.GFF)
├── genome/            # Reference genome files (.FASTA)
├── input/             # Raw FASTQ files
├── output/            # All analysis outputs
│   ├── qc/
│   ├── trimmed/
│   ├── aligned/
│   ├── counts/
│   └── deseq2/
└── scripts/           # Custom scripts and notebooks
```

4. Step-by-Step Workflow
A. Quality Control
Check the quality of your raw FASTQ files:

```bash
fastqc -o output/qc/ input/*.fastq.gz
```

B. Trimming
Trim adapters and low-quality bases:

```bash
trimmomatic PE input/sample_R1.fastq.gz input/sample_R2.fastq.gz \
  output/trimmed/sample_R1_paired.fastq.gz output/trimmed/sample_R1_unpaired.fastq.gz \
  output/trimmed/sample_R2_paired.fastq.gz output/trimmed/sample_R2_unpaired.fastq.gz \
  ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:20 MINLEN:36
```

C. Alignment
Align reads to the reference genome:

```bash
# Generate genome index (run once)
STAR --runThreadN 4 --runMode genomeGenerate --genomeDir genome/ --genomeFastaFiles genome/genome.fa --sjdbGTFfile annotation/genes.gtf
```

# Align reads
```STAR --runThreadN 4 --genomeDir genome/ \
  --readFilesIn output/trimmed/sample_R1_paired.fastq.gz output/trimmed/sample_R2_paired.fastq.gz \
  --readFilesCommand zcat \
  --outFileNamePrefix output/aligned/sample_
```

D. Counting Reads
Count reads per gene:

```bash
featureCounts -a annotation/genes.gtf -o output/counts/gene_counts.txt output/aligned/*.bam
```

Alternatively, use HTSeq:

```bash
htseq-count -f bam -r pos -s no output/aligned/sample_Aligned.out.bam annotation/genes.gtf > output/counts/sample_counts.txt
```

E. Quality Summary
Summarize QC results:

```bash
multiqc output/qc/ -o output/qc/
```

5. Differential Expression Analysis with DESeq2
A. Prepare Count Matrix
Combine all sample count files into a single matrix (rows: genes, columns: samples).

B. Run DESeq2 in R
Start R:

```bash
R
```
Load DESeq2 and Import Data:

```r
library(DESeq2)
countData <- read.table("output/counts/gene_counts.txt", header=TRUE, row.names=1)
colData <- data.frame(
  row.names = colnames(countData),
  condition = c("control", "control", "treated", "treated") # Edit as appropriate
)
dds <- DESeqDataSetFromMatrix(countData = countData, colData = colData, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
write.csv(as.data.frame(res), file="output/deseq2/deseq2_results.csv")
```

6. Example: Running the Workflow from GitHub
You can clone this repository and follow the included README for step-by-step instructions:

```bash
git clone https://github.com/Zailbeast/Genomics-Bioinformatics-Scripts-Repository.git/
cd (Your repo)
```

7. Additional Tips
Always check the documentation for each tool for version-specific options.

Use MultiQC to quickly spot any issues in QC or alignment.

For larger projects, consider workflow managers like Snakemake or Nextflow for automation.

Getting Started

Each module contains a README file explaining its purpose, dependencies, and usage instructions. Feel free to explore, contribute, or modify scripts as needed!

_________________________________________________________________________________________

##Installation of tools##

I have provided the yaml files for these tools and you could just download these and make use of these for your pc as mentioned above. 


