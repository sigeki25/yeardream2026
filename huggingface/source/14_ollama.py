# uv pip install ollama
# ollama run hf.co/Jackrong/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF
from ollama import chat

text = input("ollama 와 대화해 보세요\n")


def chat_generator(input):
    print(f"입력 내용 : {input}")
    print("생각중...")
    resp = chat(
        model="exaone3.5:2.4b",
        messages=[{"role": "user", "content": input}]
    )
    print(resp.message.content)

# chat_generator(text)

def chat_stream(input):
    print(f"입력 내용 : {input}")
    print("생각중...")
    resp = chat(
        model="hf.co/Jackrong/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF:latest",
        messages=[{"role": "user", "content": input}],
        stream=True
    )

    for chunk in resp:
        # end= 는 print문에 출력한 후 마지막에 출력하는 부분(기본은 다음줄로 넘김)
        # flush=True 는 Stream 에 남아있는 잔여 데이터를 모두 밖으로 내보낸다.
        print(chunk.message.content, end="", flush=True)

chat_stream(text)

# ollama rm hf.co/Jackrong/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF:latest