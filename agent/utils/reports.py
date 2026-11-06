def formatear_precio(valor: float | None) -> str:
    """
    Da formato argentino a un precio. Ejemplo: 4500.5 -> "$4.500,50", -83.8 -> "-$83,80". None -> "-".
    """
    if valor is None:
        return "-"
    signo = "-" if valor < 0 else ""
    return signo + "$" + f"{abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def armar_tabla_comparados(filas: list[dict]) -> str:
    """
    Arma la tabla Markdown de los productos que se pudieron comparar.
    """
    encabezado = (
        "| Producto | Presentacion | Ragnar | Supermercado | Precio regular | Precio promocional | Diferencia | Posicion |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )
    lineas = [
        f"| {f['producto']} {f['marca']} | {f['presentacion']} | {formatear_precio(f['precio_ragnar'])} "
        f"| {f['supermercado']} | {formatear_precio(f['precio_regular'])} | {formatear_precio(f['precio_promocional'])} "
        f"| {f['diferencia_porcentual']:+.2f}% ({formatear_precio(f['diferencia_absoluta'])}) "
        f"| {f['posicion']}{' (significativa)' if f['diferencia_significativa'] else ''} |"
        for f in filas
    ]
    return encabezado + "\n".join(lineas)


def armar_informe(filas: list[dict], fecha: str) -> tuple[str, dict]:
    """
    Arma el informe comparativo en Markdown a partir de los resultados registrados.
    Devuelve el texto del informe y un resumen con los conteos de cada caso.
    """
    comparados = [f for f in filas if f["estado"] == "comparado"]
    no_confiables = [f for f in filas if f["estado"] in ("coincidencia_no_confiable", "sin_stock")]
    no_encontrados = [f for f in filas if f["estado"] == "no_encontrado"]

    resumen = {
        "productos_analizados": len({f["producto_id"] for f in filas}),
        "competidores_consultados": sorted({f["supermercado"] for f in filas}),
        "comparados": len(comparados),
        "ragnar_mas_caro": sum(f["diferencia_porcentual"] > 0 for f in comparados),
        "ragnar_mas_barato": sum(f["diferencia_porcentual"] < 0 for f in comparados),
        "diferencias_significativas": sum(f["diferencia_significativa"] for f in comparados),
        "coincidencia_no_confiable": len(no_confiables),  # incluye productos sin stock
        "no_encontrados": len(no_encontrados),
    }

    partes = [
        "# Informe comparativo de precios - Ragnar S.A.",
        f"Fecha de generacion: {fecha}",
        "## Resumen",
        f"- Productos analizados: {resumen['productos_analizados']}",
        f"- Competidores consultados: {', '.join(resumen['competidores_consultados'])}",
        f"- Comparaciones confiables: {resumen['comparados']}",
        f"- Ragnar mas caro: {resumen['ragnar_mas_caro']} | Ragnar mas barato: {resumen['ragnar_mas_barato']}",
        f"- Diferencias significativas: {resumen['diferencias_significativas']}",
        f"- Sin comparacion confiable: {resumen['coincidencia_no_confiable']} | No encontrados: {resumen['no_encontrados']}",
    ]
    if comparados:
        partes += ["## Comparacion de precios", "La diferencia se calcula sobre el precio regular del competidor.", armar_tabla_comparados(comparados)]
    if no_confiables:
        partes += ["## Productos sin comparacion confiable"]
        partes += [f"- {f['producto']} {f['marca']} {f['presentacion']} en {f['supermercado']}: {' '.join(f['motivos'])}" for f in no_confiables]
    if no_encontrados:
        partes += ["## Productos no encontrados"]
        partes += [f"- {f['producto']} {f['marca']} {f['presentacion']} en {f['supermercado']}" for f in no_encontrados]
    fuentes = [f for f in filas if f.get("url")]
    if fuentes:
        partes += ["## Fuentes"]
        partes += [f"- {f['supermercado']}: {f['url']} (consultado el {f['fecha_consulta']})" for f in fuentes]

    return "\n\n".join(partes), resumen