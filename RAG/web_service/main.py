import logging
from typing import List

from fastapi import FastAPI, UploadFile, Form, File
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount('/view', StaticFiles(directory='view'))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     [%(name)s] %(message)s - %(asctime)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("__name__")


@app.get("/")
def main():
    logger.info("main page request")
    return RedirectResponse("/view/index.html")


@app.get("/chat")
def chat():
    return RedirectResponse("/view/chat.html")


# file 과 문자열 파리메터가 섞여서 들어올때 처리 방법
@app.post("/upload")
def upload(subject: str = Form(...), files: List[UploadFile] = File([])):
    logger.info(f"subject : {subject}")
    logger.info(f"files : {files}")
    return {"upload": "Test"}
