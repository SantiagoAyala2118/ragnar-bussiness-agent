from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from ..configuration import MAX_CARACTERES_ENTRADA, SUPERMERCADOS
from ..utils import recolectar_numeros, simplificar_texto
from .rules import MENSAJE_AYUDA, MENSAJES_DENEGACION, PATRON_URL, REGLAS_ENTRADA


def buscar_sitio_no_permitido(texto: str) -> str | None:
    """
    Devuelve el primer dominio escrito por el usuario que no pertenece a un supermercado permitido.
    Ejemplo: "busca en www.ejemplo.com" -> "ejemplo.com". None si no hay dominios o todos son validos.
    """
    dominios_validos = [dominio.removeprefix("www.") for dominio in SUPERMERCADOS.values()]
    for dominio in PATRON_URL.findall(texto.lower()):
        if not any(dominio == valido or dominio.endswith("." + valido) for valido in dominios_validos):
            return dominio
    return None


def analizar_entrada(texto: str) -> str | None:
    """
    Analiza el mensaje del usuario y devuelve el motivo por el que se bloquea, o None si es seguro.
    Motivos posibles: las claves de MENSAJES_DENEGACION (ej: "anular_instrucciones").
    """
    if len(texto) > MAX_CARACTERES_ENTRADA:
        return "muy_largo"
    if buscar_sitio_no_permitido(texto):
        return "sitio_no_permitido"
    texto_simple = simplificar_texto(texto)
    for motivo, patron in REGLAS_ENTRADA:
        if patron.search(texto_simple):
            return motivo
    return None


def filtrar_entrada(callback_context: CallbackContext) -> types.Content | None:
    """
    Callback que ADK ejecuta ANTES de que el agente (y el modelo) reciba el mensaje.
    Si detecta un intento de prompt injection, corta la peticion y responde con un mensaje generico.
    Si el mensaje es seguro, guarda sus numeros (ej: un precio que da el usuario) como valores validos para la salida.
    """
    contenido = callback_context.user_content
    texto = " ".join(parte.text for parte in (contenido.parts if contenido else []) if parte.text)

    motivo = analizar_entrada(texto)
    if motivo:
        print(f"[GUARD] Entrada bloqueada ({motivo}): {texto[:80]!r}")
        mensaje = f"{MENSAJES_DENEGACION[motivo]} {MENSAJE_AYUDA}"
        return types.Content(role="model", parts=[types.Part(text=mensaje)])

    numeros_validos = set(callback_context.state.get("guard_numeros", []))
    callback_context.state["guard_numeros"] = sorted(numeros_validos | recolectar_numeros(texto))
    return None