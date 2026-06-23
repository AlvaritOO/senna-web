"""Punto de entrada FastAPI."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, whatsapp

app = FastAPI(title="Senna API")

_origenes_raw = os.getenv("CORS_ORIGINS", "*")
_origenes = [o.strip() for o in _origenes_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origenes,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(chat.router)
app.include_router(whatsapp.router)

@app.get("/")
def salud():
    return {"servicio": "senna-api", "ok": True}
