"""
ARCH-COUNCIL Knowledge Base Ingestion Script
Run this ONCE before starting the server to populate the vector database.

Usage:
    uv run python -m knowledge.ingest

What it does:
1. Loads all SEED_DOCUMENTS (TOGAF, AI patterns, governance frameworks)
2. Chunks and embeds each document
3. Stores in ChromaDB (data/chroma/)
"""
import sys
import os
import uuid
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge.sources import SEED_DOCUMENTS
from backend.rag import get_collection

CHUNK_SIZE = 800        # tokens approx (chars / 4)
CHUNK_OVERLAP = 100     # chars overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        # Try to break at a paragraph or sentence boundary
        if end < len(text):
            for delimiter in ["\n\n", "\n", ". ", " "]:
                break_point = text.rfind(delimiter, start + chunk_size // 2, end)
                if break_point != -1:
                    end = break_point + len(delimiter)
                    break
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start >= len(text):
            break

    return chunks


def ingest_seed_documents():
    """Ingest all seed documents into ChromaDB."""
    collection = get_collection()

    # Check if already populated
    existing = collection.count()
    if existing > 0:
        print(f"Knowledge base already contains {existing} chunks.")
        response = input("Re-ingest? This will delete and rebuild. [y/N]: ").strip().lower()
        if response != "y":
            print("Skipping ingest.")
            return

        # Clear and rebuild
        import chromadb
        from backend.rag import CHROMA_PATH, COLLECTION_NAME
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        client.delete_collection(COLLECTION_NAME)
        print("Cleared existing collection.")

    collection = get_collection()  # recreate after potential deletion

    print(f"\nIngesting {len(SEED_DOCUMENTS)} seed documents...")
    total_chunks = 0

    for doc in SEED_DOCUMENTS:
        content = doc["content"].strip()
        chunks = chunk_text(content)
        doc_chunks = []
        doc_ids = []
        doc_metas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}_chunk_{i}"
            doc_ids.append(chunk_id)
            doc_chunks.append(chunk)
            doc_metas.append({
                "source": doc["source"],
                "category": doc["category"],
                "doc_id": doc["id"],
                "chunk_index": i,
                "total_chunks": len(chunks),
            })

        collection.add(
            ids=doc_ids,
            documents=doc_chunks,
            metadatas=doc_metas,
        )

        total_chunks += len(chunks)
        print(f"  ✓ {doc['source']} → {len(chunks)} chunk(s)")

    print(f"\n✅ Knowledge base populated: {total_chunks} total chunks from {len(SEED_DOCUMENTS)} documents.")
    print(f"   Stored in: {Path('data/chroma').resolve()}")


def ingest_custom_document(file_path: str, category: str, source: str):
    """Ingest a custom document file (txt, md) into the knowledge base."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return

    content = path.read_text(encoding="utf-8")
    chunks = chunk_text(content)
    collection = get_collection()

    doc_id = path.stem.replace(" ", "_").lower()
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metas = [{"source": source, "category": category, "doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, metadatas=metas)
    print(f"✓ Ingested '{path.name}' → {len(chunks)} chunks (category: {category})")


def print_stats():
    """Print current knowledge base statistics."""
    from backend.rag import get_knowledge_base_stats
    stats = get_knowledge_base_stats()
    print("\n📚 Knowledge Base Statistics:")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Embed model:  {stats['embed_model']}")
    print(f"   Categories:")
    for cat, count in stats["categories"].items():
        print(f"     {cat}: {count} chunks")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ARCH-COUNCIL Knowledge Base Ingestion")
    parser.add_argument("--stats", action="store_true", help="Print knowledge base statistics")
    parser.add_argument("--add", type=str, help="Path to a custom document to add")
    parser.add_argument("--category", type=str, default="Custom", help="Category for custom document")
    parser.add_argument("--source", type=str, default="Custom Document", help="Source label for custom document")
    args = parser.parse_args()

    if args.stats:
        print_stats()
    elif args.add:
        ingest_custom_document(args.add, args.category, args.source)
        print_stats()
    else:
        ingest_seed_documents()
        print_stats()
