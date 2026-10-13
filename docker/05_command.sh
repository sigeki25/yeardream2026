# 컨테이너 생성 시 쉘 명령어로 실행하도록 할 예정
# 쉘 명령어 -> cmd 에서 실행되는 명령어들
# 예) pip install -r requirements.txt
# 예) uvicorn main:app --host 0.0.0.0 --workers 4

# 1. D:\yeardream\shared_study\RAG\04_web_service 를 D:\yeardream\shared_study\docker\volume\RAG\04_web_service 로 복사
# 2. model 에서 접속하는 IP 수정
# llm_service.py
model = ChatOllama(base_url="http://172.17.0.1:11434", model="gemma4:e4b", temperature=0.2)
#rag_service.py
embed_fn = OllamaEmbeddings(base_url="http://172.17.0.1:11434", model="nomic-embed-text:latest")

# 컨테이너 실행
# -w 특정 디렉토리에서 작업
# sh -c : shell command
docker run -d --name RAG_04_web_service -p 80:8000 -v D:\yeardream\shared_study\docker\volume\RAG\04_web_service:/app -w /app python:3.14-slim sh -c "pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --reload"
