"""
API que expone el agente de Ragnar para el frontend.

Ejecutar desde la raíz del proyecto:
    uvicorn backend.main:app --reload --port 8000

O con el módulo:
    python -m backend
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings, setup_logging
from .schemas import ChatRequest, ChatResponse
from .services import AgentConnectionError, AgentError, AgentService, AgentTimeoutError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa el servicio del agente al arrancar y limpia al cerrar."""
    setup_logging()
    logger.info("=" * 60)
    logger.info("Ragnar Backend iniciando")
    logger.info("  app_name    : %s", settings.app_name)
    logger.info("  user_id     : %s", settings.user_id)
    logger.info("  timeout     : %ds", settings.agent_timeout)
    logger.info("  CORS origins: %s", settings.allowed_origins)
    logger.info("  debug       : %s", settings.debug)
    logger.info("=" * 60)

    app.state.agent = AgentService()

    yield

    logger.info("Ragnar Backend cerrado")


# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Ragnar - Agente de inteligencia de precios",
    description=(
        "API que permite al frontend interactuar con el agente de "
        "comparación de precios de Ragnar S.A."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Middleware de logging por request
# ---------------------------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Registra método, ruta, status y duración de cada petición."""
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    logger.info(
        "%s %s → %d (%.2fs)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    return response


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _agent(request: Request) -> AgentService:
    """Atajo para obtener el AgentService desde el state de la app."""
    return request.app.state.agent


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    """Chequeo de estado del backend."""
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):
    """Envía un mensaje al agente y devuelve su respuesta."""
    try:
        session_id, reply, tool_calls = await _agent(request).chat(
            message=req.message,
            session_id=req.session_id,
        )
    except AgentTimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc))
    except AgentConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except AgentError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        tool_calls=tool_calls,
    )


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str, request: Request):
    """Elimina una sesión (historial de conversación) en memoria."""
    await _agent(request).delete_session(session_id)
    return {"status": "ok"}
