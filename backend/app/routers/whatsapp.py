"""Webhook de WhatsApp — agnóstico de proveedor.

Implementado contra **Meta WhatsApp Cloud API** (recomendado para empezar: sin
margen de un BSP). La capa de envío está aislada en `_enviar()`: si mañana
cambias a Twilio / 360dialog / Wati, solo reescribes esa función.

Pasos para activarlo (ver README):
1. App en Meta for Developers + número en Cloud API.
2. Webhook: URL pública de este servicio + WHATSAPP_VERIFY_TOKEN.
3. WHATSAPP_TOKEN y WHATSAPP_PHONE_NUMBER_ID en .env.
"""
import httpx
from fastapi import APIRouter, Request, Response
from .. import config
from ..asistente import responder

router = APIRouter()

# Verificación inicial del webhook (Meta hace un GET con un challenge).
@router.get("/webhook/whatsapp")
def verificar(request: Request):
    p = request.query_params
    if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == config.WHATSAPP_VERIFY_TOKEN:
        return Response(content=p.get("hub.challenge", ""), media_type="text/plain")
    return Response(status_code=403)

# Recepción de mensajes entrantes.
@router.post("/webhook/whatsapp")
async def recibir(request: Request):
    data = await request.json()
    for entrada in data.get("entry", []):
        for cambio in entrada.get("changes", []):
            for msg in cambio.get("value", {}).get("messages", []):
                if msg.get("type") != "text":
                    continue
                de = msg["from"]
                texto = msg["text"]["body"]
                # Sin memoria multi-turno por simplicidad; añadir historial en Redis.
                respuesta = responder([{"rol": "usuario", "texto": texto}])
                await _enviar(de, respuesta)
    return {"ok": True}

async def _enviar(a: str, texto: str):
    """Única función dependiente del proveedor (Meta Cloud API)."""
    if not config.WHATSAPP_TOKEN:
        return  # sin credenciales: no-op (útil en desarrollo)
    url = f"https://graph.facebook.com/v21.0/{config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    async with httpx.AsyncClient() as http:
        await http.post(url, headers={"Authorization": f"Bearer {config.WHATSAPP_TOKEN}"},
                        json={"messaging_product": "whatsapp", "to": a,
                              "type": "text", "text": {"body": texto}})
