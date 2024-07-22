import pickle

import os
from typing import Dict

from .vdb37 import VectorDatabase


class KV:
    """Represents a KV-paired vector database."""

    kv: Dict[str, VectorDatabase]

    def __init__(self):
        self.kv = {}

    def get(self, key: str) -> VectorDatabase:
        return self.kv[key]

    def update(self, key: str, value: VectorDatabase) -> None:
        self.kv[key] = value

    def save(self, base_path: str = "kv"):
        for key, db in self.kv.items():
            os.makedirs(f"{base_path}/{key}", exist_ok=True)
            with open(f"kv/{key}/db.pkl", "wb") as f:
                f.write(pickle.dumps(db))

    @staticmethod
    def load():
        kv = KV()
        for key in os.listdir("kv"):
            with open(f"kv/{key}/db.pkl", "rb") as f:
                kv.kv[key] = pickle.loads(f.read())
        return kv

    def __repr__(self) -> str:
        return f"<KV {self.kv}>"
