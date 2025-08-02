from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import uvicorn
import os
import random

from ai import text_to_speech_elevenlabs

# Load environment variables
load_dotenv()

# Get API keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY2')
print('ggggggggggggggggggggggggggggg',GROQ_API_KEY)
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    user_input = chat_message.message

    # Baby "working" phrases
    baby_working_phrases = [
        "Umm... wait, Lala is thinking... 🤔",
        "Hold on! Lala is looking for her answer... 🍼",
        "Lala is working really hard... just a sec! 👶",
        "Hmm... Lala is trying to remember... 🧸",
        "Wait! Lala is poking her brain... 🧠"
    ]
    working_message = random.choice(baby_working_phrases)

    prompt = f"""You are a 10-year-old baby girl named Lala. You are very clumsy, forget things easily, and talk silly.
You never give long or logical answers. You act mischievous and funny.give  every non verbal communication and cute actions enclose in square brackets eg:[giggles],[laughs],[smiles],[frowns],[bounces up and down],[trips over own feet] etc.do not use stars.

User: {user_input}
Lala:"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "model": "llama3-8b-8192"
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        lala_reply = response_data["choices"][0]["message"]["content"]
        audio=text_to_speech_elevenlabs(lala_reply, "uq8azAkk0wBebQXhvpc8", "assets/elevenlabs_output.mp3")
        return JSONResponse({
            "working": working_message,
            "reply": lala_reply.strip(),
            "length": len(lala_reply.strip()),
            "audio": "assets/elevenlabs_output.mp3"
        })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Invalid response from Groq API")

@app.get("/assets/{filename}")
async def get_asset(filename: str):
    file_path = os.path.join("assets", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    response = StreamingResponse(open(file_path, "rb"), media_type="application/octet-stream")
    
    # Disable caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
# if __name__ == "__main__":

    # uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
