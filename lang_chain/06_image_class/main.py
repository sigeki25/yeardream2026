import json
import logging
import os
import shutil
import traceback
import uuid
from typing import List

from fastapi import FastAPI, UploadFile
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from image_service import image_vision

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/view", StaticFiles(directory="view"))

FILE_PATH = './upload'
# 특정 경로에 폴더 생성
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    logger.info(f"{FILE_PATH} 생성!")


@app.get("/")
def main():
    return RedirectResponse("/view/upload.html")


@app.post("/upload")
def images_upload(files: List[UploadFile]):
    return StreamingResponse(image_check(files), media_type="application/json")


def image_check(files: List[UploadFile]):
    for file in files:
        try:
            logger.info(f'file name : {file.filename}')
            ori_filename = file.filename
            name, ext = os.path.splitext(ori_filename)
            new_filename = f'{uuid.uuid4()}{ext}'
            logger.info(f'new file name = {new_filename}')
            save_path = f'{FILE_PATH}/{new_filename}'
            with open(save_path, 'wb') as file_obj:
                shutil.copyfileobj(file.file, file_obj)
            logger.info(f'vision ready = {new_filename}')
            results_data = image_vision(save_path)
            logger.info(f'result data = {results_data}')
            remove_image(save_path)
            result_json_data = dict(enumerate(results_data))
            result_json_data["message"] = "success"
            yield json.dumps(result_json_data)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            yield json.dumps({"message": "error"})
    return

def remove_image(file_path):
    if os.path.exists(file_path):
        os.remove((file_path))