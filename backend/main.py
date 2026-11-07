"""API simple que expone el agente de Ragnar para el frontend.

Ejecutar desde la raiz del proyecto:
    uvicorn backend.main:app --reload --port 8000
"""

import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

from agent.agent import root_agent

APP_NAME = "ragnar"
USER_ID = "empleado"

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True,
)

app = FastAPI(title="Ragnar - Agente de precios")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ToolCall(BaseModel):
    name: str
    args: dict


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    tool_calls: list[ToolCall]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    mensaje = types.Content(role="user", parts=[types.Part(text=req.message)])

    reply_parts: list[str] = []
    tool_calls: list[ToolCall] = []
    try:
        async for event in runner.run_async(
            user_id=USER_ID, session_id=session_id, new_message=mensaje
        ):
            for call in event.get_function_calls() or []:
                tool_calls.append(ToolCall(name=call.name, args=call.args or {}))
            if event.is_final_response() and event.content and event.content.parts:
                reply_parts.extend(p.text for p in event.content.parts if p.text)
    except Exception as exc:  # el modelo o una herramienta fallaron
        raise HTTPException(status_code=502, detail=f"Error del agente: {exc}") from exc

    return ChatResponse(
        session_id=session_id,
        reply="\n".join(reply_parts).strip() or "(El agente no devolvio respuesta)",
        tool_calls=tool_calls,
    )


@app.delete("/api/sessions/{session_id}")
async def borrar_sesion(session_id: str):
    await session_service.delete_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    return {"status": "ok"}
