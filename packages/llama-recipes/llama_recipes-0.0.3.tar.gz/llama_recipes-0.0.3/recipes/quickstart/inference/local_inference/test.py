import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig

model_name = "llhf/Meta-Llama-3.1-8B-Instruct"
max_padding_length=None
temperature=1.0
top_p=1.0
top_k=50
max_new_tokens=100

kwargs = {'quantization_config': BitsAndBytesConfig(load_in_4bit=True), 'device_map': 'auto', 'low_cpu_mem_usage': True, 'attn_implementation': None}
print(f"{kwargs=}")
model = AutoModelForCausalLM.from_pretrained(
    model_name, return_dict=True, **kwargs
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def inference(
        user_prompt,
        temperature,
        top_p,
        top_k,
        max_new_tokens,
        **kwargs,
    ):
        batch = tokenizer(
            user_prompt,
            padding="max_length",
            truncation=True,
            max_length=max_padding_length,
            return_tensors="pt",
        )
        batch = {k: v.to("cuda") for k, v in batch.items()}

        with torch.no_grad():
            outputs = model.generate(
                **batch,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_p=top_p,
                temperature=temperature,
                min_length=None,
                use_cache=True,
                top_k=top_k,
                repetition_penalty=1.0,
                length_penalty=1,
                **kwargs,
            )
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"{output_text=}")

inference("Hello", temperature, top_p, top_k, max_new_tokens)

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# input_text = "What are we having for dinner?"
# input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

# a={'max_new_tokens': 100, 'do_sample': True, 'top_p': 1.0, 'temperature': 1.0, 'min_length': None, 'use_cache': True, 'top_k': 50, 'repetition_penalty': 1.0, 'length_penalty': 1}
# quantized_model.eval()
# with torch.no_grad():
#     output = quantized_model.generate(**input_ids, **a)

# print(tokenizer.decode(output[0], skip_special_tokens=True))