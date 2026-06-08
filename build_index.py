"""Run the full ingestion → chunking → embedding pipeline."""

from chunk import build_chunks, save_chunks
from embed import build_vector_store
from ingest import load_documents


def main():
    print("Step 1: Loading and cleaning documents...")
    docs = load_documents()
    print(f"  Loaded {len(docs)} documents")

    print("\nStep 2: Chunking...")
    chunks = build_chunks(docs)
    save_chunks(chunks)
    print(f"  Created {len(chunks)} chunks")

    print("\nStep 3: Embedding and storing in ChromaDB...")
    build_vector_store(chunks)
    print("\nDone. Run 'python retrieve.py' to test retrieval or 'python app.py' to launch the UI.")


if __name__ == "__main__":
    main()
