import os

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import board
from setting import FILE_PATH

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"))
app.include_router(board.router)
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

@app.get("/")
def main():
    return RedirectResponse("/board")