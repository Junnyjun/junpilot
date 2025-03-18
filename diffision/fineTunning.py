from transformers import AutoModel, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_from_disk
from torch import torch
from accelerate import Accelerator

model_name = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)


# 데이터 로드 (아까 만든 데이터셋)
dataset = load_from_disk("./model/result")

# 훈련 인자 정의
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=10,
)

# 트레이너 객체 정의
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"]
)

# 추가 학습 시작
trainer.train()

# 모델 저장
model.save_pretrained("./model/tuned")
tokenizer.save_pretrained("./model/tuned")
