"""
memory.py
A tiny persistent memory store (file-backed).
"""

import json
from typing import Any, Optional

class MemoryStore:
    def __init__(self, path: str = "memory_store.json"):
        self.path = path
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}

    def add(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key)

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def all(self) -> dict:
        return self.data

