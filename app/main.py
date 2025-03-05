from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import requests
from typing import List, AsyncGenerator

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"

gemma2 ="hf.co/bartowski/gemma-2-2b-it-GGUF:Q6_K"

class Message(BaseModel):
    role: str
    content: str

async def stream_ollama_response(messages: List[Message]) -> AsyncGenerator[bytes, None]:
    payload = {
        "model": gemma2,
        "messages": [msg.dict() for msg in messages],
        "stream": True,
    }

    with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
        for chunk in response.iter_lines():
            if chunk:
                yield chunk + b"\n"

@app.post("/chat")
async def chat(messages: List[Message]):
    return StreamingResponse(stream_ollama_response(messages), media_type="text/event-stream")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")
