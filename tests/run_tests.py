import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
venv_python = project_root / ".venv" / "Scripts" / "python.exe"
python = str(venv_python) if venv_python.exists() else sys.executable

subprocess.run([python, "-m", "pytest", "tests/", "-v"], cwd=project_root)
