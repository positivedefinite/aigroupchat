key = "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"
import json
import time
import openai
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

openai.api_key = key

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    username: str
    content: str

chat_history = []


async def get_chat_history():
    return chat_history


@app.get("/", response_class=HTMLResponse)
async def index():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, chat_history: List[Message] = Depends(get_chat_history)):
    await websocket.accept()
    print(f"User registered {username}")
    # Send the chat history to the new user
    with open("message_history.json", "r") as f:
        chat_history_data = json.load(f)
        for message in chat_history_data:
            await websocket.send_text(f"{message['username']}: {message['content']}")
    print(f"Chat history loaded for {username}")
    while True:
        data = await websocket.receive_text()
        message = Message(username=username, content=data)
        chat_history.append(message)

        await websocket.send_text(f"{username}: {data}")
        print(f"User provided: {username}: {data}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Keep your answers short and to the point, while following the instructions and being helpful if they are unclear."},
                {"role": "user", "content": data},
            ]
        )
        ai_message = response.choices[0].message["content"]
        chat_history.append(Message(username="Hackabrain", content=ai_message))
        await websocket.send_text(f"Hackabrain: {ai_message}")

        with open("message_history.json", "w") as f:
            json.dump([m.dict() for m in chat_history], f)
        print(f"Chat saved {len(chat_history)}")
