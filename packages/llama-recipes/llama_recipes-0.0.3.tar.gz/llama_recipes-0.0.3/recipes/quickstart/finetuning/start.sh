#!/bin/bash

# Enable for A100
export FI_PROVIDER="efa"

echo Node IP: $head_node_ip
export LOGLEVEL=INFO
# debugging flags (optional)
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=WARN
export PYTHONFAULTHANDLER=1
export LD_LIBRARY_PATH=/opt/amazon/efa/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
export CUDA_LAUNCH_BLOCKING=0
export NCCL_IB_DISABLE=1
export PYTHONFAULTHANDLER=1

# on your cluster you might need these:
# set the network interface
export NCCL_SOCKET_IFNAME="enp"
export FI_EFA_USE_DEVICE_RDMA=1
export FI_EFA_SET_CUDA_SYNC_MEMOPS=0
export NCCL_BUFFSIZE=2097152

export HF_HOME=/fsx-project/shared/mreso/.cache/huggingface/
# export MODEL_NAME="/fsx-project/shared/mreso/.cache/huggingface/hub/models--llhf--3.1_Jul10-8B/snapshots/63565f4742196ac840b9ff168f57cae073b2646b/"
export MODEL_NAME="/fsx-project/shared/mreso/.cache/huggingface/hub/models--sllhf--Meta-Llama-3.1-405B/snapshots/ce0673fe3ba1391d759ee7d6d82943261f0c551e"
# export MODEL_NAME="/fsx-project/shared/mreso/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3-70B-Instruct/snapshots/7129260dd854a80eb10ace5f61c20324b472b31c/"
# export MODEL_NAME="/fsx-project/shared/mreso/.cache/huggingface/hub/models--llhf--Meta-Llama-3.1-70B/snapshots/f7d3cc45ed4ff669a354baf2e0f05e65799a0bee"

export OUTPUT_DIR="/fsx-project/shared/mreso/output_dir_405B_base"


# export MASTER_PORT=$(expr 10000 + $(echo -n $SLURM_JOBID | tail -c 4))
# export MASTER_ADDR=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
# echo "MASTER_ADDR:MASTER_PORT="${MASTER_ADDR}:${MASTER_PORT}
export MASTER_PORT=14305
export MASTER_ADDR=cr1-p548xlarge-5

export FSDP_CPU_RAM_EFFICIENT_LOADING=1 
export ACCELERATE_USE_FSDP=1 
export TOKENIZERS_PARALLELISM=false

export TORCH_CPP_LOG_LEVEL=INFO 
export TORCH_DISTRIBUTED_DEBUG=INFO 
export TORCH_SHOW_CPP_STACKTRACES=1
export TORCH_NCCL_ENABLE_MONITORING=1

export TORCH_NCCL_DUMP_ON_TIMEOUT=1
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export TORCH_NCCL_TRACE_BUFFER_SIZE=20000
export TORCH_NCCL_DEBUG_INFO_TEMP_FILE=/fsx-project/shared/mreso/405_debugging/rank_

# srun -l hostname -s
# srun -l nvidia-smi
# srun -l env

torchrun --nnodes 4 --nproc_per_node 8 --rdzv_id 54321 --rdzv_backend c10d --rdzv_endpoint ${MASTER_ADDR}:${MASTER_PORT} ./finetuning.py  --model_name $MODEL_NAME --enable_fsdp  --mixed_precision False --low_cpu_fsdp  --use_peft --peft_method lora --quantization 4bit  --quantization_config.quant_type nf4 --output_dir $OUTPUT_DIR