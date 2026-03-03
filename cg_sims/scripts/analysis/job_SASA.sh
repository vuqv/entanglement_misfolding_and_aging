#!/bin/bash

#SBATCH -J 11_P36008

#SBATCH --partition=basic
#SBATCH --account=epo2_cr_default
## SBATCH --gres=gpu:1

#SBATCH -o output_SASA.out
#SBATCH -e error_SASA.err
#SBATCH -N 1
#SBATCH -n 1

#SBATCH --mem=24G
#SBATCH -t 48:00:00


## YOUR MAIN COMMANDS HERE

conda init bash
source /storage/home/qzv5006/work/anaconda3/etc/profile.d/conda.sh
conda activate bioenv
cd $SLURM_SUBMIT_DIR
echo `pwd`

python calculation_SASA.py
#backmap_traj.py -f 1_prod.dcd -p ../template/setup/top.psf -o aa_1
