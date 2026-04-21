from __future__ import annotations

import lmdb


class SymbolDB:
    def __init__(self, symbol_dbpath: str):
        self.symbol_dbpath = symbol_dbpath
        self.env = None
    
    def __enter__(self) -> SymbolDB:
        self.env = lmdb.open(self.symbol_dbpath, readonly=True)
    
    def __exit__(self, exc_type, exc, tb):
        self.env.close()
        self.env = None
