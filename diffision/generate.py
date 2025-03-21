from transformers import AutoModelForCausalLM, AutoTokenizer

# 로컬에 저장된 fine-tuned 모델 불러오기 (trust_remote_code 옵션 제거)
tokenizer = AutoTokenizer.from_pretrained("./model/tuned")
model = AutoModelForCausalLM.from_pretrained("./model/tuned")

prompt = "엠제이의 키는 몇일까?"
inputs = tokenizer.encode(prompt, return_tensors="pt")

outputs = model.generate(
    inputs,
    max_length=500,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

print("생성된 문장:", tokenizer.decode(outputs[0], skip_special_tokens=True))
