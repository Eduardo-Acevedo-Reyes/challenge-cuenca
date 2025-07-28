from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List, Dict
from collections import defaultdict
import random
import uvicorn

app = FastAPI()

# === In-memory storage ===
conversations: Dict[str, List[Dict[str, str]]] = defaultdict(list)
conversation_context: Dict[str, Dict[str, str]] = {}  # Stores topic and stance

# === Input / Output Schemas ===
class MessageInput(BaseModel):
    conversation_id: Optional[str]
    message: str

class RoleMessage(BaseModel):
    role: str
    message: str

class MessageResponse(BaseModel):
    conversation_id: str
    message: List[RoleMessage]

# === Generate random stance ===
def generate_stance(user_message: str) -> str:
    stance = random.choice(["agree", "disagree"])
    if stance == "agree":
        return f"Estoy totalmente de acuerdo con lo que dijiste: '{user_message}'. Aquí está mi razonamiento..."
    else:
        return f"No estoy de acuerdo con lo que planteaste: '{user_message}'. Permíteme explicarte por qué pienso diferente."

@app.post("/chat", response_model=MessageResponse)
def chat(input_data: MessageInput):
    if input_data.conversation_id is None:
        conversation_id = str(uuid4())
        # Guardar contexto del tema y la postura
        conversation_context[conversation_id] = {
            "topic": input_data.message,
            "stance": generate_stance(input_data.message)
        }
        conversations[conversation_id].append({"role": "user", "message": input_data.message})
        bot_reply = conversation_context[conversation_id]["stance"]
    else:
        if input_data.conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        conversation_id = input_data.conversation_id
        topic = conversation_context[conversation_id]["topic"]
        conversations[conversation_id].append({"role": "user", "message": input_data.message})
        bot_reply = generate_reply(topic)

    conversations[conversation_id].append({"role": "bot", "message": bot_reply})
    history = conversations[conversation_id][-10:]
    return MessageResponse(
        conversation_id=conversation_id,
        message=[RoleMessage(**m) for m in history]
    )

# === Consistent response for a given topic ===
def generate_reply(topic: str) -> str:
    return (
        f"Sigo firme en mi posición respecto a '{topic}'. "
        f"Las evidencias y el razonamiento lógico respaldan mi punto de vista, y puedo continuar argumentando si lo deseas."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

