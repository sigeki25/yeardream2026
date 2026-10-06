"""
LLM 활용하는 정보
1. 자체 모델 - 모델이 학습한 내용들(ollama)
2. RAG - 저장소에서 담고있는 고유의 지식(chromadb)
3. 인터넷 검색 - 최신정보, 실시간 정보(tavily
tavily search API - AI 에이전트 및 LLM 을 위해 최적화된 AI 전용 검색엔진 서비스 API
"""
import os

from dotenv import load_dotenv
from langchain_tavily import TavilySearch, TavilyExtract

load_dotenv()  # .env 불러오기

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


def basic_search(query: str):
    ### search_depth
    # basic   : 빠르고 저렴한 검색(1~2 credit), 결과마다 간단한 content 제공
    # advance : basic * 2 배 검색, 문맥적 의미까지 분석해 깊게 탐색(예: 광고 문구 제거)
    ### topic
    # general : 기본값, 일반 웹 검색, 뉴스, 일반지식, 블로그, 위키디피아 등 웹 전반의 통합 검색
    # news    : 최신 뉴스/기사 전용 검색
    # finance : 금융/경제/주식 전용 검색
    search = TavilySearch(max_results=3, search_depth="basic", topic="general")
    result = search.invoke({"query": query})
    # print(result)
    for r in result["results"]:
        print(f"  title : {r["title"]}")
        print(f"    url : {r["url"]}")
        print(f"summary : {str(r["content"][:150]).replace("\n", "\n" + " " * 8 + "| ")}...\n")


# basic_search("2026년 langchain 최신버전 주요 변경사항")

def detail_content(query: str):
    search = TavilySearch(max_results=1, search_depth="basic", topic="general")
    result = search.invoke({"query": query})
    ### search_depth
    # basic   : 표준적인 본문 텍스트 추출
    # advance : 표, 구조, 동적요소 등을 정밀한 추출
    extract = TavilyExtract(extract_depth="basic")

    for r in result["results"]:
        print(f"  title : {r["title"]}")
        url = r["url"]
        print(f"    url : {url}")
        content = extract.invoke({"urls": [url]})
        print(f"   keys : {r.keys()}")
        print(f"content : {str(r["raw_content"]).replace("\n", "\n" + " " * 8 + "| ")}...\n")

# detail_content("tavily 활용법")

def advanced_search(query: str):
    # include_answer = "advanced"
    # include_raw_content = "markdown"
    # title_range = "year"
    # exclude_domains = ["youtube.com"]
    search = TavilySearch(
        max_results=3,
        topic="general",
        include_depth="advanced",
        include_answer="advanced",
        include_raw_content = "markdown",
        title_range="year",
        exclude_domains=["youtube.com"]
    )
    result = search.invoke({"query": query})
    for r in result["results"]:
        print(f"       keys : {r.keys()}")
        print(f"      title : {r["title"]}")
        print(f"    content : {str(r["content"]).replace("\n", "\n" + " " * 12 + "| ")}...")
        print("             ==================================")
        print(f"raw_content : {str(r["raw_content"]).replace("\n", "\n" + " " * 12 + "| ")}...")
        print()
        break

advanced_search("RAG 시스템에서 검색 품질을 높이는 최신 기법")