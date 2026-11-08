"""
Servicio que envuelve el agente de Google ADK.

Encapsula Runner + InMemorySessionService con:
- Timeout configurable por turno del agente.
- Manejo diferenciado de errores (conexión, timeout, genéricos).
- Logging estructurado de cada interacción.
"""

import asyncio
import logging
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent.agent import root_agent

from .config import settings
from .schemas import ToolCall

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Excepciones del servicio
# ---------------------------------------------------------------------------

class AgentError(Exception):
    """Error genérico del agente."""


class AgentTimeoutError(AgentError):
    """El agente excedió el tiempo máximo permitido."""


class AgentConnectionError(AgentError):
    """No se pudo conectar con el servicio del modelo (Ollama)."""


# ---------------------------------------------------------------------------
# Servicio
# ---------------------------------------------------------------------------

class AgentService:
    """Envuelve el Runner de ADK con manejo de errores, timeouts y logging."""

    def __init__(self) -> None:
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name=settings.app_name,
            agent=root_agent,
            session_service=self.session_service,
            auto_create_session=True,
        )
        logger.info(
            "AgentService inicializado (app=%s, timeout=%ds)",
            settings.app_name,
            settings.agent_timeout,
        )

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    async def chat(
        self, message: str, session_id: str | None = None
    ) -> tuple[str, str, list[ToolCall]]:
        """
        Envía un mensaje al agente y devuelve ``(session_id, reply, tool_calls)``.

        Raises:
            AgentConnectionError: Si no se puede conectar con Ollama / el modelo.
            AgentTimeoutError: Si el agente excede el tiempo máximo.
            AgentError: Para cualquier otro error del agente o sus herramientas.
        """
        session_id = session_id or str(uuid.uuid4())
        content = types.Content(
            role="user", parts=[types.Part(text=message)]
        )

        reply_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        logger.info(
            "Chat [%s] ← %r (%d chars)",
            session_id[:8],
            message[:80],
            len(message),
        )

        try:
            await asyncio.wait_for(
                self._run_agent(session_id, content, reply_parts, tool_calls),
                timeout=settings.agent_timeout,
            )
        except asyncio.TimeoutError:
            logger.error(
                "Chat [%s]: timeout (%ds)", session_id[:8], settings.agent_timeout
            )
            raise AgentTimeoutError(
                f"El agente no respondió en {settings.agent_timeout} segundos. "
                "Intentá con una consulta más simple o volvé a intentar."
            )
        except ConnectionRefusedError:
            logger.error("Chat [%s]: Ollama no disponible", session_id[:8])
            raise AgentConnectionError(
                "No se pudo conectar con Ollama. "
                "Verificá que esté corriendo (ollama serve) y que el modelo esté disponible."
            )
        # El detalle tecnico queda solo en el log: el usuario recibe un mensaje fijo
        except (ConnectionError, OSError) as exc:
            logger.exception("Chat [%s]: error de conexión", session_id[:8])
            raise AgentConnectionError(
                "No se pudo conectar con el servicio del modelo. Volvé a intentar en unos segundos."
            ) from exc
        except Exception as exc:
            logger.exception("Chat [%s]: error inesperado", session_id[:8])
            raise AgentError(
                "Ocurrió un error inesperado al procesar la consulta. Volvé a intentar."
            ) from exc

        # Linea en blanco entre bloques para que el markdown no se mezcle
        reply = "\n\n".join(reply_parts).strip() or "(El agente no devolvió respuesta)"

        logger.info(
            "Chat [%s] → %d chars, %d tool(s)",
            session_id[:8],
            len(reply),
            len(tool_calls),
        )

        return session_id, reply, tool_calls

    async def _run_agent(
        self,
        session_id: str,
        content: types.Content,
        reply_parts: list[str],
        tool_calls: list[ToolCall],
    ) -> None:
        """Consume el async generator del runner y recolecta partes y tool calls."""
        async for event in self.runner.run_async(
            user_id=settings.user_id,
            session_id=session_id,
            new_message=content,
        ):
            for call in event.get_function_calls() or []:
                tool_calls.append(
                    ToolCall(name=call.name, args=call.args or {})
                )
                logger.debug("  Tool: %s(%s)", call.name, call.args)

            # Se junta el texto de TODAS las respuestas del agente, no solo la final:
            # el modelo suele escribir el informe y en el mismo paso llamar a otra
            # herramienta (ej: guardar_investigacion), y ese texto quedaba afuera.
            if event.author == "user" or event.partial or not event.content:
                continue
            texto = "".join(
                p.text for p in (event.content.parts or []) if p.text and not p.thought
            ).strip()
            if texto:
                reply_parts.append(texto)

    # ------------------------------------------------------------------
    # Sesiones
    # ------------------------------------------------------------------

    async def delete_session(self, session_id: str) -> bool:
        """
        Elimina una sesión del almacén en memoria.

        Devuelve ``True`` si se eliminó, ``False`` si no existía o hubo un
        error menor.  Nunca lanza excepción por sesión inexistente.
        """
        try:
            await self.session_service.delete_session(
                app_name=settings.app_name,
                user_id=settings.user_id,
                session_id=session_id,
            )
            logger.info("Sesión eliminada: %s", session_id[:8])
            return True
        except Exception as exc:
            # InMemorySessionService puede lanzar KeyError, ValueError, etc.
            # si la sesión ya no existe.  Lo tratamos como idempotente.
            logger.warning(
                "No se pudo eliminar sesión %s: %s", session_id[:8], exc
            )
            return False
