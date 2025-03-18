import dataset
from datasets import load_dataset
from transformers import GPT2Tokenizer
from transformers import AutoTokenizer


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # ★필수★

datasets = load_dataset("model/dataset", data_files={
    "train": "*-train.txt",
    "validation": "*-validation.txt"
})

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = datasets.map(tokenize_function, batched=True)
tokenized_datasets.save_to_disk("model/result")
