"""Consumer probe and mutation controls for historical python-dotenv #697.

Only disposable git-archive copies are edited. No installation or API key is
needed. Click must already be available in the invoking Python environment.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import tempfile
from importlib.metadata import version

BEFORE = "a00cb2eed0704cd6d2071b2004c37e95ccc86ee5"
AFTER = "e0310e5bb3f2b701b11bbc007ca0c82c1bd56f38"
CASES = [
    ("--no-override", "environment", ["environment", "environment/suffix"]),
    ("--no-override", "", ["", "/suffix"]),
    ("--override", "environment", ["file", "file/suffix"]),
]
VARIANTS = [
    ("historical-before", BEFORE, None, "historical defect"),
    ("upstream-fixed", AFTER, None, "upstream repair; no further repair needed"),
    ("wrong-layer-default", BEFORE, "wrong-default", "injected ineffective repair"),
    ("global-precedence", BEFORE, "global-precedence", "injected overbroad repair"),
    ("incomplete-propagation", AFTER, "drop-filter", "injected incomplete repair"),
    ("misleading-readme", BEFORE, "readme", "injected incorrect documentation claim"),
]
EXPECTED = {
    "historical-before": [False, False, True, True],
    "upstream-fixed": [True, True, True],
    "wrong-layer-default": [False, False, True],
    "global-precedence": [True, True, False],
    "incomplete-propagation": [False, False, True],
    "misleading-readme": [False, False, True],
}


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise ValueError(f"Mutation target is not unique: {path.name}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def mutate(root, mutation):
    main = root / "src/dotenv/main.py"
    if mutation == "wrong-default":
        replace_once(main, "        override: bool = True,", "        override: bool = False,")
    elif mutation == "global-precedence":
        replace_once(main, "        override=True,", "        override=False,")
    elif mutation == "drop-filter":
        replace_once(root / "src/dotenv/cli.py", "if v is not None and (override or k not in os.environ)", "if v is not None")
    elif mutation == "readme":
        path = root / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n\n## Synthetic audit-control claim\nThe CLI --no-override mode already expands derived values using the inherited environment. No implementation gap remains.\n", encoding="utf-8")


def observe(root, envfile, option, value, expected, api=False):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root / "src")
    env["RTA_CASE_BASE"] = value
    env.pop("RTA_CASE_DERIVED", None)
    env.pop("PYTHON_DOTENV_DISABLED", None)
    read_values = "import json,os; print(json.dumps([os.environ['RTA_CASE_BASE'], os.environ['RTA_CASE_DERIVED']]))"
    if api:
        command = [sys.executable, "-c", "from dotenv import load_dotenv; import sys; load_dotenv(sys.argv[1], override=False); " + read_values, str(envfile)]
    else:
        command = [sys.executable, "-m", "dotenv", "-f", str(envfile), "run", option, sys.executable, "-c", read_values]
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=15)
    try:
        actual = json.loads(result.stdout)
    except json.JSONDecodeError:
        actual = None
    return {
        "mode": "load_dotenv(override=False)" if api else option,
        "existing_value": value, "expected": expected, "actual": actual,
        "returncode": result.returncode,
        "pass": result.returncode == 0 and actual == expected,
        "stderr": result.stderr,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.resolve().is_relative_to(args.repo.resolve()):
        parser.error("--output must be outside the observed source repository")
    records = []
    for name, revision, mutation, provenance in VARIANTS:
        archive = subprocess.run(["git", "archive", revision, "src", "README.md"], cwd=args.repo, capture_output=True, check=True, timeout=60).stdout
        with tempfile.TemporaryDirectory(prefix="rta-dotenv-") as temporary:
            root = Path(temporary)
            with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
                # These pinned inputs contain regular source files only. Write
                # their bytes explicitly; no extraction-filter version dependency
                # and no link or traversal interpretation is needed.
                for member in stream:
                    if member.isdir():
                        continue
                    member_path = Path(member.name)
                    if not member.isfile() or member_path.is_absolute() or ".." in member_path.parts:
                        raise ValueError("Unexpected pinned source archive entry")
                    target = root / member_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(stream.extractfile(member).read())
            mutate(root, mutation)
            envfile = root / ".env"
            envfile.write_text("RTA_CASE_BASE=file\nRTA_CASE_DERIVED=${RTA_CASE_BASE}/suffix\n", encoding="utf-8")
            observations = [observe(root, envfile, *case) for case in CASES]
            if name == "historical-before":
                observations.append(observe(root, envfile, *CASES[0], api=True))
            records.append({
                "variant": name, "revision": revision, "provenance": provenance,
                "source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in [root / "src/dotenv/cli.py", root / "src/dotenv/main.py", root / "README.md"]},
                "observations": observations,
            })
    output = {
        "case": "python-dotenv-697-consumer-environment", "schema_version": 1,
        "upstream_repository": "https://github.com/theskumar/python-dotenv",
        "issue_url": "https://github.com/theskumar/python-dotenv/issues/697",
        "repair_url": "https://github.com/theskumar/python-dotenv/pull/698",
        "python": platform.python_version(), "platform": platform.system(),
        "click_version": version("click"),
        "execution_surface": "python -m dotenv from temporary source archive; actual spawned child reads final environment",
        "variants": records,
        "matrix_matches_expectation": all(
            [row["pass"] for row in record["observations"]] == EXPECTED[record["variant"]]
            and all(row["returncode"] == 0 for row in record["observations"])
            for record in records),
    }
    rendered = json.dumps(output, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if output["matrix_matches_expectation"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
