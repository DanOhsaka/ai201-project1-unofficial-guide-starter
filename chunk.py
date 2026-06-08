"""Split cleaned documents into overlapping chunks."""

import json
from pathlib import Path

from config import CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_CACHE
from ingest import load_documents


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks of fixed character length."""
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start += chunk_size - overlap

    return chunks


def build_chunks(documents: list[dict] | None = None) -> list[dict]:
    """Chunk all documents and attach source metadata."""
    if documents is None:
        documents = load_documents()

    all_chunks = []
    for doc in documents:
        pieces = chunk_text(doc["text"])
        for i, piece in enumerate(pieces):
            all_chunks.append(
                {
                    "text": f"Source document: {doc['source']}\n{piece}",
                    "source": doc["source"],
                    "chunk_index": i,
                }
            )
    return all_chunks


def save_chunks(chunks: list[dict], path: Path = CHUNKS_CACHE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")


def load_chunks(path: Path = CHUNKS_CACHE) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    chunks = build_chunks()
    save_chunks(chunks)
    print(f"Total chunks: {len(chunks)}")
    print("\n--- 5 representative chunks ---")
    indices = [0, len(chunks) // 4, len(chunks) // 2, 3 * len(chunks) // 4, len(chunks) - 1]
    for idx in indices:
        c = chunks[idx]
        print(f"\n[{idx}] source={c['source']} index={c['chunk_index']}")
        print(c["text"])
        print("-" * 60)
