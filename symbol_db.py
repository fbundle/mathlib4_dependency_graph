from __future__ import annotations
from typing import Iterator

import lmdb
from pydantic import BaseModel
from tqdm import tqdm

class Symbol(BaseModel):
    name: str
    kind: str
    isProp: bool
    
    typeFallback: str # always exist
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[str]
    valueReferences: list[str]

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

    def __getitem__(self, name: str) -> Symbol:
        symbol: bytes = self.txn.get(name.encode(ENCODING))
        return Symbol.model_validate_json(symbol)
    
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

def main():
    dbpath = "output/mathlib4_dependency_graph/symbol_5e932f97dd25535344f80f9dd8da3aab83df0fe6.db"

    typeFallback_always_exist = True
    typeFull_always_exist = True
    typeReadable_always_exist = True

    with SymbolDB(dbpath) as kv:
        for s in tqdm(kv.__iter__(), total=len(kv)):
            if typeFallback_always_exist:
                if s.typeFallback is None:
                    typeFallback_always_exist = False
            if typeFull_always_exist:
                if s.typeFull is None:
                    typeFull_always_exist = False
            if typeReadable_always_exist:
                if s.typeReadable is None:
                    typeReadable_always_exist = False
            
            if typeFallback_always_exist == False and typeFull_always_exist == False and typeReadable_always_exist == False:
                break
    
    print(typeFallback_always_exist, typeFull_always_exist, typeReadable_always_exist)

if __name__ == "__main__":
    main()
