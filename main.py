from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List, Dict
from collections import defaultdict
import random
import uvicorn

app = FastAPI()

# Conversaciones en memoria
conversations: Dict[str, List[Dict[str, str]]] = defaultdict(list)

# Posiciones posibles del bot
POSITIONS = [
    "Estoy totalmente a favor de este punto.",
    "Estoy totalmente en contra de esta idea."
]

RESPONSE_TEMPLATES = [
    "Desde mi punto de vista, {stance}. {extra}",
    "Aunque parezca extraño, defiendo que {stance}. Considera esto: {extra}",
    "Entiendo tus dudas, pero {stance}. Te explico: {extra}",
    "Sigo convencido de que {stance}. Aquí un argumento más: {extra}",
    "Muchos lo niegan, pero {stance}. {extra}"
]

EXTRA_ARGUMENTS = [
    "Hay múltiples estudios que respaldan esta idea.",
    "Las experiencias reportadas en distintas culturas lo confirman.",
    "La lógica indica que esta es la conclusión más coherente.",
    "Los datos empíricos no muestran lo contrario.",
    "Es una cuestión que ha sido malinterpretada históricamente.",
    "Las apariencias engañan, pero los hechos son consistentes.",
    "Se han hecho experimentos que confirman esta posición."
]

# Entrada del usuario
class MessageInput(BaseModel):
    conversation_id: Optional[str]
    message: str

# Salida del bot
class RoleMessage(BaseModel):
    role: str
    message: str

class MessageResponse(BaseModel):
    conversation_id: str
    message: List[RoleMessage]

# Generador de respuesta basado en postura
def generate_reply(user_msg: str, stance: str) -> str:
    template = random.choice(RESPONSE_TEMPLATES)
    extra = random.choice(EXTRA_ARGUMENTS)
    return template.format(stance=stance, extra=extra)

@app.post("/chat", response_model=MessageResponse)
def chat(input_data: MessageInput):
    if input_data.conversation_id is None:
        # Nueva conversación
        conversation_id = str(uuid4())
        conversations[conversation_id].append({"role": "user", "message": input_data.message})

        # Elige postura aleatoria
        stance = random.choice(POSITIONS)
        conversations[conversation_id].append({"role": "bot", "message": stance})
    else:
        # Conversación existente
        conversation_id = input_data.conversation_id
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")

        conversations[conversation_id].append({"role": "user", "message": input_data.message})

        # Recuperar postura inicial
        first_bot_msg = next((m for m in conversations[conversation_id] if m["role"] == "bot"), None)
        stance = first_bot_msg["message"] if first_bot_msg else "Mantengo mi postura."

        # Generar respuesta dinámica
        bot_reply = generate_reply(input_data.message, stance)
        conversations[conversation_id].append({"role": "bot", "message": bot_reply})

    history = conversations[conversation_id][-10:]
    return MessageResponse(
        conversation_id=conversation_id,
        message=[RoleMessage(**m) for m in history]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

