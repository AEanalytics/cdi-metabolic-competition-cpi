# cdi-metabolic-competition-cpi
Investigating the Colonization Dynamics of Clostridioides difficile through Metabolic Niche Competition in Human and Animal Gut Microbiomes

CPI Framework for Predicting Microbial Competition Against Clostridioides difficile
Overview

This repository contains the computational framework developed as part of the Master's thesis:

"Investigating the Colonization Dynamics of Clostridioides difficile through Metabolic Niche Competition in Human and Animal Gut Microbiomes"

The project introduces a pathway-based computational method for predicting microbial species capable of competing with Clostridioides difficile through amino acid metabolic overlap.

The framework calculates a Competitive Potential Index (CPI) based on KEGG Ortholog pathway completeness across fourteen amino acid metabolic pathways associated with Clostridioides difficile physiology and Stickland fermentation.

#Objectives
Identify amino acid pathways essential to Clostridioides difficile
Quantify metabolic overlap between gut microbial species
Calculate Competitive Potential Index (CPI)
Generate heatmaps and radar plots for comparative analysis
Support functional microbiome analysis and probiotic candidate screening

#Features
KEGG Ortholog mapping
Pathway completeness scoring
CPI calculation
Automated visualization generation
Comparative metabolic analysis
Reproducible workflow
Workflow
Genome acquisition from NCBI
Quality control
Functional annotation using eggNOG-mapper
KEGG Ortholog extraction
Amino acid pathway reconstruction
CPI calculation
Visualization and reporting
Amino Acids Included

The framework evaluates overlap across the following amino acids:

Proline
Glycine
Leucine
Isoleucine
Valine
Arginine
Asparagine
Glutamate
Glutamine
Histidine
Lysine
Methionine
Threonine
Cysteine

Example Output

Outputs include:

CPI score tables
Heatmaps
Radar plots
Comparative pathway reports
BRIG genome comparison visualizations
Scientific Significance

This framework provides:

Functional interpretation of colonization resistance
A computational approach to microbiome competition analysis
A scalable method for probiotic candidate identification
A metabolism-centered alternative to taxonomic profiling
Citation

If you use this repository, please cite:

Abimbola Ebenezer, Anastasia Kholodnaya. Investigating the Colonization Dynamics of Clostridioides difficile through Metabolic Niche Competition in Human and Animal Gut Microbiomes. Master's Thesis. 2026.
