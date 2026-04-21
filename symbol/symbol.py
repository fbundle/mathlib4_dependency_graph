
from pydantic import BaseModel


class Symbol(BaseModel):
    name: str
    kind: str # Literal['inductive', 'opaque', 'recursor', 'definition', 'constructor', 'theorem']
    isProp: bool
    
    typeFallback: str # always exist
    typeFull: str | None
    typeReadable: str | None

    typeReferences: list[str]
    valueReferences: list[str]