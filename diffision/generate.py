from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("./model/tuned")
model = GPT2LMHeadModel.from_pretrained("./model/tuned")

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
