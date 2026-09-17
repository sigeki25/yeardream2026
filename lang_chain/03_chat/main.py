from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import chat

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
app.mount("/view", StaticFiles(directory="view"))
app.include_router(chat.router)

@app.get("/")
def main():
    return RedirectResponse("/view/chat.html")