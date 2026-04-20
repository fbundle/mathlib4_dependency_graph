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


filename_list = list(os.listdir(graph_dir))

total_count, error_count = 0, 0

with lmdb.open("cache", map_size=100 * 1024**3) as env: # max 100GB
    with env.begin(write=True) as txn:
        for filename in filename_list:
            file_key = get_file_key(filename)
            if txn.get(file_key.encode()) is not None:
                continue
            
            path = os.path.join(graph_dir, filename)
            for o in stream_json_list(path):
                total_count += 1
                try:
                    i = JixiaItem.model_validate(o)    
                    txn.put(get_item_key(i).encode(), i.model_dump_json().encode())
                        
                except pydantic_core._pydantic_core.ValidationError:
                    error_count += 1
                    print("error ratio:", error_count/total_count)

print(error_count, total_count)