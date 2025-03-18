import dataset
from datasets import load_dataset
from transformers import AutoTokenizer
from tokenizers import Tokenizer

model_name = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

datasets = load_dataset("model/dataset", data_files={
    "train": "*-train.txt",
    "validation": "*-validation.txt"
})

def tokenize_function(examples):
    tokenized = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    tokenized["labels"] = tokenized["input_ids"].copy()  # ← 이 부분 추가 필수!
    return tokenized

tokenized_datasets = datasets.map(tokenize_function, batched=True)
tokenized_datasets.save_to_disk("model/result")
