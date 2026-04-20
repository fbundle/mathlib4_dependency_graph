import dbm
import json
import os
import sys



import lmdb
from pydantic import BaseModel
import pydantic_core




from pydantic import BaseModel
from tqdm import tqdm


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

def get_dot_name(lean_name: JixiaLeanName) -> str:
    return ".".join(lean_name)


graph_dir = "output/mathlib4_dependency_graph/data_5e932f97dd25535344f80f9dd8da3aab83df0fe6"

name_list = list(os.listdir(graph_dir))

total_count = 0
error_count = 0

with lmdb.open("cache", map_size=100 * 1024**3) as env: # max 100GB
    with env.begin(write=True) as txn:
        for name in tqdm(name_list):
            path = os.path.join(graph_dir, name)
            o_list = json.load(open(path))
            for o in o_list:
                total_count += 1
                try:
                    i = JixiaItem.model_validate(o)
                    key = get_dot_name(i.name)
                    txn.put(key.encode(), i.model_dump_json().encode())
                except pydantic_core._pydantic_core.ValidationError:
                    error_count += 1

print(error_count, total_count)