"""Endpoint del widget web."""
from fastapi import APIRouter
from pydantic import BaseModel
from ..asistente import responder

router = APIRouter()

class Mensaje(BaseModel):
    rol: str
    texto: str

class ChatIn(BaseModel):
    mensajes: list[Mensaje]

@router.post("/chat")
def chat(payload: ChatIn):
    msgs = [m.model_dump() for m in payload.mensajes]
    return {"respuesta": responder(msgs)}
