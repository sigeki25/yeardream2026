# uv pip install fastapi uvicorn
# uvicorn main:app --host=0.0.0.0
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"message": "test"}