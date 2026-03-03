# cg_sims

Coarse-grained (CG) simulation scripts, preparation notebooks, and analysis workflows for protein folding and entanglement.



## Primary entry points


| Workflow                                                                      | Location            | Contents                                                                  |
| ----------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| CG folding of age-associated structural-change and entangled proteins         | `sc_ent/`           | Setup for proteins in this category                                       |
| CG folding of non-age-associated structural-change and non-entangled proteins | `nsc_nent/`         | Setup for proteins in this category                                       |
| Template scripts                                                              | `scripts/`          | Reusable simulation and analysis job templates                            |
| Template analysis notebooks                                                   | `scripts/analysis/` | MSM analysis, free-energy plots, visualization, representative structures |


## Step-by-step: run CG simulations

### Step 1: `1_copy_sim_set.sh` (prepare trajectory folders)

Copies the `template` directory into 50 trajectory folders (`0` to `49`) and replaces `SETINDEX` in `job.sh`, `control.cntrl`, `job_cg_ext.sh`, and `control_ext.cntrl`.

```bash
./1_copy_sim_set.sh
```

### Step 2: `2_submit_set_of_jobs.sh` (submit MD production jobs)

Submits initial CG MD production jobs (`job.sh`) for all 50 trajectories. Each job runs `single_run.py` with `control.cntrl`.

```bash
./2_submit_set_of_jobs.sh
```

### Step 3: `3_copy_GQ.sh` (prepare GQ entanglement scripts)

Copies GQ job scripts (`job_GQ.sh`, `job_GQ_mgc.sh`, `job_GQ_open.sh`) from `template` into each trajectory folder and replaces `SETINDEX`.

```bash
./3_copy_GQ.sh
```

### Step 4: `4_submit_GQ.sh` (submit entanglement analysis)

Submits GQ analysis jobs to compute entanglement metrics (G, Q) from production trajectories.

Available submission scripts:

- `4_submit_GQ.sh`: standard GQ (`job_GQ.sh`)
- `4_b_submit_GQ_mgc.sh`: MGC variant (`job_GQ_mgc.sh`)
- `4_c_submit_GQ_open.sh`: open variant (`job_GQ_open.sh`)

```bash
./4_submit_GQ.sh
```

### Step 5: `5_check_md_finish.sh` (check MD completion)

Verifies that production trajectories finished correctly by checking for `{i}_prod.dcd` and `fQ.dat`, and by confirming the last value in `fQ.dat` is `100000000`.

```bash
./5_check_md_finish.sh
```

### Step 6: `6_check_GQ.sh` (check GQ output)

Checks that G and Q files exist (`{i}/GQ/G/{i}.G`, `{i}/GQ/Q/{i}.Q`) and have the expected number of lines (default: `20000`).

```bash
./6_check_GQ.sh
```

### Step 7: `7_check_fQ.sh` (inspect `fQ.dat`)

Prints the first two lines and last line of `fQ.dat` for each trajectory for quick inspection of native-contact fraction time series.

```bash
./7_check_fQ.sh
```

### Optional step 8: `8_copy_sim_set_ext.sh` (prepare extended simulation scripts)

Copies extended-simulation files (`job_cg_ext.sh`, `control_ext.cntrl`) into each trajectory folder and replaces `SETINDEX`.

Use this step only if simulations need to run longer than 1.5 microseconds (as defined in `control.cntrl`).

```bash
./8_copy_sim_set_ext.sh
```

### Optional step 9: `9_submit_set_of_jobs_ext.sh` (submit extended MD jobs)

Run this step only if Step 8 is required.

Submits extended CG MD jobs (`job_cg_ext.sh`), where each job runs `single_run.py` with `control_ext.cntrl`.

```bash
./9_submit_set_of_jobs_ext.sh
```

## Summary workflow


| Step         | Script                        | Purpose                                 |
| ------------ | ----------------------------- | --------------------------------------- |
| 1            | `1_copy_sim_set.sh`           | Create trajectory folders from template |
| 2            | `2_submit_set_of_jobs.sh`     | Submit CG MD production jobs            |
| 3            | `3_copy_GQ.sh`                | Copy GQ scripts                         |
| 4            | `4_submit_GQ.sh`              | Submit entanglement (GQ) analysis       |
| 5            | `5_check_md_finish.sh`        | Verify MD completion                    |
| 6            | `6_check_GQ.sh`               | Verify GQ output                        |
| 7            | `7_check_fQ.sh`               | Inspect `fQ.dat`                        |
| 8 (optional) | `8_copy_sim_set_ext.sh`       | Copy extended-simulation scripts        |
| 9 (optional) | `9_submit_set_of_jobs_ext.sh` | Submit extended MD jobs                 |


