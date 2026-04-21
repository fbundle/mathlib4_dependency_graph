from typing import Callable

from .symbol import Symbol

def get_lean_theorem_template(db: Callable[[str], Symbol], sym: Symbol) -> str:
    assert sym.kind == "theorem"

    lines = []

    references = set(sym.typeReferences + sym.valueReferences)
    for name in references:
        ref = db(name)
        lines.append(f"variable ({ref.name} : {ref.typeFallback})")
    
    lines.append(f"def {sym.name} : {sym.typeFallback} :=")

    return "\n".join(lines)

