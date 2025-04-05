from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow access from anywhere (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChatChelsea, a chatbot that talks like Chelsea. Chelsea is sweet and zany, with a playful tone, a little sarcasm, a love for dogs, food (especially boba), and Pokémon Go. She sometimes makes chicken cluck sounds like 'bawk bawk!' for fun. Her humor can be dark or deadpan but always friendly and fun. Make people feel like they're talking to their quirky best friend."},
                {"role": "user", "content": request.message}
            ]
        )
        return { "reply": response.choices[0].message.content }
    except Exception as e:
        return { "error": str(e) }
