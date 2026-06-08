"""End-to-end RAG: retrieve context and generate a grounded answer."""

import os

from dotenv import load_dotenv
from groq import Groq

from config import LLM_MODEL, TOP_K
from retrieve import retrieve

load_dotenv()

SYSTEM_PROMPT = """You are a helpful guide for Riverside State University campus dining.
Answer the student's question using ONLY the information in the provided document excerpts.
Do not use any outside knowledge, assumptions, or general facts about college dining.

Rules:
1. If the excerpts contain enough information, answer clearly and concisely.
2. If the excerpts do NOT contain enough information to answer, respond with exactly:
   "I don't have enough information on that."
3. Mention which source document(s) your answer draws from by filename.
4. Never invent wait times, prices, hours, or ratings not present in the excerpts."""


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Excerpt {i} | source: {chunk['source']} | chunk {chunk['chunk_index']}]\n{chunk['text']}"
        )
    return "\n\n".join(parts)


def ask(question: str, top_k: int = TOP_K) -> dict:
    """Retrieve chunks and generate a grounded answer with source list."""
    chunks = retrieve(question, top_k=top_k)
    context = format_context(chunks)
    sources = sorted({c["source"] for c in chunks})

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Document excerpts:\n\n{context}\n\nQuestion: {question}",
            },
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    q = "What are the wait times at North Dining Hall during lunch peak?"
    result = ask(q)
    print(f"Question: {q}\n")
    print(f"Answer: {result['answer']}\n")
    print(f"Sources: {result['sources']}")
