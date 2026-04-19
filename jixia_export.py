import os
import shutil

import jixia_util as jixia
from jixia_util.structs import LeanName

JIXIA = "jixia/.lake/build/bin/jixia"
MATHLIB_DIR = "mathlib4"
MATHLIB_MODULE = "Mathlib"
OUTPUT_DIR = "output/mathlib4_dependency_graph"

def to_jixia_module(module: str) -> LeanName:
    return module.split(".")

def get_lean_version(repo_dir: str) -> str:
    version = open(os.path.join(repo_dir, "lean-toolchain")).read()
    return version.strip()

jixia.run.executable = os.path.abspath(JIXIA)

def main():
    shutil.copyfile(
        src="README.md",
        dst=os.path.join(OUTPUT_DIR, "README.md"),
    )

    version = get_lean_version(MATHLIB_DIR)
    version_number = version.split(":")[-1]

    project = jixia.LeanProject(
        root=os.path.abspath(MATHLIB_DIR),
        output_dir=os.path.abspath(os.path.join(OUTPUT_DIR, f"data_{version_number}")),
    )

    project.batch_run_jixia(
        prefixes=[to_jixia_module(MATHLIB_MODULE)], 
        timeout=300,
        max_workers=4,
    )

if __name__ == "__main__":
    main()
