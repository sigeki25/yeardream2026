# uv pip install uvicorn fastapi
from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()

@app.get("/")
def main(req:Request):
    print(f"method : {req.method}")
    print(f"url : {req.url}")
    return {"info" : f"{req.method} {req.url}"}

@app.get("/setInfo")
def setInfo(req:Request):
    print(f"host : {req.client.host} : {req.client.port}")
    print(f"path : {req.url.path}")
    # /setIngo?data=data1
    print(f"query : {req.query_params}")
    print(f"data : {req.query_params.get("data")}")
    return {"msg": "OK"}
