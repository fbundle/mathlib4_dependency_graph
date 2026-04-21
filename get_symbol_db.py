from pydantic import BaseModel

import lmdb
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

MAP_SIZE = 100 * 1024 * 1024 * 1024 # 100 GB

def process_symbol_file(symbol_path: str):
    assert symbol_path.endswith(".jsonl")

    symbol_dbpath = symbol_path.rstrip(".jsonl") + ".db"
    with lmdb.open(symbol_dbpath, map_size=MAP_SIZE) as env:
        with env.begin(write=True) as txn:
            for line in tqdm(open(symbol_path), desc="loading ..."):
                line = line.strip()
                symbol = Symbol.model_validate_json(line)
                txn.put(symbol.name.encode("utf-8"), line.encode("utf-8"))

if __name__ == "__main__":
    symbol_path = "output/mathlib4_dependency_graph/symbol_5e932f97dd25535344f80f9dd8da3aab83df0fe6.jsonl"
    process_symbol_file(symbol_path)

