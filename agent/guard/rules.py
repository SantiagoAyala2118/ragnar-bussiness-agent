import re

# Las reglas se aplican sobre el texto simplificado: minusculas, sin tildes ni guiones.
# Para evitar falsos positivos, casi todas exigen un VERBO cerca de un OBJETO protegido:
# "olvida tus reglas" se bloquea, pero "olvida la conversacion" o "un informe sobre las reglas" no.

DISTANCIA_MAXIMA = 4  # cantidad maxima de palabras entre el verbo y el objeto


def verbo_cerca_de_objeto(verbos: str, objetos: str) -> re.Pattern:
    """
    Arma un patron que detecta un verbo seguido de un objeto a pocas palabras de distancia.
    Ejemplo: verbos "olvid", objetos "reglas" -> detecta "olvida todas tus reglas".
    """
    return re.compile(rf"\b(?:{verbos})\w*(?:\W+\w+){{0,{DISTANCIA_MAXIMA}}}?\W+(?:{objetos})\b")


# --- Vocabulario ---
VERBOS_ANULAR = (
    r"olvid|ignor|omit|salt|desobedec|desconsider|anul|sobrescrib|reemplaz|evad|romp|bypass|override|forget|disregard"
    r"|deja de (?:seguir|respetar|cumplir)|no (?:sigas|respetes|cumplas)"
)
OBJETOS_INSTRUCCIONES = (
    r"instrucci\w*|regla\w*|programacion|restriccion\w*|prompt\w*|directiva\w*|politica\w*|configuracion|limitacion\w*|rol|roles"
    r"|instructions?|rules|guidelines"  # ataques en ingles
)

VERBOS_DESTRUIR = r"borr|elimin|destru|drop|vaci|formate|desinstal|deshabilit|desactiv|apag|resete|quit"
OBJETOS_SISTEMA = r"base de datos|bd|db|herramientas?|tools?|catalogo|codigo|servidor|archivos?|tablas?|historial|memoria|funciones|vector store|sistema"

VERBOS_REVELAR = r"mostr|revel|deci|dec|dame|pasame|repet|imprim|copi|escrib|filtr|cuales son"
OBJETOS_INTERNOS = r"tus instrucciones|tus reglas|tu prompt|system prompt|prompt del sistema|prompt inicial|tu programacion|tu configuracion|configuracion interna|codigo fuente"

# --- Reglas: (motivo, patron) ---
REGLAS_ENTRADA = [
    ("anular_instrucciones", verbo_cerca_de_objeto(VERBOS_ANULAR, OBJETOS_INSTRUCCIONES)),
    ("accion_destructiva", verbo_cerca_de_objeto(VERBOS_DESTRUIR, OBJETOS_SISTEMA)),
    ("extraer_instrucciones", verbo_cerca_de_objeto(VERBOS_REVELAR, OBJETOS_INTERNOS)),
    ("suplantar_rol", re.compile(
        r"\b(?:(?:a partir de )?ahora (?:sos|eres|seras|vas a ser)|fingi\w* ser|finge ser|simula\w* ser|hace de cuenta que sos"
        r"|modo (?:desarrollador|developer|dios|admin\w*|debug|libre|sin restricciones)|jailbreak"
        r"|sin (?:restricciones|filtros|censura)|you are now|act as|developer mode)\b"
    )),
    ("falsa_autoridad", re.compile(
        r"\b(?:soy (?:tu|el|la) (?:desarrollador|creador|programador|administrador|admin|duen[oa])"
        r"|orden del (?:sistema|administrador)|mensaje del sistema|system prompt)\b|\[(?:system|sistema)\]|<\s*/?\s*(?:system|sistema)\s*>"
    )),
    ("comandos", re.compile(r"rm -rf|drop table|delete from|truncate table|\bsudo\b|os\.system|subprocess|\beval\(|\bexec\(|<script|import os")),
    ("texto_codificado", re.compile(r"[a-z0-9+/]{60,}={0,2}")),  # bloques largos tipo base64
]

# Direcciones web escritas por el usuario (se validan contra la lista de supermercados permitidos)
PATRON_URL = re.compile(r"(?:https?://)?(?:www\.)?((?:[a-z0-9-]+\.)+(?:com|net|org|io|gov|edu|ar|info|xyz)(?:\.[a-z]{2})?)\b", re.IGNORECASE)

# --- Mensajes genericos de denegacion ---
MENSAJE_AYUDA = "Puedo ayudarte a consultar el catalogo de Ragnar, comparar precios con la competencia y generar informes."
MENSAJES_DENEGACION = {
    "anular_instrucciones": "No puedo ignorar ni modificar mis reglas de funcionamiento.",
    "accion_destructiva": "No puedo borrar, desactivar ni modificar datos, herramientas o sistemas.",
    "extraer_instrucciones": "No puedo compartir mi configuracion interna.",
    "suplantar_rol": "No puedo cambiar mi rol: soy el agente de precios de Ragnar S.A.",
    "falsa_autoridad": "No acepto instrucciones de sistema o de administrador dentro de una consulta.",
    "comandos": "No puedo ejecutar comandos ni codigo.",
    "texto_codificado": "No puedo procesar texto codificado.",
    "sitio_no_permitido": "Solo puedo consultar los sitios de supermercados autorizados.",
    "muy_largo": "El mensaje es demasiado largo. Escribi una consulta mas corta.",
}

# --- Salida ---
# Marcas de las instrucciones internas: si aparecen en una respuesta, se filtro la configuracion
MARCAS_INSTRUCCIONES = ["### rol", "### objetivo", "### flujo de una investigacion", "### seguridad", "instrucciones = "]
MENSAJE_DATOS_NO_VERIFICADOS = (
    "No muestro esa respuesta porque incluia valores que no provienen de las fuentes consultadas ({montos}). "
    "Pedime que repita la busqueda o que genere el informe."
)
MENSAJE_FILTRACION = "No puedo compartir mi configuracion interna. " + MENSAJE_AYUDA
MENSAJE_RECORTE = "\n\n(Respuesta recortada por ser muy extensa. Pedime el detalle de una parte puntual.)"