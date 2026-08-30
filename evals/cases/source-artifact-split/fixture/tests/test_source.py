#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys


root = Path(__file__).resolve().parents[1]
result = subprocess.run(
    [sys.executable, "src/cli.py"],
    cwd=root,
    check=False,
    capture_output=True,
    text=True,
)
if result.returncode != 0 or result.stdout.strip() != "artifact-v2":
    raise SystemExit("source CLI contract failed")
print("source CLI contract: PASS")
