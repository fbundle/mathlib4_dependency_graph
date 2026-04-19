import os

import jixia_util as jixia
from jixia_util.structs import LeanName

JIXIA = "jixia/.lake/build/bin/jixia"
MATHLIB_DIR = "mathlib4"
MATHLIB_MODULE = "Mathlib"
OUTPUT_DIR = "output"

def to_jixia_module(module: str) -> LeanName:
    return module.split(".")


jixia.run.executable = os.path.abspath(JIXIA)

project = jixia.LeanProject(
    root=os.path.abspath(MATHLIB_DIR),
    output_dir=os.path.abspath(OUTPUT_DIR),
)

project.batch_run_jixia(
    prefixes=[to_jixia_module(MATHLIB_MODULE)], 
    timeout=1800,
)