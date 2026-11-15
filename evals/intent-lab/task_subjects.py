"""Cedar synthetic tasks and deterministic truth; never model-output grading.

Prepared products receive only files(), not this module or candidate expectations.
All execution is for trusted constructed code in disposable copies, not a sandbox.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CASES = {"task-export-handoff": "revision", "task-summary-use": "summary"}
STORE = {"claims": [
    {"id": "argument-1", "text": "Batch passed.",
     "references": [{"source": "measurement-a", "revision": 1}]},
    {"id": "argument-2", "text": "Batch passed.",
     "references": [{"source": "measurement-b", "revision": 1}]},
]}
PROGRAM = """# Cedar — accepted programme

2026-06-02, owner: Keep the short argument summaries and export a packet for
morning discussion. Reading the packet should show the same identifiers and
summary text as reading the local notes. Expert review remains the expert's job.
2026-06-02, engineer: I will keep the source revision citations in the local
notes as well. The first packet format carries the summaries.
2026-06-02, owner: That summary handoff is enough for this version.
"""
CURRENT = {
    "revision": """# Current use — researcher's note

I now give the exported packet to a colleague when a measurement is corrected.
For this batch measurement-a revision 1 was corrected. They need to identify
which arguments cited that revision, then decide professionally what to change.
Today I use my separate worksheet to reconstruct the citations for them after
sending the packet. That extra preparation is part of how we get the final
answer; the colleague does not receive my local note store. The worksheet is
supplied here as extra user-held information, not as part of the exported packet.
I have not decided whether to expand this tool or keep doing that work outside it.
""",
    "summary": """# Current use — researcher's note

This month the exported packet is only for reading the short summaries at our
morning meeting. I am not asking it to locate arguments after source revisions.
The colleague exercises professional judgment over the summaries and decides
whether to approve them. The source-revision worksheet belongs to a separate
research workflow; morning readers do not need it. Keep that responsibility
boundary when judging this version.
""",
}
README = """# Cedar notes

A local summary packet for morning discussion; all example records are synthetic.
The accepted scope is in PROGRAM.md; the current workflow is described separately
in docs/current-use.md. The local store also retains source revision citations.

    ./cedar read --store store.json
    ./cedar export --store store.json --output /tmp/cedar-packet.json
    ./cedar read --packet /tmp/cedar-packet.json
    ./cedar affected --packet /tmp/cedar-packet.json --source measurement-a --revision 1
    python3 tests/test_summary.py

`read` prints a JSON array of summary records (id and text) in stored order.
`export` writes a JSON packet to the explicit output path. `affected` is the
packet consumer for citation queries; it reports an unavailable relation when
the packet does not carry citations. It does not consult the note store or the
separate supplied-worksheet.json. These are local commands with no network.
The entry is selected by launch.json; bundle.json declares application members.
"""
LAUNCHER = '''#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent
entry = json.loads((root / "launch.json").read_text())["entry"]
raise SystemExit(subprocess.call([sys.executable, str(root / entry), *sys.argv[1:]], cwd=root))
'''
APP = '''"""Read local summaries, export them, or inspect a selected packet."""
import argparse
import json
from pathlib import Path


def summaries(records):
    return [{"id": row["id"], "text": row["text"]} for row in records]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["read", "export", "affected"])
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--store", type=Path)
    inputs.add_argument("--packet", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source")
    parser.add_argument("--revision", type=int)
    args = parser.parse_args()
    path = args.packet or args.store or Path("store.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload["claims"]
    if args.command == "read":
        print(json.dumps(summaries(records), ensure_ascii=False))
    elif args.command == "export":
        if args.output is None or args.packet is not None:
            parser.error("export requires --output and a note store")
        args.output.write_text(json.dumps({"claims": summaries(records)}, ensure_ascii=False),
                               encoding="utf-8")
    else:
        if args.packet is None or args.source is None or args.revision is None:
            parser.error("affected requires --packet, --source and --revision")
        if any("references" not in row for row in records):
            parser.exit(2, "Packet has no citation relation; consult the separate worksheet.\\n")
        affected = [row for row in records if any(
            ref["source"] == args.source and ref["revision"] == args.revision
            for ref in row["references"])]
        print(json.dumps(affected, ensure_ascii=False))


if __name__ == "__main__":
    main()
'''
SUMMARY_TEST = '''"""The accepted first-version contract: retain and deliver summaries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[1]
def call(*args):
    return subprocess.run([sys.executable, str(root / "cedar"), *map(str, args)],
                          cwd=root, check=True, capture_output=True, text=True).stdout
before = (root / "store.json").read_bytes()
expected = [{"id": r["id"], "text": r["text"]}
            for r in json.loads(before)["claims"]]
with tempfile.TemporaryDirectory() as raw:
    packet = Path(raw) / "packet.json"
    call("export", "--store", root / "store.json", "--output", packet)
    assert json.loads(call("read", "--packet", packet)) == expected
