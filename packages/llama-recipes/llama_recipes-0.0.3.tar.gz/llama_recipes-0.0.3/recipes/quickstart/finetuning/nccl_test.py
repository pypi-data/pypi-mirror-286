import os
import torch.distributed as dist
import torch

os.environ["MASTER_ADDR"] = "127.0.0.1"
os.environ["MASTER_PORT"] = "25679"

dist.init_process_group(backend="nccl", world_size=1, rank=0)

# Assuming the process group has been initialized
tensor = torch.randn(10).cuda()
# Reduce operation across all GPUs
dist.reduce(tensor, dst=0, op=dist.ReduceOp.SUM)