import re
from typing import Callable, Set, Dict, List
from .symbol import Symbol

# Common Lean 4 and Mathlib built-ins/classes to skip declaring
BUILTINS = {
    "Prop", "Type", "Sort", "Eq", "HEq", "Unit", "PUnit", "True", "False",
    "And", "Or", "Not", "Exists", "Decidable", "Bool", "Nat", "Int", "UInt8", "UInt16", "UInt32", "UInt64",
    "Float", "String", "Char", "List", "Array", "Option", "Sum", "Prod", "PProd", "MProd",
    "Inhabited", "Nonempty", "Subsingleton", "Unique", "DecidableEq", "BEq", "Hashable",
    "Add", "Sub", "Mul", "Div", "Mod", "Neg", "Pow", "LE", "LT",
    "EmptyCollection", "HasSubset", "HasSSubset", "Union", "Inter", "SUnion", "SInter",
    "SetLike", "FunLike", "Coe", "CoeOut", "CoeTail", "CoeHead", "CoeDep", "CoeFun", "CoeSort",
    "OfNat", "OfInt", "HPow", "HAdd", "HSub", "HMul", "HDiv", "HMod", "HNeg",
    "Membership", "SizeOf", "DecidableRel", "DecidablePred", "Quot", "Quotient", "Subtype",
    "Fin", "Set", "Function", "Iff", "Trans", "Inv", "Max", "Min", "Ne", "NeZero",
    "DecidableLE", "DecidableLT", "Equivalence", "HasEquiv", "Insert", "IntCast", "Inv",
    "LawfulBEq", "LawfulSingleton", "NatCast", "Ord", "Ordering", "PEmpty", "PLift", "PSigma",
    "Pure", "SDiff", "SMul", "Setoid", "Sigma", "Singleton", "WellFounded", "Zero",
    "absurd", "and_assoc", "and_comm", "and_congr", "and_false", "and_iff_left", "and_imp",
    "and_left_comm", "and_self", "and_self_iff", "and_true", "autoParam", "compareOfLessAndEq",
    "cond", "congr", "congrArg", "congrFun", "decidable_of_decidable_of_iff", "decidable_of_iff",
    "decide_eq_true_eq", "decide_true", "dif_neg", "dif_pos", "dite", "dite_congr", "eagerReduce",
    "eq_comm", "eq_false", "eq_iff_iff", "eq_iff_true_of_subsingleton", "eq_of_heq", "eq_self",
    "eq_true", "exists_and_left", "exists_congr", "exists_imp", "exists_prop", "exists_prop_congr",
    "false_or", "flip", "forall_and", "forall_comm", "forall_congr", "forall_const", "forall_eq",
    "forall_not_of_not_exists", "forall_prop_domain_congr", "funext", "funext_iff", "heq_eq_eq",
    "heq_of_eq", "id", "if_neg", "if_pos", "if_true", "iff_of_eq", "iff_of_true", "iff_self",
    "iff_true", "iff_true_intro", "imp_congr_right", "imp_iff_right", "imp_not_comm", "imp_self"
}

def get_lean_theorem_template(db: Callable[[str], Symbol | None], sym: Symbol) -> str:
    def sanitize_name(name: str) -> str:
        name = re.sub(r'\.\{.*\}', '', name)
        name = name.replace(".", "_dot_")
        name = name.replace("ᵒᵖ", "_op")
        name = name.replace("ᵃ", "_a")
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        if name and name[0].isdigit():
            name = "n" + name
        return name

    def sanitize_type(text: str) -> str:
        if text is None: return "Type"
        def repl(match):
            name = match.group(0)
            if name.startswith(".{"): return name
            return name.replace(".", "_dot_").replace("ᵒᵖ", "_op").replace("ᵃ", "_a")
        text = re.sub(r'(?<!\.)\b[a-zA-Z][a-zA-Z0-9._]*\b', repl, text)
        text = text.replace("ᵒᵖ", "_op")
        text = text.replace("ᵃ", "_a")
        return text

    assert sym.kind == "theorem"

    all_refs: Dict[str, Symbol] = {}
    pending = set(sym.typeReferences + sym.valueReferences)
    visited = set()

    all_mentioned = set(sym.typeReferences + sym.valueReferences)

    while pending:
        name = pending.pop()
        if name in visited: continue
        visited.add(name)
        
        ref = db(name)
        if ref:
            all_refs[name] = ref
            pending.update(ref.typeReferences)
            pending.update(ref.valueReferences)
            all_mentioned.update(ref.typeReferences)
            all_mentioned.update(ref.valueReferences)

    # Topological sort
    sorted_names = []
    topo_visited = set()
    stack = set()

    def visit(name):
        if name in stack: return # Cycle
        if name in topo_visited: return
        stack.add(name)
        ref = all_refs.get(name)
        if ref:
            deps = sorted(list(set(ref.typeReferences + ref.valueReferences)))
            for dep in deps:
                visit(dep)
        stack.remove(name)
        topo_visited.add(name)
        if name in all_refs:
            sorted_names.append(name)

    for name in sorted(all_refs.keys()):
        visit(name)

    universes = set()
    def collect_universes(text: str):
        if text:
            matches = re.findall(r'\b(u|v|w|u_\d+|v_\d+|w_\d+)\b', text)
            universes.update(matches)

    lines = []
    lines.append("set_option autoImplicit true")
    lines.append("set_option checkBinderAnnotations false")
    lines.append("set_option linter.unusedVariables false")

    # Declare missing things
    for m in sorted(list(all_mentioned)):
        if m in BUILTINS: continue
        if m in all_refs: continue
        if "." not in m: continue
        san_m = sanitize_name(m)
        lines.append(f"variable ({san_m} : _)")

    for name in sorted_names:
        if name in BUILTINS: continue
        ref = all_refs[name]
        collect_universes(ref.typeFull)
        lines.append(f"axiom {sanitize_name(ref.name)} : {sanitize_type(ref.typeFull)}")
    
    collect_universes(sym.typeFull)
    
    header = []
    if universes:
        header.append(f"universe {' '.join(sorted(list(universes)))}")
    
    lines.append(f"def {sanitize_name(sym.name)} : {sanitize_type(sym.typeFull)} := sorry")

    return "\n".join(header + lines)
