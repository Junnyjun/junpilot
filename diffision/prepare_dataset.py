from datasets import load_dataset
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel

model_name = "skt/kogpt2-base-v2"
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 패딩 토큰이 없다면, 직접 추가합니다.
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})

datasets = load_dataset("text", data_files={
    "train": "model/dataset/*train*",
    # "validation": "model/dataset/*validation*"
})

def tokenize_function(examples):
    tokenized = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_datasets = datasets.map(tokenize_function, batched=True)
tokenized_datasets.save_to_disk("model/result")
