#!/bin/bash

#SBATCH --job-name=LDAMODELTRAIN

#SBATCH --partition=gpu
#SBATCH --nodes=1  # Number of nodes
#SBATCH --gres=gpu:1                    # Number of GPUs
#SBATCH --mem=120G                      # Total memory required

#SBATCH --output=logs_train_lda.log
#SBATCH --error=errlogs_train_lda.log

NOTEBOOK_FILE="content_LDA_model.ipynb"

cd ..

# Convert the specific .ipynb file to a .py file
jupyter nbconvert --to script "$NOTEBOOK_FILE"

SCRIPT_FILE="${NOTEBOOK_FILE%.ipynb}.py"

# Run the generated Python script
python3 "$SCRIPT_FILE"

rm "$SCRIPT_FILE"