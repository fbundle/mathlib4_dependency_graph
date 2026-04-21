from __future__ import annotations
from typing import Any, Iterator

import lmdb
from .symbol import Symbol

ENCODING = "utf-8"

class SymbolDB:
    def __init__(self, sym_dbpath: str):
        self.sym_dbpath = sym_dbpath
        self.env = None
        self.txn = None
    
    def __enter__(self) -> SymbolDB:
        self.env = lmdb.open(self.sym_dbpath, readonly=True)
        self.txn = self.env.begin().__enter__()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.txn.__exit__(exc_type, exc, tb)
        self.env.close()
        self.env = None

    def __getitem__(self, name: str, default: Any = None) -> Symbol:
        sym: bytes | None = self.txn.get(name.encode(ENCODING))
        if sym is None:
            return default
        return Symbol.model_validate_json(sym)

    def __contains__(self, name: str) -> bool:
        sym: bytes | None = self.txn.get(name.encode(ENCODING))
        return sym is not None
    
    def __len__(self) -> int:
        return self.env.stat()["entries"]

    def __iter__(self, prefix: str = "") -> Iterator[Symbol]:
        cursor = self.txn.cursor()
        cursor.set_range(prefix.encode(ENCODING))
        for key, val in cursor:
            key_str = key.decode(ENCODING)
            if not key_str.startswith(prefix):
                break
            val_str = val.decode(ENCODING)
            sym = Symbol.model_validate_json(val_str)
            yield sym
