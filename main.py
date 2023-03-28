import json, os, time, openai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

#[System.Environment]::SetEnvironmentVariable('ResourceGroup','AZ_Resource_Group')

metaprompt = "Keep your answers short and to the point, while following the instructions and being helpful if they are unclear."
model = "gpt-3.5-turbo"
openai.api_key = os.environ["OPENAIAPI"]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    content: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_main.html", {"request": request})

@app.post("/generate_response")
async def generate_response_endpoint(message: Message):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": metaprompt},
            {"role": "user", "content": message.content},
        ]
    )
    return {"message": response.choices[0].message["content"]}