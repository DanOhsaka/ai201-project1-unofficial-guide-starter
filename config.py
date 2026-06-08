from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
CHUNKS_CACHE = Path(__file__).parent / "data" / "chunks.json"
TFIDF_VECTORIZER_PATH = Path(__file__).parent / "data" / "tfidf_vectorizer.joblib"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 5

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"

COLLECTION_NAME = "rsu_dining"
