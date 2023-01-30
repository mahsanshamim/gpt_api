from pyexpat import model
from sys import prefix
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from routers.gptRouter import router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from typing import Union

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router,prefix='/gpt', tags=['GPT API'])

templates = Jinja2Templates(directory="templates")
@app.get('/')
async def Home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

