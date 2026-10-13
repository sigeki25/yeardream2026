# ollama 를 도커에 설치(설치와 삭제가 쉬워서)
# 1. 기존 ollama model 을 삭제
# ollama rm [모델명]
ollama list  # 모델이 남지 않음을 확인

# ollama image 탐색 및 다운로드
docker search ollama
docker pull ollama/ollama

# GPU 지원 여부
nvidia-smi

# 컨테이너 실행
# -d : 백그라운드 실행
# --gpus=all : 가용되는 GPU 모두 사용(GPU 사용 가능 환경에서만)
# -v : 로컬경로:컨테이너내 경로
# -p : 호출포트:컨테이너에서 사용포트
# --name : 컨테이너 이름
# docker run [옵션] [사용 이미지]
docker run -d --gpus=all -v D:\yeardream\shared_study\docker\ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# 실행중인 컨테이너 리스트
docker ps

# docker 내부 터미널로 접속
# docker exec -it [컨테이너 이름] /bin/bash
docker exec -it ollama /bin/bash

# ollama run gemma4:e4b
# ollama run bge-m3 <- embed 모드이기 때문에 에러가 호출됨(대화 모드가 없음)

# 1. fast-api 를 컨테이너에 올리기
# 대상 : D:\yeardream\shared_study\lang_chain\01_start
# 1. 대상 폴더에서 .env, .idea, __pycache__ 를 제외한 모든 파일을 복사
# 2. 로컬과 컨테이너를 연결할 볼륨 폴더를 생성(D:\yeardream\shared_study\docker\volume\fastapi\app)
# 3. 복사한 파일들을 이동

# 컨테이너 실행
# python:3.14-slim 이미지를 받은 적이 없어도 컨테이너 생성 시 자동으로 다운로드
docker run -d --name fastapi -p 80:8000 -v D:\yeardream\shared_study\docker\volume\fastapi\app:/app python:3.14-slim

# 실패한 컨테이너는 실패상태로 남아있으므로 삭제해야함
docker container rm -f fastapi

# -it : 터미널로 연결, 터미널 연결을 대기하므로 설치 등의 문구가 없어 실패하지 않는다.
docker run -d -it --name fastapi -p 80:8000 -v D:\yeardream\shared_study\docker\volume\fastapi\app:/app python:3.14-slim

# 터미널 짐입
docker exec -it fastapi /bin/bash

# app 톨더로 이동
cd /app
# 파일 리스트 확인
ls
# 라이브러리 설치
pip install -r requirements.txt

# 실행
uvicorn main:app --host 0.0.0.0 --workers 1 --reload

# 컨테이너 사이에는 도커 내부에서 사용하는 사설IP가 존재
# 이 IP를 통해 컨테이너 간의 통신을 해야 함(172.17.0.1)
# 모델을 불러오는 호출부에 IP주소 추가
# model = ChatOllama(base_url="172.17.0.1:11434", model="exaone3.5:2.4b")