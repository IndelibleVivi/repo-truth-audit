#!/usr/bin/env python3
"""Controlled operation rehearsal on bundled synthetic programs only.

This evaluator applies known edits; it is NOT an autonomous model, a production
patch/rollback engine, a sandbox, or an interface for arbitrary repositories.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
from typing import Any


def source(text: str) -> str:
    return textwrap.dedent(text).lstrip()


ENTRY = source('''
    import argparse
    import importlib
    import json
    from pathlib import Path
    import sys

    ROOT = Path(__file__).resolve().parent
    sys.path.insert(0, str(ROOT))
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--state', required=True)
    parser.add_argument('--format', default='json')
    args = parser.parse_args()
    try:
        selected = json.loads((ROOT / 'delivery.json').read_text())['module']
        module = importlib.import_module(selected)
        records = json.loads(Path(args.input).read_text())
        output = module.process(records, Path(args.state), args.format)
    except (ValueError, TypeError, KeyError):
        print('invalid input', file=sys.stderr)
        raise SystemExit(2)
    except OSError:
        print('io failure', file=sys.stderr)
        raise SystemExit(3)
    sys.stdout.write(output)
''')

LEGACY = source('''
    import json

    def process(records, state, mode):
        if not isinstance(records, list):
            raise ValueError('records must be a list')
        rows = []
        for row in records:
            if (not isinstance(row, dict) or not isinstance(row.get('name'), str)
                    or type(row.get('amount')) is not int):
                raise ValueError('invalid record')
            rows.append({'name': row['name'], 'amount': row['amount']})
        if mode == 'json':
            output = json.dumps(rows, ensure_ascii=False, sort_keys=True) + '\\n'
        elif mode == 'text':
            output = ''.join(f"{row['name']}:{row['amount']}\\n" for row in rows)
        else:
            raise ValueError('unknown format')
        if rows:
            with state.open('a', encoding='utf-8') as handle:
                handle.write(f"{len(rows)}:{sum(row['amount'] for row in rows)}\\n")
        return output
''')

FORMATTING = source('''
    import json

    def normalize(records):
        if not isinstance(records, list):
            raise ValueError('records must be a list')
        rows = []
        for row in records:
            if (not isinstance(row, dict) or not isinstance(row.get('name'), str)
                    or type(row.get('amount')) is not int):
                raise ValueError('invalid record')
            rows.append({'name': row['name'], 'amount': row['amount']})
        return rows

    def render(rows, mode):
        if mode == 'json':
            return json.dumps(rows, ensure_ascii=False, sort_keys=True) + '\\n'
        if mode == 'text':
            return ''.join(f"{row['name']}:{row['amount']}\\n" for row in rows)
        raise ValueError('unknown format')
''')

TRANSITION = source('''
    from formatting import normalize, render

    def process(records, state, mode):
        rows = normalize(records)
        output = render(rows, mode)
        if rows:
            with state.open('a', encoding='utf-8') as handle:
                handle.write(f"{len(rows)}:{sum(row['amount'] for row in rows)}\\n")
        return output
''')

STORAGE = source('''
    def append_receipt(rows, state):
        if rows:
            with state.open('a', encoding='utf-8') as handle:
                handle.write(f"{len(rows)}:{sum(row['amount'] for row in rows)}\\n")
''')

RUNNER = source('''
    from formatting import normalize, render
    from storage import append_receipt

    def process(records, state, mode):
        rows = normalize(records)
        output = render(rows, mode)
        append_receipt(rows, state)
        return output
''')

BASELINE: dict[str, str] = {
    'entry.py': ENTRY,
    'legacy.py': LEGACY,
    'delivery.json': json.dumps({'module': 'legacy'}) + '\n',
    'bundle.json': json.dumps(['entry.py', 'legacy.py', 'delivery.json']) + '\n',
    'owner-notes.txt': 'Unrelated pre-existing uncommitted owner content.\n',
}

CUT_ONE: dict[str, str | None] = {
    'legacy.py': TRANSITION,
    'formatting.py': FORMATTING,
    'bundle.json': json.dumps(['entry.py', 'legacy.py', 'formatting.py', 'delivery.json']) + '\n',
}

CUT_TWO: dict[str, str | None] = {
    'runner.py': RUNNER,
    'storage.py': STORAGE,
    'legacy.py': None,
    'delivery.json': json.dumps({'module': 'runner'}) + '\n',
    'bundle.json': json.dumps(['entry.py', 'runner.py', 'formatting.py', 'storage.py', 'delivery.json']) + '\n',
}

ROWS = [{'name': 'Mina', 'amount': 3}, {'name': '舟', 'amount': 5}]
# Expected observations are fixed evaluator data, not generated from the candidate.
PROBES = [
    ('json', ROWS, 'json', False, 0,
     '[{"amount": 3, "name": "Mina"}, {"amount": 5, "name": "舟"}]\n', '', 'old\n2:8\n'),
    ('text_compat', ROWS, 'text', False, 0, 'Mina:3\n舟:5\n', '', 'old\n2:8\n'),
    ('empty', [], 'json', False, 0, '[]\n', '', 'old\n'),
    ('invalid_shape', {}, 'json', False, 2, '', 'invalid input\n', 'old\n'),
    ('bool_is_not_amount', [{'name': 'n', 'amount': True}], 'json', False,
     2, '', 'invalid input\n', 'old\n'),
    ('unknown_format', ROWS, 'unsupported', False, 2, '', 'invalid input\n', 'old\n'),
    ('write_failure', ROWS, 'json', True, 3, '', 'io failure\n', '<directory>'),
]


class ReconcileRequired(RuntimeError):
    pass


def seed(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name, contents in BASELINE.items():
        (root / name).write_text(contents, encoding='utf-8')


def snapshot(root: Path) -> dict[str, bytes]:
    """Fixture-only, quiet regular-file snapshot; no hostile-filesystem claim."""
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob('*')) if p.is_file()}


def identity(state: dict[str, bytes]) -> str:
    h = hashlib.sha256()
    for name, contents in sorted(state.items()):
        h.update(name.encode('utf-8') + b'\0')
        h.update(hashlib.sha256(contents).digest())
    return h.hexdigest()


def apply_known_cut(root: Path, cut: dict[str, str | None], expected: dict[str, bytes]) -> None:
    """Non-atomic evaluator edits on a quiet fixture, never a production patcher."""
    if snapshot(root) != expected:
        raise ReconcileRequired('snapshot moved: inspect before another write')
    for name, contents in cut.items():
        target = root / name
        if contents is None:
            if target.exists():
                target.unlink()
        else:
            target.write_text(contents, encoding='utf-8')


def restore_owned_fixture_changes(root: Path, before: dict[str, bytes], after: dict[str, bytes]) -> None:
    """Demonstrate selective code recovery; no crash-atomic or real-data guarantee."""
    touched = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
    current = snapshot(root)
    if any(current.get(name) != after.get(name) for name in touched):
        raise ReconcileRequired('owned postimage moved: do not overwrite concurrent work')
    for name in touched:
        target = root / name
        if name in before:
            target.write_bytes(before[name])
        elif target.exists():
            target.unlink()


def observe(root: Path, records: Any, mode: str, state_is_directory: bool = False) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix='rta-probe-') as temp:
        scratch = Path(temp)
        input_path = scratch / 'input.json'
        input_path.write_text(json.dumps(records, ensure_ascii=False), encoding='utf-8')
        state_path = scratch / 'ledger.txt'
        if state_is_directory:
            state_path.mkdir()
        else:
            state_path.write_text('old\n', encoding='utf-8')
        argv = [sys.executable, '-I', '-B', str(root / 'entry.py'),
                '--input', str(input_path), '--state', str(state_path), '--format', mode]
        env = {'PATH': os.defpath, 'HOME': str(scratch), 'TMPDIR': str(scratch),
               'LANG': 'C.UTF-8'}
        # For this known, bounded synthetic program only. Timeout/env are NOT an OS sandbox.
        result = subprocess.run(argv, cwd=scratch, env=env, capture_output=True,
                                timeout=5, check=False)
        if len(result.stdout) + len(result.stderr) > 32768:
            raise AssertionError('synthetic probe exceeded expected output')
        return {'exit': result.returncode, 'stdout': result.stdout.decode('utf-8'),
                'stderr': result.stderr.decode('utf-8'),
                'state': '<directory>' if state_path.is_dir() else state_path.read_text(encoding='utf-8')}


def characterize(root: Path) -> dict[str, dict[str, Any]]:
    observations = {}
    for name, rows, mode, directory, code, stdout, stderr, state in PROBES:
        actual = observe(root, rows, mode, directory)
        expected = dict(exit=code, stdout=stdout, stderr=stderr, state=state)
        if actual != expected:
            raise AssertionError(f'{name}: expected {expected!r}; observed {actual!r}')
        observations[name] = actual
    return observations


def assert_structure(root: Path) -> None:
    """Exact synthetic retirement contract; not a general reachability analyzer."""
    selected = json.loads((root / 'delivery.json').read_text())
    if selected != {'module': 'runner'}:
        raise AssertionError('delivery selector still chooses legacy')
    if (root / 'legacy.py').exists():
        raise AssertionError('old implementation has not been retired')
    for name in ('runner.py', 'formatting.py', 'storage.py'):
        if not (root / name).is_file():
            raise AssertionError(f'missing structural owner: {name}')
    for path in root.glob('*.py'):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'legacy':
                raise AssertionError('legacy delegation remains')
            if isinstance(node, ast.Import) and any(n.name == 'legacy' for n in node.names):
                raise AssertionError('legacy import remains')
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == 'open' and path.name != 'storage.py':
                    raise AssertionError('durable write primitive outside storage owner')


def build_artifact(root: Path, destination: Path) -> None:
    """Copy the fixture's declared delivery files, never arbitrary project build hooks."""
    destination.mkdir()
    for name in json.loads((root / 'bundle.json').read_text()):
        if not isinstance(name, str) or Path(name).name != name or name not in {
            'entry.py', 'legacy.py', 'runner.py', 'formatting.py', 'storage.py', 'delivery.json'
        }:
            raise AssertionError('invalid synthetic delivery member')
        (destination / name).write_bytes((root / name).read_bytes())


