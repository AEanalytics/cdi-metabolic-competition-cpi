![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Bioinformatics](https://img.shields.io/badge/field-bioinformatics-orange)
![Biotechnology](https://img.shields.io/badge/field-biotechnology-purple)

## Overview

This repository contains the computational framework developed for the Master's thesis:

"Investigating the Colonization Dynamics of _Clostridioides difficile_ through Metabolic Niche Competition in Human and Animal Gut Microbiomes"

The project introduces a pathway-based computational method for predicting microbial species capable of competing with _Clostridioides difficile_ through amino acid metabolic overlap.

The framework calculates a Competitive Potential Index (CPI) using KEGG Ortholog pathway completeness across amino acid pathways associated with _Clostridioides difficile_ metabolism.

## Biological Background

_Clostridioides difficile_ is a major cause of hospital-acquired infectious diarrhea and recurrent gastrointestinal disease(Laura et al., 2025).While bile acid metabolism and immune modulation have been widely studied as mechanisms of colonization resistance, amino acid competition remains comparatively underexplored. This project investigates whether microbial species with overlapping amino acid metabolic capabilities may reduce nutrient availability for _C. difficile_ and contribute to colonization resistance.

## Objectives

- Identify amino acids essential to _C. difficile_ metabolism
- Quantify metabolic overlap between microbial species
- Develop a Competitive Potential Index (CPI)
- Generate comparative visualizations
- Support microbiome-based therapeutic research

## Workflow

1. Genome acquisition from NCBI
2. Functional annotation using eggNOG-mapper
3. KEGG Ortholog extraction
4. Amino acid pathway reconstruction
5. CPI calculation
6. Visualization and reporting

## Amino Acids Included

The framework evaluates overlap across the following amino acids:

- Proline
- Glycine
- Leucine
- Isoleucine
- Valine
- Arginine
- Asparagine
- Glutamate
- Glutamine
- Histidine
- Lysine
- Methionine
- Threonine
- Cysteine

## Installation

### Clone Repository

```bash
git clone https://github.com/AEanalytics/cdi-metabolic-competition-cpi.git
cd cdi-metabolic-competition-cpi
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run CPI Pipeline

```bash
python Report_generator_script/Report_generator.py
```

### Generate Visualizations

```bash
python Report_generator_script/visualization_suite.py
```

## Outputs

The framework generates:

- CPI score tables
- Heatmaps
- Radar plots
- Comparative pathway reports

## Scientific Significance

This framework provides a functional approach for analyzing colonization resistance through metabolic competition.

The project supports:
- probiotic candidate screening
- microbiome therapeutic design
- functional metagenomics analysis
- computational microbiome research

## External Tools

The framework requires the following external bioinformatics software:

| Tool | Purpose |
|------|----------|
| eggNOG-mapper | Functional annotation and KEGG Ortholog assignment |
| BLAST+ | Sequence comparison |
| BRIG | Comparative genome visualization |

These tools should be installed separately and configured in the system PATH

### eggNOG-mapper

Functional annotation was performed using eggNOG-mapper v2.

Example command:

```bash
emapper.py -i GCA_018885085.1_ASM1888508v1_protein.faa \
--data_dir ~/eggnog_db \
--database bact \
-o C_difficile_annotations
```

## Citation

If you use this repository, please cite:

Ebenezer T. A., Anastasia K.N. Investigating the Colonization Dynamics of Clostridioides difficile through Metabolic Niche Competition in Human and Animal Gut Microbiomes. Master's Thesis. 2026.
