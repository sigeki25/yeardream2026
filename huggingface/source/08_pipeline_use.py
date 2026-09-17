import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"

model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# uv pip install accelerate
pipe = pipeline(task="text-generation", model=model_id, device_map="auto")

q = input("아무거나 질문 하세요\n")
# 허깅페이스에서 파이프라인 API에 대해서 설명해줘

result = pipe(q, max_new_tokens=1024, do_sample=True, temperature=0.7, top_p=0.9)
print(result[0]["generated_text"])