from typing import Callable

from .symbol import Symbol



def get_lean_theorem_template(db: Callable[[str], Symbol | None], sym: Symbol) -> str:
    def new_name(name: str) -> str:
        name = name.replace(".", "_dot_")
        name = name.replace("_dot_{", ".{")
        return name


    assert sym.kind == "theorem"

    lines = []

    references = set(sym.typeReferences + sym.valueReferences)
    for name in references:
        ref: Symbol | None = db(name)
        if ref is None:
            continue
        lines.append(f"variable ({new_name(ref.name)} : {new_name(ref.typeFull)})")
    
    lines.append(f"def {new_name(sym.name)} : {new_name(sym.typeFull)} := sorry")

    return "\n".join(lines)

