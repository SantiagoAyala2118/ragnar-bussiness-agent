from datetime import datetime

from google.adk.tools import ToolContext

from ..configuration import CARPETA_INFORMES
from ..utils import armar_informe, respuesta_error, respuesta_ok, respuesta_vacia


def generar_informe(tool_context: ToolContext) -> dict:
    """
    Herramienta para generar el informe comparativo de la investigacion actual.
    Arma el informe con los resultados registrados (precios, diferencias, promociones, fuentes y fechas),
    lo guarda como archivo Markdown y devuelve su contenido y un resumen.
    Utilizala cuando termines de registrar los resultados o cuando el usuario pida el informe.
    """
    # 1. Validar
    filas = tool_context.state.get("investigacion", [])
    if not filas:
        return respuesta_vacia("No hay resultados registrados. Usa registrar_resultado antes de generar el informe.")

    # 2. Armar el informe (los numeros salen de los resultados registrados, no del modelo)
    fecha = datetime.now()
    informe, resumen = armar_informe(filas, fecha.strftime("%Y-%m-%d %H:%M"))

    # 3. Guardar el archivo
    ruta = CARPETA_INFORMES / f"informe_{fecha.strftime('%Y%m%d_%H%M%S')}.md"
    try:
        CARPETA_INFORMES.mkdir(parents=True, exist_ok=True)
        ruta.write_text(informe, encoding="utf-8")
    except OSError as e:
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo guardar el informe: {e}")

    # 4. Recordar el ultimo informe en la sesion (lo usa guardar_investigacion)
    tool_context.state["ultimo_informe"] = {
        "texto": informe,
        "archivo": ruta.name,
        "fecha": fecha.strftime("%Y-%m-%d %H:%M"),
        "productos": sorted({f"{f['producto']} {f['marca']} {f['presentacion']}" for f in filas}),
        "categorias": sorted({f["categoria"] for f in filas}),
        "supermercados": resumen["competidores_consultados"],
    }
    return respuesta_ok(archivo=ruta.name, resumen=resumen, informe=informe)