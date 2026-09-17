import logging
from typing import Dict, Any

import langchain
from fastapi import APIRouter
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

from tools import plus, minus, multiply, divide

# 추론 과정을 확인하기 위한 로그 설정
logging.basicConfig(level=logging.INFO)
langchain.debug = True

# 모델 불러오기
model_id = "gemma4:e4b"
model = ChatOllama(model=model_id, temperature=0)

# 도구 등록
tools = [plus, minus, multiply, divide]

# 에이전트 생성
agent = create_agent(model=model, tools=tools)

# 프롬프트 제작
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 사칙연산 전문가 입니다. 값 a와 값 b, 연산자가 주어지면 연산 후 답을 반환하는 작업을 수행하세요."),
    ("user", "{message}")
])

# 파이프라인 조합
chain = prompt | agent

# 실행
# 3+3 은?
# a=5, b=10 일 경우 a+b를 계산해 줘
# msg = input("사칙 연산을 입력하세요.\n 예) 4+3\n")
#
# resp = chain.invoke({"message", msg})
#
# print("---AI 의 생각 과정 모니터링---")
# for i, message in enumerate(resp["messages"]):
#     print(f"[step{i:2d}]  {message}")
#
# print(resp["messages"][-1].content)

router = APIRouter(prefix="/calc", tags=["calc"])

@router.get("")
def get_calculate(val1:str, val2:str, oper:str):
    return calculate(val1, val2, oper)
    # return StreamingResponse(calculate(data["val1"], data["val2"], data["oper"]), media_type="text/plain")

def calculate(a:str | int | float, b:str | int | float, oper:str):
    msg = f"{a} {oper} {b} 을 계산해서 결과만 출력"
    resp = chain.invoke({"message", msg})
    return resp["messages"][-1].content