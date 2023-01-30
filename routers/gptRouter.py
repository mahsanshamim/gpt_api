from email import message
from fastapi import APIRouter, HTTPException, Path, Depends, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from config.config import *
import openai
from models.schema import RequestSchema, Response
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
router = APIRouter()


templates = Jinja2Templates(directory="templates")
@router.get('/')
async def get(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/uploadfile/")
async def create_upload_file(request: Request,file: UploadFile = File(description="Multiple files as UploadFile",default=None)):
    try:
        openai.api_key = openai_key
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        img = file.file.read()
        io_bytes = io.BytesIO(img)
        img = Image.open(io_bytes)
        # img = cv2.imread(img)
        print(type(img))
        img = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2RGB)
        imgocr = pytesseract.image_to_string(img)
        imgocr = imgocr.replace('\/n','<br/>')
        response = openai.Completion.create(
                model=model,
                prompt=imgocr,
                max_tokens=max_tokens,
                temperature=temperature,
        )
        result = response.choices[0].text
        response = {"text":imgocr, "result": result}
        return Response(code=200, status='Ok', message='Success', result=response).dict(exclude_none=True )
    except Exception as e:
        return Response(code=500, status='Error', message='Try Again', result=e).dict(exclude_none=True )