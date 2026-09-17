import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

# 1. 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)
# 2. 모델 불러오기
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.float16,  # dtype=torch.bffloat16 <- 메모리 절약 및 안정성 확보(GPU 에서 지원되야 함)
    # attn_implementation="flash_attention_2", # "eager", "sdpa"
    device_map="auto"
)

prompt = input("Ai 에게 질문하고 싶은 내용은?\n")
print(prompt)
# 3. 토큰화
message = [
    {"role": "system", "content": "너는 IT 전문가야, IT 지식을 주로 다루고 있으며 알기 쉽게 예를 들어서 설명해 주는것을 잘해"},
    {"role": "user", "content": prompt}
]

chat = tokenizer.apply_chat_template(
    message,
    tokenize=False,
    add_genderation_prompt=True
)
print(chat)

inputs = tokenizer(chat, return_tensors="pt").to(model.device)

# 4. 모델 추론
print("생각 하는 중...")
# with torch.no_grad():
#     output = model.generate(
#         **inputs,
#         max_new_tokens=2048,
#         do_sample=True,
#         temperature=0.7,
#         eos_token_id=tokenizer.eos_token_id
#     )
#     print(tokenizer.decode(output[0]))

# 실시간 출력을 위해서는 Streamer 가 필요하다.
streamer = TextStreamer(tokenizer, skip_prompt=True)

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=2048,
        do_sample=True,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,
        streamer=streamer
    )
