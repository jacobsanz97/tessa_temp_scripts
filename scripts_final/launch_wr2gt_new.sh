#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --account=def-jbpoline
#SBATCH --mem-per-cpu=32768M
module load apptainer/1.1
module load python
export APPTAINER_BIND="/lustre04/scratch/jacobsr"
python 07_WR2GT.py
