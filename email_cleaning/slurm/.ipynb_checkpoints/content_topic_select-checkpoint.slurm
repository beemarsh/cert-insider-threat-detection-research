#!/bin/bash

#SBATCH --job-name=SELECTTOPIC

#SBATCH --partition=gpu
#SBATCH --nodes=1  # Number of nodes
#SBATCH --gres=gpu:1                    # Number of GPUs
#SBATCH --mem=100G                      # Total memory required

#SBATCH --output=logs_topic_select.log
#SBATCH --error=errlogs_topic_select.log

NOTEBOOK_FILE="content_topic_selection.ipynb"

cd ..

# Convert the specific .ipynb file to a .py file
jupyter nbconvert --to script "$NOTEBOOK_FILE"

SCRIPT_FILE="${NOTEBOOK_FILE%.ipynb}.py"

# Run the generated Python script
python3 "$SCRIPT_FILE"

rm "$SCRIPT_FILE"