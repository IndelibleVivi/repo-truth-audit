#!/usr/bin/env python3
"""Probe a real mitt package consumer in disposable copies, without installing.

Prepare pinned inputs as documented in README.md. This evaluator never invokes
an agent, fetches dependencies, or edits the source checkout or package seed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE_SHA = "6b41670516ed8e8b738612f60491995470aa63b3"
TASK = """import mitt from 'mitt';
const events = mitt<{ foo: string }>();
events.on('*', (type, value) => {});
events.off('*');
"""
CONTROL = """import mitt from 'mitt';
const events = mitt<{ foo: string }>();
const wildcard = (type: 'foo', value: string) => {};
events.on('*', wildcard);
events.off('*', wildcard);
events.off('foo');
// @ts-expect-error invalid events must remain rejected
events.off('missing');
// @ts-expect-error wrong handler type must remain rejected
events.off('*', (type: 'foo', value: number) => {});
"""
RUNTIME = """const assert = require('node:assert/strict');
const mitt = require('mitt');
const events = mitt();
const observed = [];
events.on('foo', x => observed.push(['named', x]));
events.on('*', (type, x) => observed.push(['wildcard', type, x]));
events.emit('foo', 'before');
events.off('*');
events.emit('foo', 'after');
assert.deepEqual(observed, [
  ['named', 'before'], ['wildcard', 'foo', 'before'], ['named', 'after']
]);
console.log(JSON.stringify(observed));
"""
OLD = "off(type: '*', handler: WildcardHandler<Events>): void;"
NEW = "off(type: '*', handler?: WildcardHandler<Events>): void;"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise ValueError(f"Input changed: nonunique mutation in {path.name}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def run(cwd: Path, argv: list[str], paths: dict[str, str]) -> dict:
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=30)
    def portable(value: str) -> str:
        for path, label in paths.items():
            value = value.replace(path, label)
        return value
    return {"argv": [portable(str(a)) for a in argv], "exit_code": result.returncode,
            "stdout": portable(result.stdout), "stderr": portable(result.stderr)}


def probe(source: Path, seed: Path) -> dict:
    source = source.resolve()
    seed = seed.resolve()
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    if sha != SOURCE_SHA:
        raise ValueError(f"Expected source {SOURCE_SHA}; received {sha}")
    package = seed / "node_modules/mitt"
    compiler = seed / "node_modules/typescript"
    for root, expected in ((package, "3.0.1"), (compiler, "4.9.5")):
        if json.loads((root / "package.json").read_text())["version"] != expected:
            raise ValueError(f"Unexpected dependency at {root.name}; expected {expected}")
    original = subprocess.check_output(
        ["git", "show", f"{SOURCE_SHA}:src/index.ts"], cwd=source).decode("utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Source input changed")
    result = {"schema_version": 1, "source_repo": "https://github.com/developit/mitt",
              "source_sha": sha, "source_input": "git show of pinned src/index.ts; working-tree edits unused",
              "source_file_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
              "node": subprocess.check_output(["node", "--version"], text=True).strip(),
              "typescript": "4.9.5", "npm_package": "mitt@3.0.1", "variants": {}}
    expected = {
        "baseline": {"consumer_typecheck": 2, "type_controls": 0, "runtime_preservation": 0},
        "source_only": {"consumer_typecheck": 2, "type_controls": 0, "runtime_preservation": 0,
                        "source_typecheck": 0},
        "delivered_types": {"consumer_typecheck": 0, "type_controls": 0, "runtime_preservation": 0},
        "wrong_clear_all": {"consumer_typecheck": 0, "type_controls": 0, "runtime_preservation": 1},
    }
    with tempfile.TemporaryDirectory(prefix="rta-mitt-") as raw:
        workspace = Path(raw)
        paths = {str(workspace): "<temporary>", str(seed): "<consumer-seed>"}
        for kind, obligations in expected.items():
            work = workspace / kind
            selected = work / "node_modules/mitt"
            shutil.copytree(package, selected)
            (work / "task.ts").write_text(TASK, encoding="utf-8")
            (work / "control.ts").write_text(CONTROL, encoding="utf-8")
            (work / "runtime.cjs").write_text(RUNTIME, encoding="utf-8")
            if kind == "source_only":
                (work / "src").mkdir()
                (work / "src/index.ts").write_text(original.replace(OLD, NEW), encoding="utf-8")
                (work / "source-task.ts").write_text(TASK.replace("from 'mitt'", "from './src/index'"), encoding="utf-8")
            if kind in {"delivered_types", "wrong_clear_all"}:
                replace_once(selected / "index.d.ts", OLD, NEW)
            if kind == "wrong_clear_all":
                replace_once(selected / "dist/mitt.js", "off:function(e,t){",
                             'off:function(e,t){if(e==="*"&&!t){n.clear();return;}')
            def compile_file(name):
                return run(work, ["node", str(compiler / "bin/tsc"), name, "--noEmit", "--strict",
                                  "--lib", "es2015", "--moduleResolution", "node"], paths)
            checks = {"consumer_typecheck": compile_file("task.ts"),
                      "type_controls": compile_file("control.ts"),
                      "runtime_preservation": run(work, ["node", "runtime.cjs"], paths)}
            if kind == "source_only":
                checks["source_typecheck"] = compile_file("source-task.ts")
            for name, code in obligations.items():
                if checks[name]["exit_code"] != code:
                    raise AssertionError(f"{kind}/{name}: {checks[name]}")
            checks["declaration_sha256"] = hashlib.sha256((selected / "index.d.ts").read_bytes()).hexdigest()
            result["variants"][kind] = checks
    result["status"] = "passed"
    result["target_model_invocations"] = 0
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--consumer-seed", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and any(args.output.resolve().is_relative_to(root.resolve())
                           for root in (args.source, args.consumer_seed)):
        parser.error("--output must be outside the observed source and consumer seed")
    result = probe(args.source, args.consumer_seed)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
