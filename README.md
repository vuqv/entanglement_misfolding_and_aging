# Native entanglement misfolding contributes to age-associated structural changes across the *Saccharomyces cerevisiae* proteome

This repository evaluates the association between native non-covalent lasso entanglements (NCLEs) and age-associated structural changes in the yeast proteome. It includes:

- Statistical association workflows (protein-level, residue-level, and association with abundance increase)
- Coarse-grained (CG) folding and misfolding simulation workflows
- Figure-generation notebooks
- A reproducible software environment (`bioenv.yml`)

## Design choices

This project does not use a formal workflow manager (for example, Snakemake or Nextflow) because:

- The analysis flow is linear.
- Major analysis steps are deterministic and notebook-based.
- The dataset is fixed and relatively small.
- Transparency and interactivity are priorities.

Given this scope, notebook-based orchestration was chosen for readability and accessibility.

## Primary entry points


| Workflow                | Location                   | Purpose                                                                                                                                      |
| ----------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Statistical association | `statistical_association/` | Main notebooks for NCLE vs. structural-change association (odds ratios and residue-level analyses). See `statistical_association/README.md`. |
| CG simulations          | `cg_sims/`                 | Temperature-quenching workflows at 300 K, MSM analyses, and visualization. See `cg_sims/README.md`.                                          |


## Project layout

- `statistical_association/`: Association analyses, datasets, and notebooks
- `cg_sims/`: CG simulation inputs, scripts, and analysis workflows
- `bioenv.yml`: Conda environment specification

## Data overview

This project uses two primary input datasets for the association analyses.

### Input data


| Data              | Original source                                                                                   |
| ------------------|------------------------------------------------------------------------------------------------- |
| LiP-MS data       | [Molecular Cell dataset](https://linkinghub.elsevier.com/retrieve/pii/S1097276523006512)          |
| Entanglement data |  [JMB dataset](https://www.sciencedirect.com/science/article/abs/pii/S0022283624000251?via%3Dihub) |


### Processed data (used in notebooks)

The above inputs are integrated into a single processed dataset:
`statistical_association/data/SC_Ent.pkl`.

This merged file combines:

- **LiP-MS data**: quantified proteins from the LiP-MS experiment, including whether each protein shows age-related structural changes and the positions of significant proteolytic alterations.
- **Entanglement data**: NCLE status per protein, entangled-region annotations, and protein length.

Only proteins with average pLDDT >= 70 are included in the entanglement-based integration.

## Installation

### Prerequisites

- [Mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) (recommended; faster solver)
- [Conda/Miniconda](https://docs.conda.io/en/latest/miniconda.html) (fallback)

All required packages are listed in `bioenv.yml`.

### Setup

1. Clone this repository and enter the project directory.
2. Create and activate the environment with `mamba`:

```bash
mamba env create -f bioenv.yml
conda activate bioenv
```

If `mamba` is not available, use:

```bash
conda env create -f bioenv.yml
conda activate bioenv
```

## Reproducing results

### Statistical association

Notebook location: `statistical_association/notebook/`

Run the following notebooks:


| Notebook                                                   | Required input                                    |
| ---------------------------------------------------------- | ------------------------------------------------- |
| `1_0_SC_Ent_Protein_level.ipynb`                           | `statistical_association/data/SC_Ent.pkl`         |
| `1_1_SC_Ent_Residue_level.ipynb`                           | `statistical_association/data/SC_Ent.pkl`         |
| `2_Association_structural_change_abundance_increase.ipynb` | `statistical_association/data/protein_abundances` |


### CG simulations

Workflow location: `cg_sims/`

- Temperature quenching at 300 K: follow the workflow in `cg_sims/README.md`.

### Figures and tables

Main figures and Tables (results) are generated using following notebooks:

| Source                   | Notebook                                                                   | Output location                        |
| ------------------------ | -------------------------------------------------------------------------- | -------------------------------------- |
| Statistical association  | `1_0_SC_Ent_Protein_level.ipynb`, `1_1_SC_Ent_Residue_level.ipynb`, and `2_Association_structural_change_abundance_increase.ipynb` | `statistical_association/notebook/`    |
| CG misfolding propensity | `Plot_misfolding_propensity_Nature_style.ipynb`                            | `cg_sims/plot_misfolding_probability/` |


## Computational requirements


| Component                                   | Storage                     | CPUs                                        | RAM   | GPUs     | Runtime                                                                                         |
| ------------------------------------------- | --------------------------- | ------------------------------------------- | ----- | -------- | ----------------------------------------------------------------------------------------------- |
| Statistical association (Jupyter notebooks) | Minimal                     | 1 core                                      | 8 GB  | None     | Negligible                                                                                      |
| CG simulations                              | Depends on trajectory count | 1 core (CPU-only) or 1 CPU + 1 GPU (faster) | 8 GB+ | Optional | ~3 h for short proteins (~100 residues, 1.5 us) to ~1 day for long proteins (~800 residues) |


Statistical association analyses run on modest hardware (for example, a laptop with 8 GB RAM and 1 CPU core). CG simulations can run on CPU only and benefit from optional GPU acceleration.

## Authors

Quyen V. Vu<sup>1</sup>, Ian Sitarik<sup>2,3</sup>, Daniel A. Nissley<sup>2,3</sup>, and Edward P. O'Brien<sup>1,2,3,4</sup>*

1. Department of Chemistry, Pennsylvania State University, University Park, PA, USA
2. National Science Foundation - National Synthesis Center for the Emergence in the Molecular and Cellular Sciences, Pennsylvania State University, University Park, PA, USA
3. Institute for Computational and Data Sciences, Pennsylvania State University, University Park, PA, USA
4. Bioinformatics and Genomics Graduate Program, The Huck Institutes of the Life Sciences, Pennsylvania State University, University Park, PA, USA

*Scientific correspondence: [epo2@psu.edu](mailto:epo2@psu.edu)*

*Maintainer (code/data): [qzv5006@psu.edu](mailto:qzv5006@psu.edu) or [vuqv.phys@gmail.com*](mailto:vuqv.phys@gmail.com)

## How to cite

If you use these datasets in your work, please cite:

> [Citation placeholder - add full bibliographic reference when published (journal, volume, pages, year, DOI).]

This work was supported by the National Science Foundation National Synthesis Center for the Emergence of Molecular and Cellular Sciences (NCEMS, DBI-2335029).