#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --account=def-jbpoline
#SBATCH --mem-per-cpu=32768M

module load python/3.10
source ENV_nib/bin/activate
python ./06_warprate.py
