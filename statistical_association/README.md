# statistical_association

Statistical association workflows for testing the relationship between native non-covalent lasso entanglements (NCLEs) and age-associated structural changes in the yeast proteome.

## Primary entry points

Main notebooks are located in `analysis/`.

| Notebook | Required input | Aim |
| --- | --- | --- |
| `1_0_SC_Ent_Protein_level.ipynb` | `statistical_association/data/SC_Ent.pkl` | Test the association between age-associated structural-change proteins and the presence of NCLEs. |
| `1_1_SC_Ent_Residue_level.ipynb` | `statistical_association/data/SC_Ent.pkl` | Test the association between age-associated structural-change residues and entangled regions (within entangled proteins). |
| `2_Association_structural_change_abundance_increase.ipynb` | `statistical_association/data/protein_abundances` | Test the association between age-related structural change and abundance increase with age. |

## Data folder

Primary datasets and preprocessing resources are in `data/`.

| Path | Description |
| --- | --- |
| `data/SC_Ent.pkl` | Integrated dataset used by protein-level and residue-level NCLE association notebooks. |
| `data/protein_abundances/` | Protein abundance data and preprocessing files used for abundance-vs-structural-change association analysis. |
