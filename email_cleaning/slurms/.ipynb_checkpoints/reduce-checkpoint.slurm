#!/bin/bash

#SBATCH --job-name=REDUCEDATASET

##SBATCH --partition=himem
#SBATCH --nodes=1  # Number of nodes
#SBATCH --cpus-per-task=20  # Number of CPU cores
#SBATCH --output=logs_reduce.log
#SBATCH --error=errlogs_reduce.log

NOTEBOOK_FILE="../reduce_dataset.ipynb"

# Convert the specific .ipynb file to a .py file
jupyter nbconvert --to script "$NOTEBOOK_FILE"

SCRIPT_FILE="${NOTEBOOK_FILE%.ipynb}.py"

# Run the generated Python script
python3 "$SCRIPT_FILE"

rm "$SCRIPT_FILE"