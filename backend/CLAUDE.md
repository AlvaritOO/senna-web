# Backend Senna (FastAPI)

- `app/asistente.py`  cerebro: system prompt + tools + bucle de function-calling.
  REGLA: el modelo nunca inventa datos; todo sale de tools que consultan la DB.
- `app/db.py`         acceso a Postgres; cada función devuelve texto para tool_result.
- `app/routers/chat.py`      endpoint del widget web (POST /chat).
- `app/routers/whatsapp.py`  webhook Meta Cloud API; envío aislado en `_enviar()`.
- `sql/001_schema.sql`  esquema; pgvector preparado pero inactivo.

## Para crecer
- Memoria multi-turno en WhatsApp: guardar historial por número en Redis.
- Activar RAG: poblar tabla `conocimiento` + tool `buscar_conocimiento` (pgvector).
- Cambiar de proveedor de WhatsApp: reescribir solo `_enviar()`.

## Comandos
- `docker compose up --build` (desde la raíz) levanta API + Postgres + Redis.
- API en http://localhost:8000 — salud en `/`.
