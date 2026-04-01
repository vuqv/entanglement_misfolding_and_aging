#!/bin/bash

#SBATCH -J 25_P39106_SETINDEX

#SBATCH --partition=standard
#SBATCH --account=epo2_cr_default
#SBATCH --gres=gpu:1

#SBATCH -o output.out
#SBATCH -e error.err
#SBATCH -N 1
#SBATCH -n 1

#SBATCH --mem=4G
#SBATCH -t 72:00:00


## YOUR MAIN COMMANDS HERE

cd $SLURM_SUBMIT_DIR
echo `pwd`
#
python single_run.py -f control.cntrl
