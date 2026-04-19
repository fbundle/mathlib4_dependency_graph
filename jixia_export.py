import os

import jixia_util as jixia

jixia.run.executable = os.path.abspath("jixia/.lake/build/bin/jixia")

project = jixia.LeanProject(
    root=os.path.abspath("mathlib4"),
    output_dir=".jixia",
)

project.batch_run_jixia(
    prefixes=["Mathlib"]
)