#!/bin/bash

#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --gpus-per-task 8
#SBATCH --account genai_interns
#SBATCH --qos genai_interns

export HF_HOME=/fsx-project/shared/mreso/.cache/huggingface/

srun -l hostname -s
srun -l nvidia-smi
srun -l env