import chromadb
from llama_index.core import Settings, VectorStoreIndex, ChatPromptTemplate, PromptTemplate
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# 1. 모델 등록
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.llm = Ollama(model="gemma4:e4b", request_timeout=300)

# 2. chromadb 와 llama-index 연동
client = chromadb.PersistentClient(path="store")
coll = client.get_collection("my_collection")
store = ChromaVectorStore(chroma_collection=coll)

# 3. 초개ㅡㅁ유 dml collection 불러오기
index = VectorStoreIndex.from_vector_store(store)

def query_engine(question:str):
    qa_template = ChatPromptTemplate.from_messages([
        ("system", "당신은 소설 분석 전문가입니다. 제공된 [소설 본문 발췌]를 근거로 사용자의 [질문]에 대답해 주세요."),
        ("user", "[소설 본문 발췌]\n{context_str}\n\n[질문]\n{query_str}")
    ])

    engine = index.as_query_engine(similarity_top_k=5, text_qa_template=qa_template, streaming=True)
    resp = engine.query(question)
    for chunk in resp.response_gen:
        print(chunk, end="", flush=True)

# question = input("운수 좋은날에 대한 질문을 해 주세요 : ")
# query_engine(question)

def chat_engine(question):
    prompt = PromptTemplate("[소설 본문 발췌]\n{context_str}\n\n[질문]\n{query_str}")
    engine = index.as_chat_engine(
        chat_mode="condense_plus_context",
        similarity_top_k=5,
        system_prmopt="당신은 소설 분석 전문가입니다. 제공된 [소설 본문 발췌]를 근거로 사용자의 [질문]에 대답해 주세요.",
        context_prompt=prompt
    )
    # reap = engine.chat(question) # 동기 방식(실시간이 아님)
    reap = engine.stream_chat(question)
    for chunk in reap.response_gen:
        print(chunk, end="", flush=True)
    print("\n")

while True:
    question = input("운수 좋은날에 대한 질문을 해 주세요(exit : 종료) : ")
    if question.lower() == "exit":
        break
    chat_engine(question)