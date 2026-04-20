import os
from typing import Iterator



import lmdb
from pydantic import BaseModel
import pydantic_core


import ijson

from pydantic import BaseModel
from tqdm import tqdm

import multiprocess as mp

type JixiaLeanName = list[str]

class JixiaItem(BaseModel):
    name: JixiaLeanName
    kind: str # TODO - check all kinds - change this to Literal
    isProp: bool
    
    typeFallback: str
    typeFull: str
    typeReadable: str

    typeReferences: list[JixiaLeanName]
    valueReferences: list[JixiaLeanName]


graph_dir = "output/mathlib4_dependency_graph/data_5e932f97dd25535344f80f9dd8da3aab83df0fe6"

def get_item_key(item: JixiaItem) -> str:
    return "item." + ".".join(item.name)

def get_file_key(filename: str) -> str:
    return "file." + filename


def stream_json_list(filename: str) -> Iterator:
    with open(filename, 'rb') as f:
        items = ijson.items(f, 'item') # 'item' is the prefix for elements in a root array
        for item in items:
            yield item

def write_cache(env: lmdb.Environment, filename: str) -> bool:
    with env.begin(write=True) as txn:
        file_key = get_file_key(filename)
        if txn.get(file_key.encode()) is not None:
            return False
        
        path = os.path.join(graph_dir, filename)
        for o in stream_json_list(path):
            try:
                i = JixiaItem.model_validate(o)
                item_key = get_item_key(i)
                txn.put(item_key.encode(), i.model_dump_json().encode())
            except pydantic_core._pydantic_core.ValidationError:
                pass
        
        txn.put(file_key.encode(), b"visited")
        return True

filename_list = list(os.listdir(graph_dir))

with lmdb.open("cache", map_size=100 * 1024**3) as env: # max 100GB
    with mp.Pool() as pool:  # type: ignore
        for r in tqdm(
            pool.imap_unordered(lambda filename: write_cache(env, filename), filename_list),
            total=len(filename_list),
        ):
            pass