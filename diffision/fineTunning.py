from datasets import load_from_disk
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, Trainer, TrainingArguments

# 모델과 토크나이저 로드 (여기서는 KoGPT2‑base‑v2 사용)
model_name = "skt/kogpt2-base-v2"
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 패딩 토큰이 없다면 직접 추가
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})

# 이전 단계에서 토큰화된 데이터셋 로드
dataset = load_from_disk("./model/result")

# TrainingArguments 설정 (필요에 따라 조정)
training_args = TrainingArguments(
    output_dir="./model/result",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=10,
)

# Trainer 객체 정의 (모델, 학습 인자, 데이터셋 지정)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"]
)

# 모델 추가 학습 시작
trainer.train()

# 학습이 완료되면 모델과 토크나이저 저장
model.save_pretrained("./model/tuned")
tokenizer.save_pretrained("./model/tuned")
