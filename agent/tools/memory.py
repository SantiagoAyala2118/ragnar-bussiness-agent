from google.adk.tools import ToolContext

from ..utils import dividir_en_fragmentos, obtener_base_vectorial, respuesta_error, respuesta_ok, respuesta_vacia


def guardar_investigacion(conclusiones: str, tool_context: ToolContext) -> dict:
    """
    Herramienta para guardar el ultimo informe generado y sus conclusiones en el historial de investigaciones.
    El historial es una base de datos vectorial (RAG) que permite consultar investigaciones anteriores.
    Utilizala despues de generar_informe, con las conclusiones que le diste al usuario.
    Args:
        conclusiones: str -> Conclusiones principales del informe, en pocas oraciones.
    """
    # 1. Validar
    informe = tool_context.state.get("ultimo_informe")
    if not informe:
        return respuesta_error("No hay un informe generado. Usa generar_informe primero.")
    if len(conclusiones.strip()) < 10:
        return respuesta_error("Escribe conclusiones de al menos una oracion.")

    # 2. Armar el documento con sus metadatos (Chroma solo acepta textos, numeros o booleanos)
    texto = f"{informe['texto']}\n\n## Conclusiones\n\n{conclusiones.strip()}"
    metadatos = {
        "fecha": informe["fecha"],
        "archivo": informe["archivo"],
        "productos": ", ".join(informe["productos"]),
        "categorias": ", ".join(informe["categorias"]),
        "supermercados": ", ".join(informe["supermercados"]),
    }

    # 3. Dividir en fragmentos y guardar los embeddings
    try:
        fragmentos = dividir_en_fragmentos(texto, metadatos)
        obtener_base_vectorial().add_documents(fragmentos)
    except Exception as e:
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo guardar la investigacion: {e}")

    return respuesta_ok(mensaje="Investigacion guardada en el historial.", fragmentos=len(fragmentos), fecha=informe["fecha"])


def consultar_investigaciones(consulta: str, cantidad: int = 4) -> dict:
    """
    Herramienta para buscar en el historial de investigaciones anteriores (RAG).
    Devuelve los fragmentos de informes pasados mas parecidos a la consulta, con su fecha y archivo.
    Utilizala cuando el usuario pregunte por investigaciones, informes o conclusiones anteriores.
    Args:
        consulta: str -> Que buscar (ej: "conclusiones sobre bebidas").
        cantidad: int -> Cantidad de fragmentos a recuperar (entre 1 y 10).
    """
    # 1. Validar
    if len(consulta.strip()) < 3:
        return respuesta_error("La consulta debe tener al menos 3 caracteres.")
    if not 1 <= cantidad <= 10:
        return respuesta_error("cantidad debe estar entre 1 y 10.")

    # 2. Buscar por similitud (puntaje mas cercano a 0 = mas parecido)
    try:
        resultados = obtener_base_vectorial().similarity_search_with_score(consulta.strip(), k=cantidad)
    except Exception as e:
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo consultar el historial: {e}")

    # 3. Responder
    if not resultados:
        return respuesta_vacia("El historial de investigaciones esta vacio.")
    fragmentos = [
        {"texto": documento.page_content, **documento.metadata, "puntaje": round(puntaje, 4)}
        for documento, puntaje in resultados
    ]
    return respuesta_ok(cantidad=len(fragmentos), fragmentos=fragmentos)