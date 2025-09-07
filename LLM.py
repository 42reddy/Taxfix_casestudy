from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer, pipeline
import torch

model = 'mistralai/Mistral-7B-Instruct-v0.1'

tokenizer = AutoTokenizer.from_pretrained(model)
quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",  # or "fp4"
        bnb_4bit_compute_dtype=torch.bfloat16, # or torch.float16
    )

model = AutoModelForCausalLM.from_pretrained(
        model,
        quantization_config=quant_config,
        device_map="cuda", # or specify your device
    )

mistral_pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
    temperature=0.9
)