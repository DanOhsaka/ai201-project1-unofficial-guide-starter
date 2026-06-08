"""Load and clean documents from the documents/ directory."""

import html
import re
from pathlib import Path

from config import DOCUMENTS_DIR


def clean_text(text: str) -> str:
    """Remove HTML artifacts, normalize whitespace, and strip boilerplate."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    """Load all .txt files and return list of {source, text} dicts."""
    documents = []
    for path in sorted(documents_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw)
        if cleaned:
            documents.append({"source": path.name, "text": cleaned})
    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    if docs:
        print(f"\n--- Sample cleaned document: {docs[0]['source']} ---")
        print(docs[0]["text"][:600])
        print("...")
