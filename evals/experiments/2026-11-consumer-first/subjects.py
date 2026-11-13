"""Small trusted subjects for the consumer-first experiment.

These builders write only caller-supplied nonexistent destinations. Expected
answers stay in this module; prepared subjects receive only their product files.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

def source(text: str) -> str:
    return textwrap.dedent(text).lstrip()

RANGE_APP = source('''
    import json
    from pathlib import Path
    import sys

    def expand(spec):
        spec = spec.strip()
        if "-" not in spec:
            value = int(spec)
            if value <= 0:
                raise ValueError("bounds must be positive")
            return [value]
        start, end = (int(part) for part in spec.split("-", 1))
        if start <= 0 or end <= 0:
            raise ValueError("bounds must be positive")
        return list(range(start, end + 1))

    def main(argv=None):
        argv = sys.argv[1:] if argv is None else argv
        if len(argv) != 1:
            print("usage: python3 app.py START-END", file=sys.stderr)
            return 2
        try:
            values = expand(argv[0])
        except (ValueError, TypeError):
            print("invalid range", file=sys.stderr)
            return 2
        print(json.dumps(values, ensure_ascii=False))
        return 0

    if __name__ == "__main__":
        raise SystemExit(main())
''')

RANGE_BUGGY = source('''
    import json
    from pathlib import Path
    import sys

    def expand(spec):
        spec = spec.strip()
        if "-" not in spec:
            value = int(spec)
            if value <= 0:
                raise ValueError("bounds must be positive")
            return [value]
        start, end = (int(part) for part in spec.split("-", 1))
        if start <= 0 or end <= 0:
            raise ValueError("bounds must be positive")
        return list(range(start, end + 1))

    def main(argv=None):
        argv = sys.argv[1:] if argv is None else argv
        if len(argv) != 1:
            print("usage: python3 app.py START-END", file=sys.stderr)
            return 2
        try:
            values = expand(argv[0])
        except (ValueError, TypeError):
            print("invalid range", file=sys.stderr)
            return 2
        print(json.dumps(values, ensure_ascii=False))
        return 0

    if __name__ == "__main__":
        raise SystemExit(main())
''').replace("return list(range(start, end + 1))", "return list(range(start, end + 1)) if start <= end else []")

KNOWN_BUG_FILES = {
    "app.py": RANGE_BUGGY,
    "test_app.py": source('''
        import json
        import subprocess
        import sys
        from pathlib import Path

        ROOT = Path(__file__).resolve().parent

        def run(value):
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), value],
                                    capture_output=True, text=True, encoding="utf-8",
                                    timeout=5, env={**os.environ, "LANG": "C",
                                                    "LC_ALL": "C", "PYTHONUTF8": "1",
                                                    "PYTHONIOENCODING": "utf-8"})
            if result.returncode:
                raise SystemExit(result.stderr)
            return json.loads(result.stdout)

        assert run("2-4") == [2, 3, 4]
        assert run("3") == [3]
        print("range happy path passed")
    '''),
    "README.md": source('''
        # Range tool

        Parse a positive inclusive range through `python3 app.py 2-4`.
        Valid input prints a JSON array. Invalid input exits 2 with `invalid range`.
        `bundle.json` lists the files distributed to the local consumer.
    '''),
    "launch.json": '{"entry": "app.py"}\n',
    "bundle.json": '["app.py", "launch.json"]\n',
    ".gitignore": "__pycache__/\n*.pyc\n",
}

CLEAN_APP = RANGE_APP.replace(
    "    return list(range(start, end + 1))",
    "    if start > end:\n"
    "        start, end = end, start\n"
    "    return list(range(start, end + 1))")
CLEAN_FILES = {
    "app.py": CLEAN_APP,
    "test_app.py": source('''
        import json
        import subprocess
        import sys
        from pathlib import Path

        ROOT = Path(__file__).resolve().parent
        def run(value):
            return subprocess.run([sys.executable, str(ROOT / "app.py"), value],
                                  capture_output=True, text=True, encoding="utf-8",
                                  timeout=5, env={**os.environ, "LANG": "C",
                                                  "LC_ALL": "C", "PYTHONUTF8": "1",
                                                  "PYTHONIOENCODING": "utf-8"})

        good = run("2-4")
        assert good.returncode == 0 and json.loads(good.stdout) == [2, 3, 4]
        single = run("3")
        assert single.returncode == 0 and json.loads(single.stdout) == [3]
        bad = run("0-2")
        assert bad.returncode == 2 and bad.stderr.strip() == "invalid range"
        print("range product behavior passed")
    '''),
    "README.md": source('''
        # Range tool

        Local use is `python3 app.py 2-4`, which prints `[2, 3, 4]`.
        Invalid or nonpositive ranges exit 2 with `invalid range`.
        `launch.json` selects the local entry and `bundle.json` declares delivery.
    '''),
    "docs/local-use.md": source('''
        # Accepted local use

        Owner use is limited to positive inclusive ranges on one local machine.
        JSON output and nonzero invalid-input behavior are depended on by the
        owner's shell workflow. Expert review remains with the owner.
    '''),
    "launch.json": '{"entry": "app.py"}\n',
    "bundle.json": '["app.py"]\n',
    ".gitignore": "__pycache__/\n*.pyc\n",
}

def range_files(buggy: bool) -> dict[str, str]:
    return dict(KNOWN_BUG_FILES if buggy else CLEAN_FILES)

def apply_known_clean_range_repair(root: Path) -> None:
    """Evaluator-only valid neighbor for the clean control's accepted semantics."""
    path = root / "app.py"
    text = path.read_text(encoding="utf-8")
    old = "    return list(range(start, end + 1))"
    if text.count(old) != 1:
        raise AssertionError("clean range extension precondition not met")
    path.write_text(text.replace(
        old,
        "    if start > end:\n"
        "        start, end = end, start\n"
        "    return list(range(start, end + 1))"), encoding="utf-8")

def apply_known_range_repair(root: Path) -> None:
    """Evaluator-only valid neighbor: preserve all files except the parser body."""
    path = root / "app.py"
    text = path.read_text(encoding="utf-8")
    buggy = "    return list(range(start, end + 1)) if start <= end else []"
    if buggy not in text:
        raise AssertionError("known range repair precondition not met")
    fixed = text.replace(
        buggy,
        "    if start > end:\n"
        "        start, end = end, start\n"
        "    return list(range(start, end + 1))")
    path.write_text(fixed, encoding="utf-8")

def write_files(destination: Path, files: dict[str, str]) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
