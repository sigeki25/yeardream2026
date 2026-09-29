# Hash 암호화
import datetime
import logging
import secrets
from typing import Dict, Any

import bcrypt
import jwt


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def encode_pass(plain: str):
    # 1. 문자열을 byte 형태로 변환
    plane_bytes = plain.encode("utf-8")
    # 2. 해시 암호화 진행
    # salt 값 : 같은 입력을 하여도 결과값이 다르게 나오게 하는 하나의 값
    enc_bytes = bcrypt.hashpw(plane_bytes, bcrypt.gensalt())
    # 3. 문자 형태로 변경(DB 에 저장하기 위해)
    return enc_bytes.decode("utf-8")


# 암호화 확인
def matches(plain: str, hash: str):
    return bcrypt.checkpw(plain.encode("utf-8"), hash.encode("utf-8"))


"""
plane_text = input("암호하 하려는 문자열을 입력하세요 : ")
hash_text = encode_pass(plane_text)
print(hash_text)
# input : 125
# $2b$12$mzxO1wzWvDrooSvbpTYeXOuwGVYsFKReYP/vDR/g0MH.sWH32Sz.S
# $2b$12$CN6oJvtHywYzvXGuWmCUVONl1d/MWU0emc.wVgNE1Va9dlKnYS1nq


confirm_text = input("방금 입력한 암호를 다시 입력하세요 : ")
check = matches(confirm_text, hash_text)
print(f"일치 여부 : {check}")

check = matches(confirm_text, "$2b$12$mzxO1wzWvDrooSvbpTYeXOuwGVYsFKReYP/vDR/g0MH.sWH32Sz.S")
print(f"일치 여부 : {check}")
check = matches(confirm_text, "$2b$12$CN6oJvtHywYzvXGuWmCUVONl1d/MWU0emc.wVgNE1Va9dlKnYS1nq")
print(f"일치 여부 : {check}")
"""

# JWT
# 비밀키, 알고리즘 종류, 유지시간
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 30


def get_token(data: Dict[str, Any]) -> str:
    """
    특정한 내용을 넣으면 토큰으로 생성
    :param data: 토큰에 저장할 내용
    :return: 토큰 문자열
    """
    # 내용에는 토큰 수명도 추가해야 함
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRE_MIN)
    data.update({"exp": expire_time})
    # jwt.encode(내용, 비밀키, 알고리즘)
    return jwt.encode(data, SECRET_KEY, ALGORITHM)


def verify_token(token: str) -> Dict[str, Any] | None:
    """
    토큰 문자열을 넣으면 토큰에 저장된 데이터를 반환
    :param token: 토큰 문자열
    :return: 토큰의 내용이 담긴 Dict
    """
    payload = None
    try:
        jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as e: # 비밀키가 틀렸거나, 토큰 시간이 만료된 경우
        logger.error(e)
    return payload

# result_token = get_token({"id": "admin", "name": "어드민"})
# logger.info(f"result_token : {result_token}")
# result_payload = verify_token(result_token)
# logger.info(f"result_payload : {result_payload}")
