# collection : lecture
# 과목 : FAST API, PANDAS, SCIKIT-LEARN 중 택일(모두 해도 상관 없음)
# 시험용 LLM 제작
import os
from pathlib import Path

import chromadb
import ollama
import tiktoken
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest"
)

client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name="lecture",
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
        if len(coll.get(where={"file": {"$eq": file}}, limit=1, include=[])['ids']) != 0:
            print(f"이미 존재함 : {file}")
            continue
        reader = PdfReader(path / file)
        text = ""
        i = 0
        print(f"새로운 pdf 등록 : {file}, page : {len(reader.pages)}")
        print(f"진행중... (0/{len(reader.pages)})", end="")
        for i, page in enumerate(reader.pages):  # PDF 페이지들을 한장씩 꺼내기
            text = page.extract_text()  # 텍스트를 추출 후 text 변수에 누적
            text_spliter = RecursiveCharacterTextSplitter(
                chunk_size=800,  # 쵀대 청크 크기
                chunk_overlap=50,  # 청크간 전후 문맥 파악을 위해 겹쳐지는 수
                length_function=my_tokenizer,  # 토큰의 길이를 뭘로 정할지
            )
            chunks = text_spliter.split_text(text)
            ids = [f"{filename} page{i + 1}-{j}" for j in range(1, len(chunks) + 1)]
            metadatas = [{"file": file, "page": i + 1, "part": j + 1} for j in list(range(1, len(chunks) + 1))]
            coll.upsert(
                documents=chunks,
                metadatas=metadatas,
                ids=ids)
            print(f"\r진행중... ({i+1}/{len(reader.pages)})", end="")
        print(f"\r등록 완료")
        print("=" * 40)


insert_data("data/")


def search_data(query: str) -> None:
    print(f"질문내용 : {query}")
    results = coll.query(
        query_texts=[query],
        n_results=5,
    )
    print(results)
    # 가져온 리스트 안의 내용을 줄바꿈 두번으로 붙여서 사나의 텍스트로 변환
    context = "\n\n".join(f"{document}\nfile : {metadata.get("file")}, page : {metadata.get("page")}, part : {metadata.get("part")}" for document, metadata in zip(results["documents"][0], results["metadatas"][0]))

    print(context)

    # llm 에 전달할 프롬프트 작성
    prompt = f"""
    당신은 PDF 검색 전문가 입니다. 제공된 [PDF 내용]를 바탕으로 사용자의 [질문]에 답하세요.
    PDF 내용에 근거하여 상세하게 설명해 주세요.

    [PDF 내용]
    {context}

    [질문]몌
    {query}
    """

    resp = ollama.generate(model="gemma4:e4b", prompt=prompt, stream=True)
    for chunk in resp:
        print(chunk["response"], end="", flush=True)


question = input("PDF에서 찾을 내용 입력\n")
# 이 소설의 주인공은?
# 이 소설의 줄거리를 요약
search_data(question)
