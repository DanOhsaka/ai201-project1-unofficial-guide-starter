"""Embed chunks and store in ChromaDB.

Primary path: sentence-transformers all-MiniLM-L6-v2.
Fallback path (offline-safe): sklearn TF-IDF vectors.
"""

import chromadb
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from chunk import build_chunks, load_chunks, save_chunks
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TFIDF_VECTORIZER_PATH


def get_embedding_model() -> SentenceTransformer | None:
    try:
        return SentenceTransformer(EMBEDDING_MODEL)
    except Exception:
        return None


def build_vector_store(chunks: list[dict] | None = None, reset: bool = True) -> chromadb.Collection:
    """Embed all chunks and persist to ChromaDB."""
    if chunks is None:
        chunks = build_chunks()
        save_chunks(chunks)

    texts = [c["text"] for c in chunks]
    model = get_embedding_model()
    using_fallback = model is None
    if model is not None:
        embeddings = model.encode(texts, show_progress_bar=True).tolist()
        embedding_method = EMBEDDING_MODEL
    else:
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            lowercase=True,
            sublinear_tf=True,
        )
        matrix = vectorizer.fit_transform(texts)
        embeddings = matrix.toarray().tolist()
        TFIDF_VECTORIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(vectorizer, TFIDF_VECTORIZER_PATH)
        embedding_method = "tfidf-fallback"

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine", "embedding_method": embedding_method},
    )

    ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.add(
            ids=ids[i : i + batch_size],
            documents=texts[i : i + batch_size],
            embeddings=embeddings[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )

    print(
        f"Stored {len(chunks)} chunks in ChromaDB collection '{COLLECTION_NAME}' "
        f"using {embedding_method}{' (offline fallback)' if using_fallback else ''}"
    )
    return collection


def get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(COLLECTION_NAME)


if __name__ == "__main__":
    chunks = load_chunks() if (CHROMA_DIR.parent / "data" / "chunks.json").exists() else None
    if chunks is None:
        chunks = build_chunks()
        save_chunks(chunks)
    build_vector_store(chunks)
