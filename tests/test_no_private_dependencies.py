import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_repo_validator_passes():
    subprocess.run([sys.executable, "scripts/validate_public_repo.py"], cwd=ROOT, check=True)
