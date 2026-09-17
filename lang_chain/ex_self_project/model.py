from pydantic import BaseModel, Field

class ReviewAnalysis(BaseModel):
    sentiment: str = Field(description="긍정, 부정, 중립 중 하나로 반드시 한국어로 출력")
    score: int = Field(description="1점 부터 5점 까지의 만족도 점수, 1점에서 5점 사이의 정수로만 출력")
    summary: str = Field(description="리뷰 핵심 내용을 한줄 요약")
