# MATHLIB4 DEPENDENCY GRAPH

make dependency graph for [mathlib4](https://github.com/leanprover-community/mathlib4) using [jixia](https://github.com/frenzymath/jixia_py)

## HOW TO

how to make your own mathlib4 graph

0. Clone the repository at [https://github.com/fbundle/mathlib4_dependency_graph](https://github.com/fbundle/mathlib4_dependency_graph)

1. Check out your favorite mathlib version

2. Use `build` script to build mathlib and jixia

3. Extract dependency graph by `jixia_export.py`

4. Get symbol file by `get_symbol_file.py`

5. Upload to huggingface using `upload_huggingface.py`



or just download the prebuilt files using `download_huggingface.py`

## PREBUILT GRAPH

- [https://huggingface.co/khanh2023/mathlib4_dependency_graph](https://huggingface.co/khanh2023/mathlib4_dependency_graph)