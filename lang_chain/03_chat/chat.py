from typing import Dict

from fastapi import APIRouter
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/ask", tags=["ask"])

# 모델 호출
model = ChatOllama(model="exaone3.5:2.4b")

conversation_history = []  # 대화 저장 리스트

# 프롬프트 작성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 답변 전문 AI 모델 입니다. 주어진 질문에 대해서 핵심만 간단히 대답하세요."),
    MessagesPlaceholder(variable_name="history"),  # 대화 내용을 history 라는 이름으로 제공
    ("user", "{query}")
])


@router.post("/chat")
def chat_answer(info: Dict[str, str]):
    return StreamingResponse(chatting(info["q"]), media_type="text/plain")


def chatting(query:str):
    # 파이프라인 조립
    chain = prompt | model

    if query in ["/test"]:
        yield "aa\nbb  \ncc"
        return
    if query in ["/history"]:
        if len(conversation_history) == 0:
            yield "대화 내역이 없습니다."
            return
        yield "=== 대화 내용 ===\n\n"
        for history in conversation_history:
            if isinstance(history, HumanMessage):
                yield f"\[User\]: {history.content}\n\n"
            elif isinstance(history, AIMessage):
                yield f"\[ AI \] : {history.content}\n\n"
        return

    if query in ["/clear"]:
        conversation_history.clear()
        # print(f"\nhistory length : {len(conversation_history)}")
        yield "대화 내역을 초기화합니다."
        return

    answer = ""
    for chunk in chain.stream({"query": query, "history": conversation_history}):
        yield chunk.content
        print(chunk.content, end="", flush=True)
        answer += chunk.content
    conversation_history.append(HumanMessage(content=query))
    conversation_history.append(AIMessage(content=answer))
