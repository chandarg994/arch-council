"""
ARCH-COUNCIL RAG (Retrieval-Augmented Generation) Module
Manages the ChromaDB knowledge base and semantic retrieval.
Headroom compression applied to retrieved chunks before LLM injection.
"""
import logging
from pathlib import Path
from typing import Dict
import chromadb
from chromadb.utils import embedding_functions

try:
    from headroom import compress as _hr_compress
    _HEADROOM_AVAILABLE = True
except ImportError:
    _HEADROOM_AVAILABLE = False
    logging.getLogger(__name__).warning("headroom-ai not installed. pip install headroom-ai")

def _compress(text: str) -> str:
    if not _HEADROOM_AVAILABLE or not text or len(text) < 200:
        return text
    try:
        return _hr_compress(text)
    except Exception:
        return text

BASE_DIR = Path(__file__).parent.parent
CHROMA_PATH = str(BASE_DIR / "data" / "chroma")
COLLECTION_NAME = "arch_knowledge"
EMBED_MODEL = "all-MiniLM-L6-v2"

def _get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = _get_embedding_function()
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef, metadata={"hnsw:space": "cosine"})

def retrieve_context(query: str, n_results: int = 8, min_relevance: float = 0.25) -> str:
    collection = get_collection()
    if collection.count() == 0:
        return "[Knowledge base is empty. Run `python -m knowledge.ingest` to populate it.]"
    results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()), include=["documents", "metadatas", "distances"])
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    if not docs:
        return "[No relevant context found in knowledge base.]"
    parts = []
    for doc, meta, dist in zip(docs, metas, dists):
        if (1.0 - dist) >= min_relevance:
            parts.append(f"[{meta.get('category','General')} | {meta.get('source','Unknown')}]\n{_compress(doc)}")
    return "\n\n---\n\n".join(parts) if parts else "[No sufficiently relevant context found.]"

def retrieve_by_category(query: str, category: str, n_results: int = 5) -> str:
    collection = get_collection()
    if collection.count() == 0:
        return "[Knowledge base empty.]"
    results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()), where={"category": category}, include=["documents", "metadatas"])
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    if not docs:
        return f"[No {category} context found.]"
    return "\n\n---\n\n".join(f"[{m.get('source','Unknown')}]\n{_compress(d)}" for d, m in zip(docs, metas))

def get_knowledge_base_stats() -> Dict:
    collection = get_collection()
    count = collection.count()
    categories: Dict[str, int] = {}
    if count > 0:
        for meta in collection.get(include=["metadatas"])["metadatas"]:
            cat = meta.get("category", "Unknown")
            categories[cat] = categories.get(cat, 0) + 1
    return {"total_chunks": count, "categories": categories, "embed_model": EMBED_MODEL, "chroma_path": CHROMA_PATH, "headroom_compression": _HEADROOM_AVAILABLE}
