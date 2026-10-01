from typing import TypedDict, List, Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

from store_func import coll, load_excel_data
from utils import retrieve_to_text, python_code_parser, run_code


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
llm = ChatOllama(model="gemma4:e4b")


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

    ### state 에서 context 추출 후 처리 ###
    context = state.get("context", [])
    print(f"context : {context}")
    msg_list.extend(context)

    route_prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = route_prompt | route_llm | JsonOutputParser()
    result = chain.invoke({"question": question})
    print(f"route result : {result}")
    return {'question': question, 'generation': result['route'], "context": context}


def router(state: State):
    print("router() init_answer 내용을 통해 분기")
    # plain_answer, excel_data, vector_db
    print(state['generation'])
    return state['generation']


def plain_answer(state: State):
    print("plain_answer() 학습한 내용 안에서 답변")
    question = state['question']
    msg_list = []
    context = state.get("context", [])

    msg_list.extend(context)
    msg_list.append(HumanMessage(content=question))
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({})

    # print(answer)
    return {'question': question, 'generation': answer}


def excel_data(state: State):
    print("excel_data() excel 에서 데이터 참고 코드 생성")
    question = state['question']
    df = load_excel_data()
    sys_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
    주어진 DataFrame 으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame 이름은 excel_df 이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {df.columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
    """

    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(("human", "{question}"))
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt | llm | StrOutputParser() | python_code_parser
    code = chain.invoke({"question": question})
    data = run_code("excel_df", df, code)

    return {"question": question, "generation": data, "code": code, "data": data}

def excel_answer(state: State):
    print("excel_answer() excel_data 에서 데이터 참고 후 답변")
    question = state["question"]
    data = state["data"]

    sys_prompt = """
    당신은 데이터를 바탕으로 질문에 답하는 데이터 분석가 입니다.
    사용자가 입력한 질문을 제공된 데이터를 바탕으로 질문에 답하세요.
    """

    msg_list = []
    context = state.get("context", [])
    msg_list.extend(context)

    msg_list.append(("system", sys_prompt))
    msg_list.append(("human", f"질문 : {question}\n데이터 : {data}"))

    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({})
    state["generation"] = answer

    return state

def vector_db(state: State):
    print("RAG 에서 데이터 참고 후 답변")
    question = state['question']

    ret = coll.as_retriever(search_kwargs={"k": 5})
    ret_chain = ret | retrieve_to_text
    data = ret_chain.invoke(question)

    print(f"참고자료 : {data}")
    msg_list = []
    context = state.get("context", [])
    msg_list.extend(context)
    msg_list.append(("system", "사용자의 질문을 제공하는 정보를 바탕으로 대답하세요."))
    msg_list.append(("human", f"질문 : {question}\n정보 : {context}"))


    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({})

    return {'question': question, 'generation': answer}


# 최종적으로 답변을 전달하고 context 에 대화내용을 저장하는 노드
def end_point_answer(state: State):
    context = state.get("context", [])
    context.append(HumanMessage(content=state["question"]))
    context.append(AIMessage(content=state["generation"]))
    state["context"] = context
    print(f"대화 히스토리 개수 : {len(state["context"])}")

    return state