import os

from huggingface_hub import snapshot_download
from dotenv import load_dotenv



OUTPUT_DIR = "output/mathlib4_dependency_graph"

def download(output_dir: str):
    output_dir = os.path.abspath(output_dir)

    load_dotenv()
    hf_user = os.environ.get("HF_USER", None)
    if hf_user is None:
        raise RuntimeError("HF_USER must be set")

    repo_id = hf_user + "/" + os.path.basename(output_dir)

    snapshot_download(
        local_dir=output_dir,
        repo_id=repo_id,
        repo_type="dataset",
    )


if __name__ == "__main__":
    download(OUTPUT_DIR)
