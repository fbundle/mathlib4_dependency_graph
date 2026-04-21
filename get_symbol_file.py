import multiprocess as mp
import os
from typing import Any, Iterator

from filelock import FileLock
from pydantic import BaseModel
import pydantic_core


import ijson

from pydantic import BaseModel
from tqdm import tqdm

type JixiaLeanName = list[Any]

class JixiaSymbol(BaseModel):
    name: JixiaLeanName
    kind: str
    isProp: bool
    
    typeFallback: str | None
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[JixiaLeanName] | None 
    valueReferences: list[JixiaLeanName] | None

class Symbol(BaseModel):
    name: str
    kind: str
    isProp: bool
    
    typeFallback: str # always exist
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[str]
    valueReferences: list[str]









def get_dot_name(name: JixiaLeanName) -> str:
    return ".".join([str(part) for part in name])

def get_item(jtem: JixiaSymbol) -> Symbol:
    typeReferences, valueReferences = [], []
    if jtem.typeReferences is not None:
        typeReferences = [get_dot_name(name) for name in jtem.typeReferences]
    if jtem.valueReferences is not None:
        valueReferences = [get_dot_name(name) for name in jtem.valueReferences]
    
    if jtem.typeFallback is None:
        raise RuntimeError("jtem.typeFallback must be non-nil")

    return Symbol(
        name=get_dot_name(jtem.name),
        kind=jtem.kind,
        isProp=jtem.isProp,
        typeFallback=jtem.typeFallback,
        typeFull=jtem.typeFull,
        typeReadable=jtem.typeReadable,
        typeReferences=typeReferences,
        valueReferences=valueReferences,
    )

def get_item_key(item: Symbol) -> str:
    return "item." + item.name

def get_file_key(filename: str) -> str:
    return "file." + filename


def stream_json_list(filename: str) -> Iterator:
    with open(filename, "rb") as f:
        items = ijson.items(f, "item") # "item" is the prefix for elements in a root array
        for item in items:
            yield item

def process_graph(graph_dir: str, output_path: str, max_workers: int = 10):
    if os.path.exists(output_path):
        raise RuntimeError(f"{output_path} exists")

    def process_file(filename: str):
        lines: list[str] = []
        path = os.path.join(graph_dir, filename)
        for o in stream_json_list(path):
            try:
                i = get_item(JixiaSymbol.model_validate(o))
                line = i.model_dump_json()
                lines.append(line)
            except pydantic_core._pydantic_core.ValidationError:
                pass
        
        with FileLock(output_path + ".lock"):
            with open(output_path, "a") as f:
                for line in lines:
                    f.write(line + "\n")

    filename_list = [name for name in os.listdir(graph_dir) if name.endswith(".sym.json")]

    with mp.Pool(max_workers) as pool:  # type: ignore
        for _ in tqdm(pool.imap_unordered(process_file, filename_list), total=len(filename_list)):
            pass


if __name__ == "__main__":
    process_graph(
        graph_dir="output/mathlib4_dependency_graph/data_5e932f97dd25535344f80f9dd8da3aab83df0fe6",
        output_path="output/mathlib4_dependency_graph/symbol_5e932f97dd25535344f80f9dd8da3aab83df0fe6.jsonl",
        max_workers=10,
    )

