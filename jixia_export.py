import os
import shutil

import git

import jixia_util as jixia
from jixia_util.structs import LeanName

JIXIA = "jixia/.lake/build/bin/jixia"
MATHLIB_DIR = "mathlib4"
MATHLIB_MODULE = "Mathlib"
OUTPUT_DIR = "output/mathlib4_dependency_graph"

def to_jixia_module(module: str) -> LeanName:
    return module.split(".")

def get_head_commit(repo_dir: str) -> str:
    repo = git.Repo(repo_dir)
    return repo.head.commit.hexsha

jixia.run.executable = os.path.abspath(JIXIA)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(
        src="README.md",
        dst=os.path.join(OUTPUT_DIR, "README.md"),
    )

    commit = get_head_commit(MATHLIB_DIR)

    project = jixia.LeanProject(
        root=os.path.abspath(MATHLIB_DIR),
        output_dir=os.path.abspath(os.path.join(OUTPUT_DIR, f"data_{commit}")),
    )

    project.batch_run_jixia(
        prefixes=[to_jixia_module(MATHLIB_MODULE)], 
        timeout=300,
        max_workers=8,
    )

if __name__ == "__main__":
    main()
