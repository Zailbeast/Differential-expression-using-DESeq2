#!/usr/bin/env Rscript

# DESeq2 Analysis Script for RNA-seq Data
# Author: Huzail Shaikh
# Date: 04/05/2025

# ----------------------------
# Load Required Packages and Parse Arguments
# ----------------------------

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 5) {
  stop("Usage: Rscript deseq2_analysis.R <counts_file> <metadata_file> <condition_column> <control_group> <treatment_group> <output_dir>")
}

counts_file <- args[1]
metadata_file <- args[2]
condition_column <- args[3]
control_group <- args[4]
treatment_group <- args[5]
output_dir <- ifelse(length(args) >= 6, args[6], "results")

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

packages <- c("DESeq2")
for (pkg in packages) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
        BiocManager::install(pkg)
    }
    library(pkg, character.only = TRUE)
}

check_files <- function(counts_file, metadata_file) {
    if (!file.exists(counts_file)) stop(paste("Counts file not found:", counts_file))
    if (!file.exists(metadata_file)) stop(paste("Metadata file not found:", metadata_file))
}

run_deseq2 <- function(counts_file, metadata_file, condition_column, control_group, 
                       treatment_group, output_dir = "results") {
    check_files(counts_file, metadata_file)

    if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

    counts <- read.csv(counts_file, row.names = 1, check.names = FALSE)
    metadata <- read.csv(metadata_file, row.names = 1, sep = "\t")

    if (!all(colnames(counts) %in% rownames(metadata))) {
        stop("Sample names in counts file do not match metadata file")
    }

    counts <- counts[, rownames(metadata)]

    dds <- DESeqDataSetFromMatrix(countData = counts,
                                  colData = metadata,
                                  design = as.formula(paste("~", condition_column)))

    dds[[condition_column]] <- relevel(dds[[condition_column]], ref = control_group)
    dds <- DESeq(dds)

    res <- results(dds, contrast = c(condition_column, treatment_group, control_group))
    res$gene <- rownames(res)
    write.csv(as.data.frame(res), file = file.path(output_dir, "differential_expression_results.csv"))

    return(list(results = res, dds = dds))
}

result <- run_deseq2(counts_file, metadata_file, condition_column, control_group, treatment_group, output_dir)

sessionInfo()
