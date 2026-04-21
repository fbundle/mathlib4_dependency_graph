
from pydantic import BaseModel


class Symbol(BaseModel):
    name: str
    kind: str
    isProp: bool
    
    typeFallback: str # always exist
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[str]
    valueReferences: list[str]