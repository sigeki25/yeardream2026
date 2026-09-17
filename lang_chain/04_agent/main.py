from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import agent_service

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
app.mount("/view", StaticFiles(directory="view"))
app.include_router(agent_service.router)

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")
