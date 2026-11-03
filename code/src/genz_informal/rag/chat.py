"""Antarmuka tanya-jawab RAG (retrieval + rangkuman).

Secara default hanya menampilkan dokumen paling relevan (extractive). Bila
variabel lingkungan LLM_BACKEND diset (mis. ollama), jawaban dapat dirangkai.
"""

from __future__ import annotations

from .index import RagIndex, build, search

_SYSTEM = (
    "Anda asisten statistik resmi. Jawab HANYA berdasarkan konteks yang diberikan. "
    "Sertakan sumber (var_id/tahun) bila ada. Jika tidak ada di konteks, katakan tidak tahu."
)


def answer(question: str, index: RagIndex | None = None, k: int = 4) -> dict:
    index = index or build()
    hits = search(index, question, k=k)
    context = "\n".join(f"- {h['text']}" for h in hits)
    # Rangkuman ekstraktif (tanpa LLM): ambil kalimat paling relevan
    return {
        "question": question,
        "context": context,
        "sources": [h for h in hits],
        "answer": hits[0]["text"] if hits else "Tidak ada informasi relevan dalam indeks.",
    }
