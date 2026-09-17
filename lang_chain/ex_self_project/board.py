import os
import shutil
import traceback
import uuid
from typing import Dict, Any, Annotated, Optional

from fastapi import APIRouter, Request, UploadFile
from fastapi.params import Form, File
from starlette.templating import Jinja2Templates

from ai_service import board_tag
from mongoDB import get_collection
from setting import FILE_PATH, logger

router = APIRouter(prefix="/board", tags=["board"])
templates = Jinja2Templates(directory="templates")
collection = get_collection("board")

@router.get("")
def board_main(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="board/index.html",
        context={},
    )

@router.get("/list")
def get_board_list(page:int=1):
    print(page)
    result = collection.find({"deleted": False})
    print("result : ", result)
    return {"list": list(result)}

@router.get("/write")
def write_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="board/write.html",
        context={},
    )

@router.post("/write")
async def write(
    user_name: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    content: Annotated[str, Form()],
    file: Optional[UploadFile] = File(None)  # Use File() for file uploads
):
    print(user_name, subject, content)
    print(file)
    file_path=None

    msg = "파일업로드에 실패 했습니다."
    if file is not None:
        try:
            ori_filename = file.filename
            name,ext = os.path.splitext(ori_filename)
            new_filename = f'{uuid.uuid4()}{ext}'
            save_path = f'{FILE_PATH}/{new_filename}'
            with open(save_path,'wb') as file_obj:
                shutil.copyfileobj(file.file, file_obj)
            file_path = save_path
            msg = "파일 업로드에 성공 했습니다."
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc()) # 상세 에러로그 보기
    datas = {"user_name": user_name, "subject": subject, "content": content, "file": file_path}
    await board_tag(datas, collection)
    # if files is None:
    return {"success": True}