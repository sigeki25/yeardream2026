import chromadb

client = chromadb.PersistentClient("./my_db")
coll = client.get_or_create_collection("study")

# 데이터 추가
"""
coll.add(
    documents=["파이썬 기초 문법 가이드", "자바 고급 성능 최적화"],
    metadatas=[
        {"lang": "python", "level": "beginner", "version": 3.19},
        {"lang": "java", "level": "advance", "version": 25},
    ],
    ids=["doc1", "doc2"]
)
"""

# 공부할 내용 추천
results = coll.query(
    query_texts=["서버 공부할 내용을 추천해줘"],
    n_results=1,
    where={
        "$and":[
            {"lang": {"$eq": "java"}},
            {"level": {"$eq": "advance"}}
        ]
    }
)

print(results)