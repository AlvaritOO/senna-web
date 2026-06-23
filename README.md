# Senna — Sitio multi-unidad

Departamentos amoblados en Rancagua. Dos unidades distintas por ubicación,
distribución, estadía y equipamiento. Vitrina + captación de leads, con
asistente por chat web y WhatsApp.

```
senna-web/
├─ frontend/   Astro + Svelte (despliega en Vercel) — el sitio público
├─ backend/    FastAPI dockerizado — asistente + webhook WhatsApp
├─ docker-compose.yml   API + Postgres(pgvector) + Redis para desarrollo
└─ CLAUDE.md   contexto raíz para Claude Code
```

## 1. Subir a GitHub
```bash
cd senna-web
git init && git add . && git commit -m "Senna: sitio multi-unidad inicial"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/senna-web.git
git push -u origin main
```

## 2. Desplegar el sitio (rápido, ya se ve)
En vercel.com → New Project → importa el repo. Configura:
- **Root Directory:** `frontend`
- Framework: Astro (se autodetecta)
- Variables de entorno:
  - `PUBLIC_WHATSAPP` = `56966078526`
  - `PUBLIC_API_URL` = URL del backend (cuando lo tengas; mientras, el chat
    cae elegante a WhatsApp).

Deploy. El sitio queda online con la Unidad 1 y sus fotos reales.

## 3. Backend (cuando quieras el asistente activo)
```bash
cp .env.example .env     # completa ANTHROPIC_API_KEY y, luego, WhatsApp
docker compose up --build
# API en http://localhost:8000
```
Para producción: súbelo a un host con contenedores (Fly.io / Railway / VPS) y
pon esa URL en `PUBLIC_API_URL` del frontend.

## 4. WhatsApp (Meta Cloud API)
La app normal de WhatsApp Business **no** permite bots. Necesitas Cloud API:
1. Crea una app en developers.facebook.com y agrega WhatsApp.
2. Registra un número dedicado a la API.
3. Webhook → URL pública: `https://TU_BACKEND/webhook/whatsapp`, y pon el
   mismo `WHATSAPP_VERIFY_TOKEN` que en `.env`.
4. Copia `WHATSAPP_TOKEN` y `WHATSAPP_PHONE_NUMBER_ID` al `.env`.
Recomendación para partir: Cloud API directo de Meta (sin margen de un BSP como
Twilio/Wati). El envío está aislado en `backend/app/routers/whatsapp.py::_enviar`
por si luego cambias de proveedor.

## Pendientes
- [ ] Unidad 2: fotos y datos reales (hoy es plantilla en `frontend/src/data/unidades.ts`).
- [ ] Conectar Supabase real y migrar los datos desde el archivo a la DB.
- [ ] Activar el asistente con tu `ANTHROPIC_API_KEY`.

## Trabajar con Claude Code
Hay un `CLAUDE.md` en la raíz, en `frontend/` y en `backend/` con las
convenciones (español, tokens de marca, reglas del asistente). Claude Code los
lee según dónde esté trabajando.
