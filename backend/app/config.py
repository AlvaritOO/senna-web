"""Configuración central leída desde variables de entorno."""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://senna:senna@db:5432/senna")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODELO_ASISTENTE = os.getenv("MODELO_ASISTENTE", "claude-haiku-4-5-20251001")

WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "cambia-esto")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

# Número humano de respaldo (formato wa.me, sin +)
WHATSAPP_HUMANO = "56966078526"
