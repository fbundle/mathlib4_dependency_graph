from __future__ import annotations
from typing import Any, Iterator

import lmdb
from .symbol import Symbol

ENCODING = "utf-8"

class SymbolDB:
    def __init__(self, symbol_dbpath: str):
        self.symbol_dbpath = symbol_dbpath
        self.env = None
        self.txn = None
    
    def __enter__(self) -> SymbolDB:
        self.env = lmdb.open(self.symbol_dbpath, readonly=True)
        self.txn = self.env.begin().__enter__()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.txn.__exit__(exc_type, exc, tb)
        self.env.close()
        self.env = None

    def __getitem__(self, name: str, default: Any = None) -> Symbol:
        symbol: bytes | None = self.txn.get(name.encode(ENCODING))
        if symbol is None:
            return default
        return Symbol.model_validate_json(symbol)

    def __contains__(self, name: str) -> bool:
        symbol: bytes | None = self.txn.get(name.encode(ENCODING))
        return symbol is not None
    
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
            symbol = Symbol.model_validate_json(val_str)
            yield symbol
