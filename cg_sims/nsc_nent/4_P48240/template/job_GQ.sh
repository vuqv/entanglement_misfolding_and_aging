#!/bin/bash

#SBATCH -J 4_P48240_SETINDEX

#SBATCH --partition=standard
#SBATCH --account=epo2_cr_default
## SBATCH --gres=gpu:1

#SBATCH -o output_GQ.out
#SBATCH -e error_GQ.err
#SBATCH -N 1
#SBATCH -n 4

#SBATCH --mem=24G
#SBATCH -t 48:00:00


## YOUR MAIN COMMANDS HERE

cd $SLURM_SUBMIT_DIR
echo `pwd`

GQ.py -op GQ/ -on SETINDEX -psf setup/P48240_clean_ca.psf -cor setup/P48240_clean_ca.cor -dcd SETINDEX_prod.dcd -sec setup/secondary_struc_defs.txt --aa setup/P48240_clean.pdb -t 4