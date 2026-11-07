"""Modelos de request y response para la API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Mensaje del usuario hacia el agente."""

    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ToolCall(BaseModel):
    """Información de una herramienta ejecutada por el agente durante el turno."""

    name: str
    args: dict


class ChatResponse(BaseModel):
    """Respuesta del agente al usuario."""

    session_id: str
    reply: str
    tool_calls: list[ToolCall]
