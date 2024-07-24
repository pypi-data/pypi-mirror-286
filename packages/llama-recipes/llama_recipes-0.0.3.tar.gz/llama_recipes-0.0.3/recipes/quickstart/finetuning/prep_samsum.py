from llama_recipes.datasets import get_samsum_dataset
from llama_recipes.configs.datasets import samsum_dataset
from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("/data/home/mreso/.cache/huggingface/hub/models--llhf--Meta-Llama-3.1-70B/snapshots/f7d3cc45ed4ff669a354baf2e0f05e65799a0bee")
tokenizer = AutoTokenizer.from_pretrained("/fsx-project/shared/mreso/.cache/huggingface/hub/models--llhf--3.1_Jul10-8B/snapshots/63565f4742196ac840b9ff168f57cae073b2646b/")
ds = get_samsum_dataset(samsum_dataset(), tokenizer, "train")
ds_val = get_samsum_dataset(samsum_dataset(), tokenizer, "validation")

print(ds._fingerprint)
print(ds_val._fingerprint)

# ds.save_to_disk("/fsx-project/shared/mreso/preproc_datasets/samsum_train")
# ds_val.save_to_disk("/fsx-project/shared/mreso/preproc_datasets/samsum_val")