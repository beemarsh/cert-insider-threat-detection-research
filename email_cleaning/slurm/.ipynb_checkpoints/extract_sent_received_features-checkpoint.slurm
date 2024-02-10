#!/bin/bash

#SBATCH --job-name=EXTRACTFEATURES

##SBATCH --partition=himem
#SBATCH --nodes=1  # Number of nodes
#SBATCH --cpus-per-task=20  # Number of CPU cores
#SBATCH --output=logs_email_counts_extract.log
#SBATCH --error=errlogs_email_counts_extract.log

NOTEBOOK_FILE="extract_sent_recieved_email_counts.ipynb"

cd ..

# Convert the specific .ipynb file to a .py file
jupyter nbconvert --to script "$NOTEBOOK_FILE"

SCRIPT_FILE="${NOTEBOOK_FILE%.ipynb}.py"

# Run the generated Python script
python3 "$SCRIPT_FILE"

rm "$SCRIPT_FILE"