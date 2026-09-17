import json
import os
from datetime import datetime
from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from transformers import pipeline

from setting import logger

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"

vision = pipeline(model="google/vit-base-patch16-224")
model = ChatOllama(model="exaone3.5:2.4b")
board_img_tag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "당신은 이미지의 분석 결과물을 받아서 태그를 반환해야 합니다. 입력은 일치율이 높은 순서의 배열로 각 배열의 내용은 label은 항목명, score는 일치율(0~1 사이의 값)으로 입력받으며, 결과값은 score>=0.2 의 label만 핵심적인 특징만 키워드로 가공하며, 출력 형식은 해시태그 형식으로 각 태그의 시작부분은 반드시 #가 들어가고 띄어쓰기는 _ (언더바)를 사용하며 각 태그의 간격은 한칸씩 띄어야 합니다. 되도록 한국어로만 출력하며 score는 절대 출력하지 않습니다. 예를들어 'Welsh corgi'(웰시코기)의 경우 '#개 #웰시코기' 같이 연관되는 특징을 모두 표기합니다."),
    ("user", "{query}")
])

board_summation_prompt = ChatPromptTemplate.from_messages([
    ("system", "게시물의 제목과 내용, 이미지의 해시태그를 참고하여 검색시스템에서 찾기 좋도록 내용의 주제와 글의 목적을 50자 이내로 핵심만 출력해야 합니다."),
    ("human", "제목 : {subject}\n"
              "내용 : {content}\n"
              "이미지 해시태그 : {ai_img_tag}")
])


async def board_tag(data: Dict[str, Any], collection):
    summation = ai_img_tag = None
    if data["file"] is not None:
        image_vision = vision(data["file"])
        print("image_vision : ", image_vision)
        chain = board_img_tag_prompt | model | StrOutputParser()
        ai_img_tag = chain.invoke({"query": json.dumps(image_vision)})
    print("ai_img_tag : ", ai_img_tag)
    data["ai_img_tag"] = ai_img_tag
    chain = board_summation_prompt | model | StrOutputParser()
    summation = chain.invoke({"subject": data["subject"], "content": data["content"], "ai_img_tag": data["ai_img_tag"]})
    data["summation"] = summation
    data["deleted"] = False
    data["created_at"] = datetime.now()
    data["bHit"] = 0
    print(f"summation : {summation}")
    result = collection.insert_one(data)
    print(f"database save ok : {result.inserted_id}")
    return True
