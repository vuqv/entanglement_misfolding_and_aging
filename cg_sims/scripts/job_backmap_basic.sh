#!/bin/bash

#SBATCH -J PROTEININDEX_PROTEINNAME_SETINDEX

#SBATCH --partition=basic
#SBATCH --account=epo2_cr_default
## SBATCH --gres=gpu:1

#SBATCH -o output_BM.out
#SBATCH -e error_BM.err
#SBATCH -N 1
#SBATCH -n 4

#SBATCH --mem=24G
#SBATCH -t 48:00:00


## YOUR MAIN COMMANDS HERE

conda init bash
source /storage/home/qzv5006/work/anaconda3/etc/profile.d/conda.sh
conda activate bioenv
cd $SLURM_SUBMIT_DIR
echo `pwd`


backmap_traj.py -f SETINDEX_prod.dcd -p ../template/setup/top.psf -o aa_SETINDEX
