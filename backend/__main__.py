"""Permite ejecutar el backend con: python -m backend"""

import uvicorn

from .config import settings

uvicorn.run(
    "backend.main:app",
    host=settings.host,
    port=settings.port,
    reload=settings.debug,
)
