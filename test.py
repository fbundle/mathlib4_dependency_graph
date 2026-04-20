import json
import os
from typing import Any, Iterator



# import lmdb
from pydantic import BaseModel
import pydantic_core


import ijson

from pydantic import BaseModel
from tqdm import tqdm

type JixiaLeanName = list[Any]

class JixiaItem(BaseModel):
    name: JixiaLeanName
    kind: str
    isProp: bool
    
    typeFallback: str | None
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[JixiaLeanName] | None 
    valueReferences: list[JixiaLeanName] | None

class Item(BaseModel):
    name: str
    kind: str
    isProp: bool
    
    typeFallback: str | None
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[str]
    valueReferences: list[str]



graph_dir = "output/mathlib4_dependency_graph/data_5e932f97dd25535344f80f9dd8da3aab83df0fe6"

def get_dot_name(name: JixiaLeanName) -> str:
    return ".".join([str(part) for part in name])

def get_item(jtem: JixiaItem) -> Item:
    typeReferences, valueReferences = [], []
    if jtem.typeReferences is not None:
        typeReferences = [get_dot_name(name) for name in jtem.typeReferences]
    if jtem.valueReferences is not None:
        valueReferences = [get_dot_name(name) for name in jtem.valueReferences]
    
    return Item(
        name=get_dot_name(jtem.name),
        kind=jtem.kind,
        isProp=jtem.isProp,
        typeFallback=jtem.typeFallback,
        typeFull=jtem.typeFull,
        typeReadable=jtem.typeReadable,
        typeReferences=typeReferences,
        valueReferences=valueReferences,
    )

def get_item_key(item: Item) -> str:
    return "item." + item.name

def get_file_key(filename: str) -> str:
    return "file." + filename


def stream_json_list(filename: str) -> Iterator:
    with open(filename, "rb") as f:
        items = ijson.items(f, "item") # "item" is the prefix for elements in a root array
        for item in items:
            yield item


filename_list = list(os.listdir(graph_dir))
filename_list.sort()


total_count, error_count = 0, 0

with open("error.jsonl", "w") as f:
    with open("items.jsonl", "w") as f1:
        for filename in tqdm(filename_list):
            path = os.path.join(graph_dir, filename)
            for o in stream_json_list(path):
                total_count += 1
                try:
                    i = get_item(JixiaItem.model_validate(o))
                    f1.write(i.model_dump_json() + "\n")
                        
                except pydantic_core._pydantic_core.ValidationError:
                    error_count += 1
                    f.write(json.dumps(o) + "\n")
                    print("error_rate", error_count / total_count)
                    

print(error_count, total_count)