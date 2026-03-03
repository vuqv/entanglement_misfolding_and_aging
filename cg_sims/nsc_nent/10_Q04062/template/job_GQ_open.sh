#!/bin/bash

#SBATCH -J 10_Q04062_SETINDEX

#SBATCH --partition=open

#SBATCH -o output_GQ.out
#SBATCH -e error_GQ.err
#SBATCH -N 1
#SBATCH -n 4

#SBATCH --mem=24G
#SBATCH -t 24:00:00


## YOUR MAIN COMMANDS HERE

conda init bash
source /storage/home/qzv5006/work/anaconda3/etc/profile.d/conda.sh
conda activate bioenv
cd $SLURM_SUBMIT_DIR
echo `pwd`

GQ.py -op GQ/ -on SETINDEX -psf setup/Q04062_clean_ca.psf -cor setup/Q04062_clean_ca.cor -dcd SETINDEX_prod.dcd -sec setup/secondary_struc_defs.txt --aa setup/Q04062_clean.pdb -t 4
