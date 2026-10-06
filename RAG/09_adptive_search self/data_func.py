import os
from pathlib import Path
from typing import List

import chromadb
import tiktoken
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest"
)

client = chromadb.PersistentClient(path="./store")
coll_data = client.get_or_create_collection(
    name="data",
    embedding_function=ollama_ef
)
coll_preview = client.get_or_create_collection(
    name="preview",
    embedding_function=ollama_ef
)

tokenizer = tiktoken.get_encoding("cl100k_base")


def my_tokenizer(text: str) -> int:
    text = text.strip()
    if len(text) < 2:
        return 0
    token_len = len(tokenizer.encode(text))
    return token_len

def insert_data(path_str: str) -> None:
    path = Path(path_str)
    file_list = [x.name for x in path.iterdir() if x.is_file()]
    for file in file_list:
        filename, ext = os.path.splitext(file)
        if ext.lower() != ".pdf":
            print(f"pdf 파일이 아님 : {file}")
            continue
        if len(coll_data.get(where={"file": {"$eq": file}}, limit=1, include=[])['ids']) != 0:
            print(f"이미 존재함 : {file}")
            add_data_preview(file)
            continue
        reader = PdfReader(path / file)
        text = ""
        i = 0
        print(f"새로운 pdf 등록 : {file}, page : {len(reader.pages)}")
        print(f"진행중... (0/{len(reader.pages)})", end="")
        for i, page in enumerate(reader.pages):  # PDF 페이지들을 한장씩 꺼내기
            text = page.extract_text()  # 텍스트를 추출 후 text 변수에 누적
            id = f"{filename} page{i + 1}"
            metadata = {"file": file, "page": i + 1}
            coll_data.upsert(
                documents=[text],
                metadatas=[metadata],
                ids=[id])
            print(f"\r진행중... ({i+1}/{len(reader.pages)})", end="")
        print(f"\r등록 완료")
        print("=" * 40)
        add_data_preview(file)


def add_data_preview(file: str) -> bool | None:
    print(f"=== {file} preview 입력 시작 ===")
    if len(coll_preview.get(where={"file": {"$eq": file}}, limit=1, include=[])["ids"]) != 0:
        print(f"{file} preview 이미 존재함")
        return False
    pre_sort_datas = coll_data.get(where={"file": {"$eq": file}})
    fetched_data = list(zip(
        pre_sort_datas["ids"],
        pre_sort_datas["documents"],
        pre_sort_datas["metadatas"]
    ))
    if len(pre_sort_datas["ids"]) == 0:
        print(f"{file} pdf 파일의 내용이 data에 없음")
        return None

    datas = sorted(fetched_data, key=lambda x: x[2].get("page", ""))
    llm = ChatOllama(model="gemma4:e4b", model_kwargs={ "num_predict": 512 })
    sys_prompt = """
    당신은 PDF 파일에서 추출된 내용을 통해 현재의 페이지를 요약하는 전문가 입니다.
    파일명과 이전 분석기록과 입력받은 현재 페이지의 내용을 분석하여 현재 페이지의 내용을 요약하세요.
    내용이 너무 짧으면 내용 도입부의 제목일 수 있는 가능성을 고려하세요.
    파일명과 페이지, 추출된 텍스트가 입력되며 이전 분석기록은 대화내역에서 확인합니다.
    이전 분석기록에서의 페이지 입력값은 분석 성능을 위해 제공되지 않습니다.

    [입력형식]
    file : 파일명
    page : 페이지 번호
    content : 추출된 페이지 내용
    
    [입력예시]
    file : python 에서 PDF 다루기.pdf
    page : 3
    content : 파이썬에서 PDF 파일을 읽으려면...
    
    [출력규칙]
    현재 페이지에서 얻을 수 있는 정보만을 짧게 요약합니다.
    검색을 수행하기 위한 용도이므로 설명같은 방식이 아닌 매우 간결하게만 출력합니다.
    
    [출력예시]
    PDF 파일을 읽고 처리
    """
    context : List[BaseMessage] = [SystemMessage(content=sys_prompt)]
    pages = len(datas)
    print(f"새로운 pdf preview 등록 : {file}, page : {pages}")
    i = 0
    for ids, document, metadata in datas:
        i += 1
        # print("document : ", document)
        # print("metadata : ", metadata)
        query = f"""
        file : {metadata["file"]}
        page : {metadata["page"]}
        content : {document}
        """
        if len(context) > 11:
            context_run = [context[0]]
            context_run.extend(context[-10:])
        else:
            context_run = context
        context_run.append(HumanMessage(content=query))
        prompt = ChatPromptTemplate.from_messages(context_run)
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({})
        context.append(HumanMessage(content=f"{i} page 내용"))
    ()   context.append(AIMessage(content=result))
        id = f"{file} - {metadata["page"]}"
        coll_preview.upsert(
                documents=[result],
                metadatas=[metadata],
                ids=[id])
        print(f"완료 ({i}/{pages}), documents : {result}")
    print(f"표지 진행")
    sys_prompt_front = """
    당신은 PDF 파일에서 추출된 내용을 통해 전체 내용을 요약하는 전문가 입니다.
    파일명과 이전 분석기록의 내용을 바탕으로 이 PDF 파일에서 얻을 수 있는 정보를 확인할 수 있는 요약을 작성하고 목차를 작성하세요.
    이전 분석기록에서의 페이지 입력값은 분석 성능을 위해 제공되지 않습니다.
    
    파일명만 입력되며 이전 분석의 기록(대화내역)을 참고해야 합니다..
    [입력형식]
    file : 파일명

    [입력예시]
    file : python 에서 PDF 다루기.pdf

    [출력규칙]
    모든 내용을 종합하여 이 파일에서 얻을 수 있는 정보의 요약과 이전 분석기록을 바탕으로 페이지와 내용이 들어간 목차를 만듭니다.

    [출력예시]
    python 으로 PDF 파일을 다루는 방법입니다.
    
    p.1 : 제목
    p.2 : python 과 PDF 파일에 대한 설명
    p.3~5 : python 에서 PDF 파일을 읽고 출력하는 방법
    P.6~8 : python 에서 생성한 데이터를 PDF 로 저장하는 방법
    """
    context.append(SystemMessage(content=sys_prompt_front))
    query = f"""
    file : {file}
    """
    context.append(HumanMessage(content=query))
    prompt = ChatPromptTemplate.from_messages(context)
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({})
    context.append(AIMessage(content=result))
    id = f"{file} - 0"
    metadata = {'page': 0, 'file': file}
    coll_preview.upsert(
            documents=[result],
            metadatas=[metadata],
            ids=[id])
    print(f"완료 (표지)\n{result}")
    print(f"=== 등록 완료 ===")
    print("=" * 40)
    return True

insert_data("./data")