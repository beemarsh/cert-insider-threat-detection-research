#!/bin/bash

#SBATCH --job-name=Email_extract

#SBATCH --partition=himem             # Specify the partition For this we are using high memory node which has 512GB memory
#SBATCH --nodelist=himem004
#SBATCH --mem=500G
#SBATCH --cpus-per-task=20
#SBATCH --output=out.log
#SBATCH --error=err.log



python3 Email_Cleaning.py      #Be careful --> Convert the Jupyter Notebook into a python script and then run it here
#srun python3 Email\ Cleaning.py
