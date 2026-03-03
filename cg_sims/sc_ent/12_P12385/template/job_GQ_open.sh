#!/bin/bash

#SBATCH -J 12_P12385_SETINDEX

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

GQ.py -op GQ/ -on SETINDEX -psf setup/P12385_clean_ca.psf -cor setup/P12385_clean_ca.cor -dcd SETINDEX_prod.dcd -sec setup/secondary_struc_defs.txt --aa setup/P12385_clean.pdb -t 4
