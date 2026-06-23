"""Tests del backend Senna. Corren sin DB ni red: validan contratos y manejo
de errores, no llamadas reales a Postgres o Anthropic."""
import os
os.environ.setdefault("WHATSAPP_VERIFY_TOKEN", "token-de-prueba")

from fastapi.testclient import TestClient
from app.main import app
from app import asistente, db

cliente = TestClient(app)


def test_salud():
    r = cliente.get("/")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_chat_responde_texto():
    # Sin ANTHROPIC_API_KEY el asistente cae al mensaje de respaldo, pero
    # SIEMPRE debe devolver un string no vacío y status 200.
    r = cliente.post("/chat", json={"mensajes": [{"rol": "usuario", "texto": "hola"}]})
    assert r.status_code == 200
    assert isinstance(r.json()["respuesta"], str)
    assert len(r.json()["respuesta"]) > 0


def test_webhook_verifica_token_correcto():
    r = cliente.get("/webhook/whatsapp", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "token-de-prueba",
        "hub.challenge": "1234",
    })
    assert r.status_code == 200
    assert r.text == "1234"


def test_webhook_rechaza_token_incorrecto():
    r = cliente.get("/webhook/whatsapp", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "malo",
        "hub.challenge": "1234",
    })
    assert r.status_code == 403


def test_tools_bien_formadas():
    nombres = {t["name"] for t in asistente.TOOLS}
    assert {"listar_unidades", "consultar_disponibilidad", "crear_lead"} <= nombres
    for t in asistente.TOOLS:
        assert "description" in t and "input_schema" in t


def test_db_degrada_sin_conexion():
    # Sin Postgres, las funciones devuelven un string explicativo, no excepción.
    assert isinstance(db.listar_unidades(), str)
    assert isinstance(db.consultar_disponibilidad("requinoa"), str)
    assert isinstance(db.crear_lead({"contacto": "+569..."}), str)
