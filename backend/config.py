"""
Configuración centralizada del backend.

Todas las variables se pueden sobrescribir con variables de entorno
con el prefijo RAGNAR_ (ej: RAGNAR_PORT=9000, RAGNAR_DEBUG=true).
También acepta un archivo .env en la raíz del proyecto.
"""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del backend con valores por defecto sensatos."""

    model_config = SettingsConfigDict(
        env_prefix="RAGNAR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Aplicación ---
    app_name: str = "ragnar"
    user_id: str = "empleado"
    debug: bool = False

    # --- Servidor ---
    host: str = "127.0.0.1"
    port: int = 8000

    # --- CORS (orígenes del frontend) ---
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # --- Agente ---
    agent_timeout: int = 120  # segundos máximos por turno del agente


settings = Settings()


def setup_logging() -> None:
    """Configura el logging del backend con formato legible."""
    level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    # Silenciar loggers ruidosos de terceros
    for nombre in ("httpx", "httpcore", "chromadb", "LiteLLM", "urllib3"):
        logging.getLogger(nombre).setLevel(logging.WARNING)
