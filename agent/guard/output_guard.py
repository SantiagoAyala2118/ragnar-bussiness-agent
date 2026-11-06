from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.genai import types

from ..configuration import DIFERENCIA_SIGNIFICATIVA, MAX_CARACTERES_RESPUESTA
from ..utils import esta_verificado, extraer_montos, recolectar_numeros
from .rules import MARCAS_INSTRUCCIONES, MENSAJE_DATOS_NO_VERIFICADOS, MENSAJE_FILTRACION, MENSAJE_RECORTE

VALORES_FIJOS = {0.0, 100.0, DIFERENCIA_SIGNIFICATIVA}  # valores que el agente puede mencionar siempre


def registrar_datos_herramienta(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
) -> dict | None:
    """
    Callback que ADK ejecuta DESPUES de cada herramienta.
    Guarda todos los numeros que devolvio la herramienta: son los unicos valores que la respuesta puede contener.
    No modifica la respuesta de la herramienta (devuelve None).
    """
    numeros_validos = set(tool_context.state.get("guard_numeros", []))
    tool_context.state["guard_numeros"] = sorted(numeros_validos | recolectar_numeros(tool_response))
    if tool.name == "generar_informe" and tool_response.get("status") == "ok":
        tool_context.state["guard_informe_turno"] = tool_context.invocation_id  # hay un informe confiable en este turno
    return None


def reemplazar_texto(llm_response: LlmResponse, texto: str) -> LlmResponse:
    """
    Devuelve una copia de la respuesta del modelo con otro texto.
    """
    contenido = types.Content(role="model", parts=[types.Part(text=texto)])
    return llm_response.model_copy(update={"content": contenido})


def revisar_respuesta(callback_context: CallbackContext, llm_response: LlmResponse) -> LlmResponse | None:
    """
    Callback que ADK ejecuta DESPUES de cada respuesta del modelo, antes de mostrarla al usuario.
    1. Bloquea respuestas que filtran las instrucciones internas.
    2. Verifica que cada precio ($) y porcentaje (%) provenga de una herramienta o del usuario.
       Si no, muestra el informe generado en este turno o un mensaje generico.
    3. Recorta respuestas demasiado extensas.
    Devuelve None si la respuesta esta bien (ADK la muestra sin cambios).
    """
    partes = llm_response.content.parts if llm_response.content and llm_response.content.parts else []
    if llm_response.partial or any(parte.function_call for parte in partes):
        return None  # todavia no es la respuesta final: el modelo esta llamando herramientas
    texto = "".join(parte.text for parte in partes if parte.text)
    if not texto:
        return None

    # 1. Filtracion de instrucciones
    if any(marca in texto.lower() for marca in MARCAS_INSTRUCCIONES):
        print("[GUARD] Salida bloqueada (filtracion de instrucciones)")
        return reemplazar_texto(llm_response, MENSAJE_FILTRACION)

    # 2. Precios y porcentajes sin fuente
    permitidos = set(callback_context.state.get("guard_numeros", [])) | VALORES_FIJOS
    no_verificados = [monto for monto in extraer_montos(texto) if not esta_verificado(monto, permitidos)]
    if no_verificados:
        print(f"[GUARD] Salida corregida (valores sin fuente: {no_verificados})")
        informe = callback_context.state.get("ultimo_informe")
        if informe and callback_context.state.get("guard_informe_turno") == callback_context.invocation_id:
            return reemplazar_texto(llm_response, informe["texto"])
        return reemplazar_texto(llm_response, MENSAJE_DATOS_NO_VERIFICADOS.format(montos=", ".join(no_verificados)))

    # 3. Respuestas demasiado extensas
    if len(texto) > MAX_CARACTERES_RESPUESTA:
        print("[GUARD] Salida recortada (demasiado extensa)")
        corte = texto.rfind("\n", 0, MAX_CARACTERES_RESPUESTA)
        return reemplazar_texto(llm_response, texto[: corte if corte > 0 else MAX_CARACTERES_RESPUESTA] + MENSAJE_RECORTE)

    return None