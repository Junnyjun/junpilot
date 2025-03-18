from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("./model/tuned", trust_remote_code=True)
model = AutoModel.from_pretrained("./model/tuned", trust_remote_code=True)

prompt = "인공지능의 발전 방향은"
inputs = tokenizer.encode(prompt, return_tensors="pt")

outputs = model.generate(
    inputs=inputs,
    max_length=100,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

print("생성된 문장:", tokenizer.decode(outputs[0], skip_special_tokens=True))
