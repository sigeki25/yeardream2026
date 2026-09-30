import contextlib
import io

import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

### 1. 모델 설정 및 지정
llm = ChatOllama(model="gemma4:e4b")

### 2. 데이터 불러오기
data_path = "data/InkjetDB_preprocessing.csv"
df_inkjet = pd.read_csv(data_path, index_col=0)
columns = ", ".join(df_inkjet.columns)
# print(columns)

### 3. 데이터 분석 프롬프트 작성
system_prompt = f"""
당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
주어진 DataFrame 으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
DataFrame 이름은 df_inkjet 이며, 다음과 같은 컬럼들이 있습니다.
컬럼들 : {columns}
데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
"""
print(system_prompt)

### 4. 프롬프트 조립 후 실행
# 'human', 'user', 'ai', 'assistant', 'system'
msg_list = [
    ("system", system_prompt),
    ("human", "{question}")
]
prompt = ChatPromptTemplate.from_messages(msg_list)
code_gen_chain = {"question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
# result = code_gen_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어")
# print(result)

### 5. 대답에서 코드만 추출
def python_code_parser(text: str):
    # 대답중에서 ```python 으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```,code내용,```]
    code_list = text.replace("```python", "```").strip().split("```")

    # ``` 이 없어서 끊지 못한경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]
    return code_list[1]
# print("###"*30)
# print(python_code_parser((result)))

code_extract_chain = code_gen_chain | python_code_parser

def run_code(input_code: str):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(input_code, {"df_inkjet": df_inkjet})
    except Exception as e:
        print(f"Error : {e}", file=output)
    return output.getvalue()

code_exec_chain = code_extract_chain | run_code
print(code_exec_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어"))

