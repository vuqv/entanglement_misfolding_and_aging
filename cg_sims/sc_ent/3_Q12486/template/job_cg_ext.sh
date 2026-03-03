#!/bin/bash

#SBATCH -J 3_Q12486_SETINDEX

#SBATCH --partition=standard
#SBATCH --account=epo2_cr_default
#SBATCH --gres=gpu:1

#SBATCH -o output_ext.out
#SBATCH -e error_ext.err
#SBATCH -N 1
#SBATCH -n 1

#SBATCH --mem=4G
#SBATCH -t 72:00:00


## YOUR MAIN COMMANDS HERE

conda init bash
source /storage/home/qzv5006/work/anaconda3/etc/profile.d/conda.sh
conda activate cg_toolkit
cd $SLURM_SUBMIT_DIR
echo `pwd`
#
python single_run.py -f control_ext.cntrl
