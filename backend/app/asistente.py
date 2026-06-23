"""Cerebro del asistente Senna.

Diseño clave: el modelo NO inventa disponibilidad ni precios. Toda dato real
sale de la base de datos vía *tools* (function calling). Con solo dos unidades,
la ficha completa cabe en el contexto, así que NO se usa base vectorial todavía;
cuando crezca el conocimiento (FAQ, guías de barrio, más edificios) se activa
pgvector y se agrega una tool `buscar_conocimiento`.
"""
from anthropic import Anthropic
from . import config, db

cliente = Anthropic(api_key=config.ANTHROPIC_API_KEY) if config.ANTHROPIC_API_KEY else None

SYSTEM = (
    "Eres el asistente de Senna, departamentos amoblados en Rancagua, Chile. "
    "Hablas en español de Chile, cercano pero profesional, y respondes corto. "
    "Tienes dos unidades. Nunca inventes precios ni disponibilidad: usa las "
    "herramientas para consultarlos. Si el usuario quiere reservar o pide algo "
    "que no puedes resolver, ofrece continuar por WhatsApp con un humano "
    f"(+{config.WHATSAPP_HUMANO}). No prometas nada que no salga de las tools."
)

TOOLS = [
    {
        "name": "listar_unidades",
        "description": "Devuelve las unidades Senna con ubicación, distribución, equipamiento y precio.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "consultar_disponibilidad",
        "description": "Disponibilidad de una unidad para un rango de fechas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Identificador de la unidad"},
                "desde": {"type": "string", "description": "Fecha ISO YYYY-MM-DD"},
                "hasta": {"type": "string", "description": "Fecha ISO YYYY-MM-DD"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "crear_lead",
        "description": "Guarda un lead interesado (nombre y contacto) para seguimiento.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string"},
                "contacto": {"type": "string", "description": "Teléfono o correo"},
                "slug": {"type": "string"},
                "mensaje": {"type": "string"},
            },
            "required": ["contacto"],
        },
    },
]

def _ejecutar_tool(nombre: str, args: dict) -> str:
    if nombre == "listar_unidades":
        return db.listar_unidades()
    if nombre == "consultar_disponibilidad":
        return db.consultar_disponibilidad(args.get("slug"), args.get("desde"), args.get("hasta"))
    if nombre == "crear_lead":
        return db.crear_lead(args)
    return "Herramienta desconocida."

def responder(mensajes: list[dict]) -> str:
    """mensajes: [{rol, texto}] del frontend -> respuesta de texto del asistente."""
    if cliente is None:
        return ("El asistente aún no está configurado (falta ANTHROPIC_API_KEY). "
                f"Escríbenos por WhatsApp al +{config.WHATSAPP_HUMANO}.")

    historial = [
        {"role": "user" if m["rol"] == "usuario" else "assistant", "content": m["texto"]}
        for m in mensajes
    ]

    # Bucle de tool-use: hasta que el modelo entregue texto final.
    for _ in range(5):
        r = cliente.messages.create(
            model=config.MODELO_ASISTENTE, max_tokens=600,
            system=SYSTEM, tools=TOOLS, messages=historial,
        )
        if r.stop_reason == "tool_use":
            historial.append({"role": "assistant", "content": r.content})
            resultados = []
            for bloque in r.content:
                if bloque.type == "tool_use":
                    salida = _ejecutar_tool(bloque.name, bloque.input or {})
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": salida,
                    })
            historial.append({"role": "user", "content": resultados})
            continue
        return "".join(b.text for b in r.content if b.type == "text")

    return f"Mejor sigamos por WhatsApp: +{config.WHATSAPP_HUMANO}."
