"""Tiny local retrieval layer used by the demo; replace with a vector store in production."""
from __future__ import annotations

import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"


def retrieve(service_route: str, query: str, top_k: int = 2) -> list[dict[str, str]]:
    """Rank approved knowledge snippets using transparent token overlap.

    This keeps the demo offline and auditable. The production plan replaces this
    with metadata-filtered embeddings plus an evaluation set.
    """
    documents = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    query_terms = set((query + " " + service_route).lower().split())
    ranked = []
    for doc in documents:
        tokens = set((doc["title"] + " " + doc["content"] + " " + doc["service"]).lower().split())
        score = len(query_terms & tokens) + (10 if doc["service"] == service_route else 0)
        ranked.append((score, doc))
    return [doc for _, doc in sorted(ranked, key=lambda item: item[0], reverse=True)[:top_k]]
