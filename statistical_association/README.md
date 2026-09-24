# statistical_association

Statistical association workflows for testing the relationship between native non-covalent lasso entanglements (NCLEs), age-associated structural changes (ASC), and increases in protein abundance with age in the yeast proteome.

## Primary entry points

Main notebooks are located in `notebook/`.

| Notebook | Required input | Aim |
| --- | --- | --- |
| `1_0_SC_Ent_Protein_level.ipynb` | `data/SC_Ent_no_transmembrane_secretory.pkl` | Test the association between age-associated structural-change proteins and the presence of NCLEs (Fisher's exact test; logistic regression adjusted for protein length). |
| `1_1_SC_Ent_Residue_level.ipynb` | `data/SC_Ent_no_transmembrane_secretory.pkl` | Test the association between age-associated structural-change residues (cut sites) and entangled regions, within entangled proteins only (Fisher's exact test; logistic regression adjusted for protein length). |
| `2_NCLE_ASC_abundance_3_models.ipynb` | `data/SC_ENT_ABD.xlsx` | Three length-adjusted logistic regression models testing whether NCLEs and ASC are associated with increased abundance with age: (1) `Abd_up ~ entangled + length_z`, (2) `Abd_up ~ SC + length_z`, (3) `Abd_up ~ entangled + SC + length_z`. Produces the supplementary-table summary and prevalence of abundance increase by NCLE/ASC status. |

Shared plotting, logging, and model-summary helpers are in `notebook/utils.py`.

## Data folder

| Path | Proteins | Description |
| --- | --- | --- |
| `data/SC_Ent_no_transmembrane_secretory.pkl` | 1,887 | Integrated LiP-MS and entanglement dataset, excluding transmembrane and secretory proteins. Key columns: `SC`, `entangled`, `length_AF`, `Cutsite_residues`, `entangled_residues`, `clustered_entangled_residues`. |
| `data/SC_ENT_ABD.xlsx` | 1,776 | Per-protein table for the abundance models; a subset of the 1,887 proteins above (transmembrane and secretory proteins also excluded). Columns: `Accession`, `SGDID`, `Uniprot`, `length_AF`, `entangled`, `SC`, `length_z` (standardized length), `Abd_up` (1 = abundance increases with age). |

## Outputs

Figures from notebooks `1_0` and `1_1` are written to `notebook/figs/` (`Protein_Level_*` and `Residue_Level_*`) in PDF, PNG (300 dpi), and SVG formats. SVG text is kept as editable text (`svg.fonttype = "none"`), so the Arial font must be available when the files are opened. Notebook `2` prints its results and writes no files.