def complete_fixture(root: Path) -> None:
    apply_known_cut(root, CUT_ONE, snapshot(root))
    apply_known_cut(root, CUT_TWO, snapshot(root))


def add_format_probe(root: Path) -> dict[str, Any]:
    before = snapshot(root)
    new_code = FORMATTING.replace("    raise ValueError('unknown format')",
        "    if mode == 'compact':\n"
        "        return ';'.join(f\"{row['name']}={row['amount']}\" for row in rows) + '\\n'\n"
        "    raise ValueError('unknown format')")
    apply_known_cut(root, {'formatting.py': new_code}, before)
    changed = [name for name in before.keys() | snapshot(root).keys()
               if before.get(name) != snapshot(root).get(name)]
    if changed != ['formatting.py']:
        raise AssertionError(f'follow-on change crossed owners: {changed}')
    actual = observe(root, ROWS, 'compact')
    expected = dict(exit=0, stdout='Mina=3;舟=5\n', stderr='', state='old\n2:8\n')
    if actual != expected:
        raise AssertionError('follow-on formatter did not work through the selected entry')
    characterize(root)
    return {'changed_paths': changed, 'selected_entry_probe': actual}


def require_equal(actual: Any, expected: Any, label: str) -> None:
    # Validation must still execute under python -O; do not use bare assert.
    if actual != expected:
        raise AssertionError(f'{label}: observations differ')


