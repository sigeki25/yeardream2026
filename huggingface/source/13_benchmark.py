from time import time

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

text = "SDPA 와 EAGER 중에 누가 더 빠른가? 확인해 봅시다." * 30
inputs = tokenizer(text, return_tensors="pt").to("cuda")
print(f"입력 토큰 수 : {inputs["input_ids"].shape[1]}")


def benchmark(attn_type, name):
    print(f"=== [{name}] 측정 시작 ===")
    # 모델 불러오기
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        dtype=torch.float16,
        low_cpu_mem_usage=True,  # cpu, memory 절약
        attn_implementation=attn_type,
        device_map="auto"  # cuda, mps(mac)
    )
    # 실행
    start_time = time()
    with torch.no_grad():
        model(inputs["input_ids"])
    # CPU 가 GPU 작업 종료까지 기다리도록 동기화 시켜 준다.
    torch.cuda.synchronize()
    end_time = time() - start_time
    print(f"=== [{name}] 이 걸린시간 : {end_time} ===")


# benchmark("sdpa", "Flash Attention 방식(SDPA)")
benchmark("eager", "Standard Attention 방식(EAGER)")
