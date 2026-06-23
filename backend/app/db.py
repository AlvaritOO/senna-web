"""Acceso a datos. Devuelve texto listo para que el asistente lo use como
tool_result. Hoy consulta Postgres; con dos unidades es más que suficiente."""
import json
import psycopg
from . import config

def _conn():
    return psycopg.connect(config.DATABASE_URL)

def listar_unidades() -> str:
    try:
        with _conn() as c, c.cursor() as cur:
            cur.execute("""
                SELECT slug, nombre, ubicacion, distribucion, equipamiento,
                       estadia_minima, precio_valor, precio_unidad, precio_nota
                FROM unidades ORDER BY numero
            """)
            filas = cur.fetchall()
        if not filas:
            return "Aún no hay unidades cargadas."
        return json.dumps([
            {"slug": f[0], "nombre": f[1], "ubicacion": f[2], "distribucion": f[3],
             "equipamiento": f[4], "estadia_minima": f[5],
             "precio": f"{f[6]} {f[7]} ({f[8]})" if f[6] else "a consultar"}
            for f in filas
        ], ensure_ascii=False)
    except Exception as e:
        return f"No pude leer las unidades ({e}). Deriva a WhatsApp."

def consultar_disponibilidad(slug: str, desde=None, hasta=None) -> str:
    try:
        with _conn() as c, c.cursor() as cur:
            cur.execute("""
                SELECT desde, hasta FROM disponibilidad
                WHERE slug = %s AND estado = 'ocupado'
                  AND (%s IS NULL OR hasta >= %s::date)
                  AND (%s IS NULL OR desde <= %s::date)
                ORDER BY desde
            """, (slug, desde, desde, hasta, hasta))
            ocupados = cur.fetchall()
        if not ocupados:
            return f"La unidad {slug} aparece disponible en ese rango."
        bloques = "; ".join(f"{o[0]} a {o[1]}" for o in ocupados)
        return f"La unidad {slug} tiene ocupado: {bloques}. Confirmar por WhatsApp."
    except Exception as e:
        return f"No pude consultar disponibilidad ({e}). Deriva a WhatsApp."

def crear_lead(args: dict) -> str:
    try:
        with _conn() as c, c.cursor() as cur:
            cur.execute("""
                INSERT INTO leads (nombre, contacto, slug, mensaje)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (args.get("nombre"), args.get("contacto"),
                  args.get("slug"), args.get("mensaje")))
            lead_id = cur.fetchone()[0]
            c.commit()
        return f"Lead #{lead_id} guardado. Un asesor lo contactará pronto."
    except Exception as e:
        return f"No pude guardar el lead ({e}). Pide el contacto por WhatsApp."
