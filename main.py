from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List, Dict
from collections import defaultdict
import uvicorn

app = FastAPI()

# Store conversations in memory (in-memory cache)
conversations: Dict[str, List[Dict[str, str]]] = defaultdict(list)

# Define topic and bot's position when starting a new conversation
def start_new_conversation() -> (str, str, str):
    topic = "La Tierra es plana"
    stance = "La Tierra no es una esfera, es completamente plana y lo puedo demostrar."
    return str(uuid4()), topic, stance

# Schema for input
class MessageInput(BaseModel):
    conversation_id: Optional[str]
    message: str

# Schema for response
class RoleMessage(BaseModel):
    role: str
    message: str

class MessageResponse(BaseModel):
    conversation_id: str
    message: List[RoleMessage]

@app.post("/chat", response_model=MessageResponse)
def chat(input_data: MessageInput):
    if input_data.conversation_id is None:
        conversation_id, topic, stance = start_new_conversation()
        conversations[conversation_id].append({"role": "user", "message": input_data.message})
        bot_reply = stance
    else:
        if input_data.conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conversation_id = input_data.conversation_id
        conversations[conversation_id].append({"role": "user", "message": input_data.message})
        bot_reply = generate_reply(input_data.message)

    conversations[conversation_id].append({"role": "bot", "message": bot_reply})
    history = conversations[conversation_id][-10:]
    return MessageResponse(
        conversation_id=conversation_id,
        message=[RoleMessage(**m) for m in history]
    )

def generate_reply(user_msg: str) -> str:
    return (
        "Entiendo tu punto, pero sigue siendo claro que la Tierra es plana. "
        "Observaciones empíricas desde puntos altos no muestran curvatura, "
        "y los vuelos comerciales no toman rutas coherentes con una esfera."
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