def run_lab() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix='rta-operation-lab-') as temp:
        base = Path(temp)
        root = base / 'candidate'
        seed(root)
        before = snapshot(root)
        baseline = characterize(root)
        apply_known_cut(root, CUT_ONE, before)
        require_equal(characterize(root), baseline, "candidate_behavior")
        try:
            assert_structure(root)
        except AssertionError:
            first_is_transition = True
        else:
            raise AssertionError('first cut was wrongly accepted as complete')
        first = snapshot(root)
        apply_known_cut(root, CUT_TWO, first)
        require_equal(characterize(root), baseline, "candidate_behavior")
        assert_structure(root)
        after = snapshot(root)
        require_equal(after['owner-notes.txt'], before['owner-notes.txt'], 'owner_content')
        artifact = base / 'artifact'
        build_artifact(root, artifact)
        require_equal(characterize(artifact), baseline, "artifact_behavior")
        assert_structure(artifact)
        # The usefulness probe is made only in a second disposable candidate.
        probe_root = base / 'extension'
        probe_root.mkdir()
        for name, contents in after.items():
            (probe_root / name).write_bytes(contents)
        usefulness = add_format_probe(probe_root)
        require_equal(snapshot(root), after, "probe_did_not_mutate_candidate")
        return {
            'schema': 'rta-controlled-operation-lab/1',
            'status': 'passed',
            'goal': 'separate formatting and durable writer; switch actual delivery; retire legacy implementation',
            'baseline_identity': identity(before), 'final_identity': identity(after),
            'behavior_cases_at_each_boundary': len(PROBES),
            'increments': [
                {'id': 'extract-formatting', 'behavior': 'passed', 'whole_goal': 'checkpoint',
                 'structural_completion_correctly_rejected': first_is_transition},
                {'id': 'move-writer-switch-retire', 'behavior': 'passed', 'structure': 'passed',
                 'declared_artifact': 'passed', 'whole_goal': 'completed_fixture_scope'},
            ],
            'owner_dirty_content_preserved': True,
            'usefulness_probe': usefulness,
            'completion_layers': ['synthetic_source', 'synthetic_declared_artifact'],
            'not_observed': ['real_model_operation', 'independent_agent_review', 'user_repository',
                             'production_install_or_activation', 'data_migration', 'OS_enforced_sandbox',
                             'general_refactoring_ability', 'upstream_full_repository_integration'],
            'target_model_invocations': 0,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='new JSON file; existing files are never overwritten')
    args = parser.parse_args()
    result = run_lab()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output is not None:
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(text)
    print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
