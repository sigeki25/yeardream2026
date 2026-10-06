from typing import TypedDict, List, Any, Dict

import sys

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph


class State(TypedDict):
    question: str
    generation: str
    data: Dict[str, Any]
    context: List[BaseMessage]
    langgraph_history: List[str]


route_llm = ChatOllama(model="gemma4:e4b", format="json")
llm = ChatOllama(model="gemma4:e4b")


def get_state():
    return StateGraph(State)


def init_data(state: State) -> State:
    print("init_data()")
    state["question"] = state.get("question", "")
    state["generation"] = state.get("generation", "")
    state["data"] = state.get("data", {})
    state["context"] = state.get("context", [])
    state["langgraph_history"] = state.get("langgraph_history", [])
    return state


def init_answer(state: State) -> State:
    print("init_answer()")
    sys_prompt = """
    당신은 사용자의 질문을 통해 RAG, 웹 검색을 활용할지 결정하는 전문가 입니다. 아래 내용을 참고하여 선택하세요.
    "rag" : 현재 "data" 에서 답변이 가능하면 선택
    "web" : 웹 검색엔진에서 값 받아오기
    "plain" : 위 두 경우 어디에도 속하지 않을 경우 선택
    
    [출력규칙]
    주어진 질문에 맞춰 "rag", "web", "plain" 중 하나만 선택
    다른 텍스트나 설명은 생성하지 말것
    json 형태로 "route" 라는 키에 대한 답으로 작성
    예) {{"route": "plain"}}
    """
    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(("human", "{question}"))
    route_prompt = ChatPromptTemplate.from_messages({"question": state["question"]})
    chain = route_prompt | route_llm | JsonOutputParser()
    result = chain.invoke({"question": state["question"]})
    state["data"].update({"router": result})
    state["langgraph_history"].append(sys._getframe(0).f_code.co_name)
    return state


def router(state: State) -> str:
    print("router()")
    # plain_answer, excel_data, vector_db
    print(state['data'])
    return state['data']


def rag(state: State) -> State:
    pass


def plain(state: State) -> State:
    print("plain()")
    msg_list = state["context"]
    msg_list.append(("human", "{question}"))
    prompt = ChatPromptTemplate.from_messages({"question": state["question"]})
    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke({"question": state["question"]})
    state["generation"] = result
    state["langgraph_history"].append(sys._getframe(0).f_code.co_name)
    return state


def web(state: State) -> State:
    pass


def last_answer(state: State) -> State:
    print("last_answer()")
    context = state.get("context", [])
    context.append(HumanMessage(content=state["question"]))
    context.append(AIMessage(content=state["generation"]))
    state["context"] = context
    state["langgraph_history"].append(sys._getframe(0).f_code.co_name)
    return state
