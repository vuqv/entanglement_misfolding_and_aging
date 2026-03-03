# cg_sims/scripts

This folder contains **template scripts** (common parts only) used for all proteins. Scripts are copied into each protein folder during preparation; protein-specific parts are substituted there.

## Contents

| Item | Description |
| --- | --- |
| **SLURM and workflow shell scripts** | Submission/helper scripts for simulation and analysis jobs. Includes step-by-step scripts `1_copy_sim_set.sh` to `9_submit_set_of_jobs_ext.sh` for preparing folders, submitting MD runs, submitting GQ jobs, and validating outputs. |
| **`single_run.py`** | Core engine for temperature-quenching CG simulations (reads control settings and runs production trajectories). |
| **`GQ.py`** | Computes G and Q entanglement-related parameters from generated trajectories. |
| **Other job/control templates** | Includes `job.sh`, `job_GQ.sh`, `job_GQ_mgc.sh`, `job_GQ_open.sh`, `job_cg_ext.sh`, `job_backmap_basic.sh`, `control.cntrl`, and `control_ext.cntrl`. |
| **analysis/** | Template notebooks for downstream analysis (MSM, free-energy plots, SASA, chirality, visualization). Copy and adapt for each protein. |


