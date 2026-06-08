"""Retrieve relevant chunks for a query."""

import joblib
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL, TFIDF_VECTORIZER_PATH, TOP_K
from embed import get_collection


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return top-k chunks with text, source, distance, and chunk_index."""
    collection = get_collection()
    embedding_method = (collection.metadata or {}).get("embedding_method", EMBEDDING_MODEL)
    if embedding_method == "tfidf-fallback":
        vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
        query_embedding = vectorizer.transform([query]).toarray().tolist()
    else:
        model = SentenceTransformer(EMBEDDING_MODEL)
        query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "chunk_index": results["metadatas"][0][i]["chunk_index"],
                "distance": results["distances"][0][i],
            }
        )
    return chunks


if __name__ == "__main__":
    test_queries = [
        "What are the wait times at North Dining Hall during lunch peak?",
        "Which dining hall is best for vegan students?",
        "What late-night food options are available on campus after 9 PM?",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        print("=" * 70)
        for rank, chunk in enumerate(retrieve(q), 1):
            print(f"  #{rank} distance={chunk['distance']:.4f} source={chunk['source']}")
            print(f"     {chunk['text'][:200]}...")
