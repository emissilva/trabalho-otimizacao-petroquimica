from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebook"
NOTEBOOK = NOTEBOOK_DIR / "pipeline_petroquimico.ipynb"

nb = nbformat.read(NOTEBOOK, as_version=4)
client = NotebookClient(
    nb,
    timeout=900,
    kernel_name="python3",
    resources={"metadata": {"path": str(NOTEBOOK_DIR)}},
)
client.execute()
nbformat.write(nb, NOTEBOOK)
print(f"Notebook executado sem erros: {NOTEBOOK}")
