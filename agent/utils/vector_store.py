from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..configuration import (
    CARPETA_VECTOR_STORE,
    COLECCION_INVESTIGACIONES,
    MODELO_EMBEDDINGS,
    SOLAPAMIENTO_FRAGMENTO,
    TAMANO_FRAGMENTO,
    URL_OLLAMA,
)


@lru_cache(maxsize=1)
def obtener_base_vectorial() -> Chroma:
    """
    Crea (una sola vez) la conexion a la base de datos vectorial Chroma donde se guardan las investigaciones.
    Los embeddings se generan con nomic-embed-text a traves de Ollama.
    """
    embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS, base_url=URL_OLLAMA)
    return Chroma(
        embedding_function=embeddings,
        collection_name=COLECCION_INVESTIGACIONES,
        persist_directory=str(CARPETA_VECTOR_STORE),
    )


def dividir_en_fragmentos(texto: str, metadatos: dict) -> list[Document]:
    """
    Convierte un texto en un Document y lo divide en fragmentos (chunks) con solapamiento.
    Cada fragmento conserva los metadatos (fecha, productos, supermercados, archivo).
    """
    divisor = RecursiveCharacterTextSplitter(chunk_size=TAMANO_FRAGMENTO, chunk_overlap=SOLAPAMIENTO_FRAGMENTO)
    return divisor.split_documents([Document(page_content=texto, metadata=metadatos)])