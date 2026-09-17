from datetime import datetime

from langchain_core.tools import tool


@tool
def check_weather(location:str) -> str:
    """
    특정 지역의 현재 날씨를 확인하는 도구입니다.
    :param location: 지역
    :return: 현재의 기상 상황을 반환, 예) 맑음
    """
    print(f"{location} 지역 날씨 데이터 크롤링")
    return "맑음"

@tool
def now_date() -> str:
    """
    현재(오늘) 날씨와 시간을 확인해주는 도구 입니다.
    :return: "0000-00-00 00:00:00" 형식으로 반환, 예) 2026-09-11 :13:38:30
    """
    curr_datetime = datetime.now()
    fmt_datetime = curr_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f"현재 날짜와 시간 : {fmt_datetime}")
    return fmt_datetime

@tool
def check_stock() -> str:
    """
    현재(오늘) 주식시장의 현황을 알려주는 도구 입니다.
    :return:
    """
    print("주요 뉴스시이트에서 주식 정보 크롤링")
    return "오늘의 주식시장은 나쁘지 않습니다."