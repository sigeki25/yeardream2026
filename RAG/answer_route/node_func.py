from typing import TypedDict, List, Any

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph


# State 객체
class State(TypedDict):
    question: str  # 질문
    generation: str  # 질문에 의해 생성된 답
    data: str  # 참고한 데이터
    code: str  # 요청시 생성된 코드
    context: List[Any]  # 대화내용 저장


def get_state():
    return StateGraph(State)


# 최초 질문을 받아서 plain, excel, vector 중 하나를 받는다.
route_llm = ChatOllama(model="gemma4:e4b", format="json")


def init_answer(state: State):
    print(f"init_answer() 최초 질문 : {state["question"]}")
    question = state["question"]
    sys_prompt = """
    당신은 사용자의 질문을 통해 RAG, 엑셀데이터 중 어느것을 활용할지 결정하는 전문가 입니다. 아래 내용을 참고하여 선택하세요.
    "excel" : 인공지능 데이터와 관련일 경우 선택
    "vector" : 인공지능 산업 동향 관련일 경우 선택
    "plain" : 위 두 경우 어디에도 속하지 않을 경우 선택
    
    [출력규칙]
    주어진 질문에 맞춰 "excel", "vector", "plain" 중 하나만 선택
    다른 텍스트나 설명은 생성하지 말것
    json 형태로 "route" 라는 키에 대한 답으로 작성
    예) {{"route": "plain"}}
    """
    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(("human", "{question}"))
    route_prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = route_prompt | route_llm | JsonOutputParser()
    result = chain.invoke({"question": question})
    print(f"route result : {result}")
    return {"question": question, "generation": ""}


def router(state: State):
    print("router() init_answer 내용을 통해 분기")
    # plain_answer, excel_data, vector_db
    return "plain"


def plain_answer(state: State):
    print("plain_answer() 학습한 내용 안에서 답변")
    return {"question": "", "generation": ""}


def excel_data(state: State):
    print("excel_data() excel 에서 데이터 참고 후 답변")
    return {"question": "", "generation": ""}


def vector_db(state: State):
    print("RAG 에서 데이터 참고 후 답변")
    return {"question": "", "generation": ""}
