import os

import jixia_util as jixia
from jixia_util.structs import LeanName

JIXIA = "jixia/.lake/build/bin/jixia"
MATHLIB_DIR = "mathlib4"
MATHLIB_MODULE = "Mathlib"

def to_jixia_module(module: str) -> LeanName:
    return module.split(".")


jixia.run.executable = os.path.abspath(JIXIA)

project = jixia.LeanProject(
    root=os.path.abspath(MATHLIB_DIR),
    output_dir=".jixia",
)

project.batch_run_jixia(
    prefixes=[to_jixia_module(MATHLIB_MODULE)], 
)