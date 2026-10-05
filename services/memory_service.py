from __future__ import annotations

import json
import os
from typing import Any

from services.database_service import DatabaseService

try:  # Optional Hindsight SDK. Real integration is preferred when installed.
    import hindsight_memory  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    hindsight_memory = None


class MemoryService:
    def __init__(self, db_service: DatabaseService | None = None):
        self.db_service = db_service or DatabaseService()
        self.hindsight_client = self._build_hindsight_client()

    def _build_hindsight_client(self):
        if hindsight_memory is None:
            return None
        try:
            client_class = getattr(hindsight_memory, "HindsightClient", None) or getattr(hindsight_memory, "Client", None)
            if client_class is None:
                return None
            api_key = os.getenv("HINDSIGHT_API_KEY")
            base_url = os.getenv("HINDSIGHT_BASE_URL")
            kwargs = {}
            if api_key:
                kwargs["api_key"] = api_key
            if base_url:
                kwargs["base_url"] = base_url
            return client_class(**kwargs)
        except Exception:
            return None

    def store_memory(self, memory_type: str, summary: str, details: str = "", tags: str = "") -> dict:
        payload = {
            "memory_type": memory_type,
            "summary": summary,
            "details": details,
            "tags": tags,
            "source": "local_fallback",
        }
        try:
            if self.hindsight_client is not None:
                store_method = getattr(self.hindsight_client, "store_memory", None)
                if callable(store_method):
                    remote_response = store_method(memory_type=memory_type, summary=summary, details=details, tags=tags)
                    payload["source"] = "hindsight"
                    payload["remote_response"] = remote_response
                    return payload
        except Exception:
            pass

        self.db_service.save_memory(memory_type, summary, details, tags)
        return payload

    def search_memory(self, query: str, limit: int = 5) -> list[dict]:
        try:
            if self.hindsight_client is not None:
                search_method = getattr(self.hindsight_client, "search_memory", None)
                if callable(search_method):
                    results = search_method(query=query, limit=limit)
                    if results:
                        return [dict(item) if isinstance(item, dict) else {"content": str(item)} for item in results]
        except Exception:
            pass

        memories = self.db_service.list_memories()
        query_l = query.lower()
        matches = []
        for memory in memories:
            haystack = " ".join(
                [
                    str(memory.get("memory_type", "")),
                    str(memory.get("summary", "")),
                    str(memory.get("details", "")),
                    str(memory.get("tags", "")),
                ]
            ).lower()
            if query_l in haystack:
                matches.append(memory)
        return matches[:limit]

    def retrieve_relevant_memories(self, context_query: str, limit: int = 5) -> list[dict]:
        try:
            if self.hindsight_client is not None:
                retrieve_method = getattr(self.hindsight_client, "retrieve_relevant_memories", None)
                if callable(retrieve_method):
                    results = retrieve_method(context_query=context_query, limit=limit)
                    if results:
                        return [dict(item) if isinstance(item, dict) else {"content": str(item)} for item in results]
        except Exception:
            pass

        memories = self.db_service.list_memories()
        keywords = [word for word in context_query.lower().replace("?", "").split() if len(word) > 3]
        if not keywords:
            return memories[:limit]

        scored = []
        for memory in memories:
            haystack = " ".join(
                [
                    str(memory.get("memory_type", "")),
                    str(memory.get("summary", "")),
                    str(memory.get("details", "")),
                    str(memory.get("tags", "")),
                ]
            ).lower()
            score = sum(1 for keyword in keywords if keyword in haystack)
            if score > 0:
                scored.append((score, memory))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [memory for _, memory in scored[:limit]]

    def update_memory_from_feedback(self, feedback_text: str, rating: str = "") -> dict:
        summary = f"Farmer feedback: {feedback_text}"
        details = f"Rating: {rating}" if rating else "Rating not provided"
        self.store_memory("feedback", summary, details, "feedback,learning")
        return {"status": "stored", "summary": summary}
