"""Punto de entrada FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, whatsapp

app = FastAPI(title="Senna API")

# CORS: ajustar allow_origins al dominio del frontend en producción.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(whatsapp.router)

@app.get("/")
def salud():
    return {"servicio": "senna-api", "ok": True}