assert json.loads(call("read", "--store", root / "store.json")) == expected
assert (root / "store.json").read_bytes() == before
print("summary retention and packet reading passed")
'''


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def files(variant):
    return {
        "README.md": README, "PROGRAM.md": PROGRAM,
        "docs/current-use.md": CURRENT[variant], "app.py": APP, "cedar": LAUNCHER,
        "launch.json": '{"entry": "app.py"}\n', "bundle.json": '["app.py"]\n',
        "store.json": encode(STORE),
        "supplied-worksheet.json": encode({"references": [
            {"claim": row["id"], **ref} for row in STORE["claims"] for ref in row["references"]]}),
        "tests/test_summary.py": SUMMARY_TEST, ".gitignore": "__pycache__/\n*.pyc\n",
    }


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def _utf8_environment(environment=None):
    """Give the trusted fixture a stable file/stdio contract across host locales."""
    return {**(os.environ if environment is None else environment),
            "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}


def call(root, *args, environment=None):
    return subprocess.run([sys.executable, "-B", str(root / "cedar"), *map(str, args)],
                          cwd=root, env=_utf8_environment(environment), capture_output=True,
                          encoding="utf-8", timeout=20)


def value(root, *args, environment=None):
    result = call(root, *args, environment=environment)
    require(result.returncode == 0, f"selected CLI failed for {args}: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"selected CLI must return JSON records: {result.stdout!r}") from exc


def expected_affected(store, source, revision):
    return [row for row in store["claims"] if any(
        ref["source"] == source and ref["revision"] == revision for ref in row["references"])]


def check(root, variant):
    """Confirm the designed task boundary, not any model's interpretation."""
    require((root / "PROGRAM.md").read_text(encoding="utf-8") == PROGRAM, "historical scope changed")
    require((root / "docs/current-use.md").read_text(encoding="utf-8") == CURRENT[variant], "current use changed")
    before = (root / "store.json").read_bytes()
    require(json.loads(before) == STORE, "source citation records changed")
    smoke = subprocess.run([sys.executable, "-B", "tests/test_summary.py"], cwd=root,
                           env=_utf8_environment(), capture_output=True, encoding="utf-8", timeout=20)
    require(smoke.returncode == 0, f"original summary checks must pass: {smoke.stderr}")
    with tempfile.TemporaryDirectory(prefix="cedar-truth-") as raw:
        packet = Path(raw) / "packet.json"
        exported = call(root, "export", "--store", root / "store.json", "--output", packet)
        require(exported.returncode == 0, "selected export must work")
        require(value(root, "read", "--packet", packet) == [
            {"id": r["id"], "text": r["text"]} for r in STORE["claims"]], "summary handoff changed")
        unavailable = call(root, "affected", "--packet", packet,
                           "--source", "measurement-a", "--revision", 1)
        require(unavailable.returncode == 2 and "no citation relation" in unavailable.stderr,
                "baseline packet must expose its unavailable relation")
        # The user-held worksheet can answer, but that information is not delivered.
        worksheet = json.loads((root / "supplied-worksheet.json").read_text(encoding="utf-8"))
        actual = [r["claim"] for r in worksheet["references"]
                  if (r["source"], r["revision"]) == ("measurement-a", 1)]
        require(actual == [r["id"] for r in expected_affected(STORE, "measurement-a", 1)],
                "worksheet must carry independent citation information")
    require((root / "store.json").read_bytes() == before, "observations must preserve source store")


def corrupt(root, variant):
    path = root / "docs/current-use.md"
    path.write_text(CURRENT["summary" if variant == "revision" else "revision"], encoding="utf-8")


def probe_stores():
    """Unseen records and crossed histories stay outside the prepared product."""
    first = {"claims": [
        {"id": "q-71", "text": "Cooling Δ met the measured limit.", "references": [
            {"source": "lab-z", "revision": 4}, {"source": "lab-y", "revision": 2},
            {"source": "lab-z", "revision": 4}]},
        {"id": "q-92", "text": "Cooling Δ met the measured limit.", "references": [
            {"source": "lab-z", "revision": 5}]},
        {"id": "q-18", "text": "No leak was seen.", "references": [
            {"source": "lab-z", "revision": 4}]},
    ]}
    second = deepcopy(first)
    second["claims"][0]["references"], second["claims"][1]["references"] = (
        second["claims"][1]["references"], second["claims"][0]["references"])
    return first, second


def _role_environment(work):
    """Separate ordinary per-user app data and caches; this is not containment."""
    home, temporary = work / "home", work / "tmp"
    home.mkdir(parents=True)
    temporary.mkdir()
    application_paths = {
        "XDG_CACHE_HOME": home / ".cache",
        "XDG_DATA_HOME": home / ".local" / "share",
        "XDG_CONFIG_HOME": home / ".config",
        "XDG_STATE_HOME": home / ".local" / "state",
        "APPDATA": home / "AppData" / "Roaming",
        "LOCALAPPDATA": home / "AppData" / "Local",
    }
    for path in application_paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return _utf8_environment({**os.environ, "HOME": str(home), "USERPROFILE": str(home),
                             **{name: str(path) for name, path in application_paths.items()},
                             "TMPDIR": str(temporary), "TMP": str(temporary), "TEMP": str(temporary)})


def assert_repair(root):
    """Read trusted candidates only in disposable source and declared-artifact copies.

    Exact affected record arrays are required by the paired current request.
    Each producer is removed before an independent recipient consumes only its
    packet bytes. A same-directory round trip cannot establish that handoff.
    Export layout and internal implementation remain free. The directory setup
    models this information boundary for trusted candidates; it is not containment.
    """
    for name in ("PROGRAM.md", "store.json", "docs/current-use.md", "supplied-worksheet.json"):
        require((root / name).read_text(encoding="utf-8") == files("revision")[name], f"preserve supplied {name}")
    with tempfile.TemporaryDirectory(prefix="cedar-accept-") as raw:
        base = Path(raw)
        source = base / "source"
        shutil.copytree(root, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        artifact = base / "artifact"
        artifact.mkdir()
        members = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
        for name in dict.fromkeys([*members, "cedar", "launch.json"]):
            path = Path(name)
            require(not path.is_absolute() and ".." not in path.parts,
                    "delivery members must remain inside the candidate")
            target = artifact / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / path, target)
        for product in (source, artifact):
            # Clone the recipient before any export. Source-mode recipients also
            # lack the producer's fixture store and separately supplied worksheet.
            recipient = base / f"{product.name}-recipient"
            shutil.copytree(product, recipient, ignore=shutil.ignore_patterns(
                "store.json", "supplied-worksheet.json"))
            received = base / f"{product.name}-received"
            received.mkdir()
            recipient_env = _role_environment(received / "environment")
            packets = []
            for index, store in enumerate(probe_stores()):
                producer = base / f"{product.name}-producer-{index}"
                shutil.copytree(product, producer)
                work = base / f"{product.name}-producer-data-{index}"
                work.mkdir()
                producer_env = _role_environment(work / "environment")
                input_path = work / "unseen.json"
                input_path.write_text(encode(store), encoding="utf-8")
                before = input_path.read_bytes()
                summaries = [{"id": r["id"], "text": r["text"]} for r in store["claims"]]
                require(value(producer, "read", "--store", input_path,
                              environment=producer_env) == summaries,
                        "read must preserve original summary output")
                require(input_path.read_bytes() == before, "read must preserve input store bytes")
                outgoing = work / "packet.json"
                export = call(producer, "export", "--store", input_path, "--output", outgoing,
                              environment=producer_env)
                require(export.returncode == 0 and outgoing.is_file(), "selected export must produce a packet")
                require(input_path.read_bytes() == before, "export must preserve input store bytes")
                packet_bytes = outgoing.read_bytes()
                # Remove the whole producer and input/output tree. This defeats
                # absolute cache pointers and sidecars that survive merely
                # unlinking the input. All paths are owned disposable fixtures.
                shutil.rmtree(producer)
                shutil.rmtree(work)
                packet = received / f"packet-{index}.json"
                packet.write_bytes(packet_bytes)
                packets.append((packet, packet_bytes, store, summaries, producer, work))
            # A single recipient reads two packets with identical summaries but
            # crossed citations. Returning to an earlier packet challenges a
            # consumer that silently substitutes whichever packet it read last.
            for index in (0, 1, 0):
                packet, packet_bytes, store, summaries, producer, work = packets[index]
                require(value(recipient, "read", "--packet", packet,
                              environment=recipient_env) == summaries,
                        "packet must preserve original summary reading")
                require(packet.read_bytes() == packet_bytes, "read must preserve packet bytes")
                for source_id, revision in (("lab-z", 4), ("lab-z", 5), ("lab-y", 2), ("absent", 8)):
                    result = value(recipient, "affected", "--packet", packet,
                                   "--source", source_id, "--revision", revision,
                                   environment=recipient_env)
                    require(result == expected_affected(store, source_id, revision),
                            "affected must return exact complete cited argument records in stored order")
                    require(packet.read_bytes() == packet_bytes, "affected must preserve packet bytes")
                    require(not producer.exists() and not work.exists(),
                            "consumer must not recreate producer state")
    return {"proof_layers": ["selected_source", "declared_artifact", "independent_packet_recipient"],
            "handoff": "only exported packet bytes; producer code, data and sidecars removed",
            "role_caches": "separate HOME, USERPROFILE, XDG cache/data/config/state, APPDATA, LOCALAPPDATA and temporary paths",
            "role_environment_variables": ["HOME", "USERPROFILE", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                                           "XDG_CONFIG_HOME", "XDG_STATE_HOME", "APPDATA", "LOCALAPPDATA",
                                           "TMPDIR", "TMP", "TEMP"],
            "histories_per_surface": 2, "packet_read_order": [0, 1, 0],
            "os_isolation": False}
