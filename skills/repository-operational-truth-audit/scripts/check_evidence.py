#!/usr/bin/env python3
"""Bounded, read-only checks of cited file bytes, NOT an audit or repair gate.

Requires POSIX directory-relative no-follow reads. Unsupported platforms fail
closed. There are no subprocesses, Git calls, target imports, network calls, or
writes. Use a trusted installed copy, not a script supplied by the target repo.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterator

MAX_PACKET = 1_048_576
MAX_FILE = 4_194_304
MAX_TOTAL = 33_554_432
MAX_ANCHORS = 128
MAX_JSON_DEPTH = 64
SCHEMA = "rta-cited-bytes/1"
HEX = re.compile(r"[0-9a-f]{64}\Z")
ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,63}\Z")
ANCHOR_KEYS = {"id", "path", "sha256", "start_line", "end_line", "excerpt_sha256"}


class CheckError(ValueError):
    """Safe diagnostic: never contains raw target content or an absolute path."""


def secure_reads_supported() -> bool:
    return bool(
        os.name == "posix" and hasattr(os, "O_NOFOLLOW")
        and all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_CLOEXEC", "O_NONBLOCK"))
        and os.open in os.supports_dir_fd
    )


def path_parts(value: Any) -> list[str]:
    if not isinstance(value, str) or not value or len(value) > 1024:
        raise CheckError("invalid_relative_path")
    if "\\" in value or ":" in value or any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise CheckError("invalid_relative_path")
    parts = value.split("/")
    if any(p in {"", ".", ".."} for p in parts):
        raise CheckError("invalid_relative_path")
    return parts


@contextmanager
def root_descriptor(root: Path) -> Iterator[int]:
    if not secure_reads_supported():
        raise CheckError("secure_read_unavailable")
    try:
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError:
        raise CheckError("root_unavailable") from None
    try:
        yield fd
    finally:
        os.close(fd)


def read_fd(fd: int, limit: int) -> bytes:
    """Read regular, single-link files only; reject size/identity changes."""
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise CheckError("not_single_link_regular_file")
    if before.st_size > limit:
        raise CheckError("input_too_large")
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = os.read(fd, min(65536, limit + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise CheckError("input_too_large")
    after = os.fstat(fd)
    identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink,
                          s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if identity(before) != identity(after) or total != before.st_size:
        raise CheckError("file_changed_during_read")
    return b"".join(chunks)


def read_relative(root_fd: int, relative: str, limit: int = MAX_FILE) -> bytes:
    parts = path_parts(relative)
    parent = os.dup(root_fd)
    try:
        for component in parts[:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
                            | os.O_CLOEXEC, dir_fd=parent)
            os.close(parent)
            parent = child
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                     | os.O_CLOEXEC, dir_fd=parent)
        try:
            return read_fd(fd, limit)
        finally:
            os.close(fd)
    except OSError:
        raise CheckError("anchor_unavailable_or_unsafe") from None
    finally:
        os.close(parent)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excerpt(data: bytes, start: int, end: int) -> bytes:
    if type(start) is not int or type(end) is not int or start < 1 or end < start:
        raise CheckError("invalid_line_range")
    # Logical lines are LF-delimited. Preserve CRLF and final-newline bytes.
    pieces = data.split(b"\n")
    lines = [piece + b"\n" for piece in pieces[:-1]]
    if pieces[-1]:
        lines.append(pieces[-1])
    if end > len(lines):
        raise CheckError("line_range_out_of_bounds")
    return b"".join(lines[start - 1:end])


def anchor(root: Path, relative: str, start: int, end: int, ident: str) -> dict[str, Any]:
    if not isinstance(ident, str) or not ID.fullmatch(ident):
        raise CheckError("invalid_anchor_id")
    path_parts(relative)
    with root_descriptor(root) as fd:
        data = read_relative(fd, relative)
    return {"id": ident, "path": relative, "sha256": sha(data), "start_line": start,
            "end_line": end, "excerpt_sha256": sha(excerpt(data, start, end))}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CheckError("duplicate_json_key")
        result[key] = value
    return result


def reject_constant(_: str) -> None:
    raise CheckError("nonfinite_json_number")


def check_json_depth(data: bytes) -> None:
    """Bound nesting before decoding, independently of the host recursion limit."""
    depth = 0
    quoted = escaped = False
    for byte in data:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:  # backslash
                escaped = True
            elif byte == 34:  # quote
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (123, 91):  # { [
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise CheckError("json_nesting_too_deep")
        elif byte in (125, 93):  # } ]
            depth -= 1
    # Syntax, unmatched brackets and strings remain json.loads' responsibility.


def parse_packet(data: bytes) -> dict[str, Any]:
    if len(data) > MAX_PACKET:
        raise CheckError("packet_too_large")
    check_json_depth(data)
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=strict_object,
                           parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, CheckError):
            raise
        raise CheckError("invalid_json") from None
    if not isinstance(value, dict):
        raise CheckError("packet_must_be_object")
    return value


def validate_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    if set(packet) != {"schema", "anchors"} or packet["schema"] != SCHEMA:
        raise CheckError("invalid_packet_schema")
    anchors = packet["anchors"]
    if not isinstance(anchors, list) or not 1 <= len(anchors) <= MAX_ANCHORS:
        raise CheckError("invalid_anchor_count")
    ids: set[str] = set()
    for entry in anchors:
        if not isinstance(entry, dict) or set(entry) != ANCHOR_KEYS:
            raise CheckError("invalid_anchor_shape")
        ident = entry["id"]
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in ids:
            raise CheckError("invalid_or_duplicate_anchor_id")
        ids.add(ident)
        path_parts(entry["path"])
        for field in ("sha256", "excerpt_sha256"):
            if not isinstance(entry[field], str) or not HEX.fullmatch(entry[field]):
                raise CheckError("invalid_digest")
        a, b = entry["start_line"], entry["end_line"]
        if type(a) is not int or type(b) is not int or a < 1 or b < a:
            raise CheckError("invalid_line_range")
    return anchors


def check(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    entries = validate_shape(packet)
    total = 0
    with root_descriptor(root) as fd:
        for entry in entries:
            data = read_relative(fd, entry["path"], min(MAX_FILE, MAX_TOTAL - total))
            total += len(data)
            if sha(data) != entry["sha256"]:
                raise CheckError("cited_file_digest_mismatch")
            selected = excerpt(data, entry["start_line"], entry["end_line"])
            if sha(selected) != entry["excerpt_sha256"]:
                raise CheckError("cited_excerpt_digest_mismatch")
    return {
        "status": "matched", "anchors_checked": len(entries),
        "proof": "cited_file_bytes_only", "uncited_paths": "not_checked",
        "semantic_verification": "not_performed", "git_snapshot": "not_verified",
        "atomic_snapshot": "not_established", "execution_authorization": "none",
    }


def load_packet(path: Path) -> dict[str, Any]:
    # The packet's parent directory must be selected by the operator, outside
    # target-controlled scratch. Only the leaf is opened here, no-follow.
    if not secure_reads_supported():
        raise CheckError("secure_read_unavailable")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
        try:
            data = read_fd(fd, MAX_PACKET)
        finally:
            os.close(fd)
    except OSError:
        raise CheckError("packet_unavailable") from None
    return parse_packet(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    a = commands.add_parser("anchor", help="emit one byte anchor; no semantic verdict")
    a.add_argument("--root", type=Path, required=True)
    a.add_argument("--path", required=True)
    a.add_argument("--start-line", type=int, required=True)
    a.add_argument("--end-line", type=int, required=True)
    a.add_argument("--id", required=True)
    c = commands.add_parser("check", help="check a packet; does not authorize repair")
    c.add_argument("packet", type=Path)
    c.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = (anchor(args.root, args.path, args.start_line, args.end_line, args.id)
                  if args.command == "anchor" else check(args.root, load_packet(args.packet)))
    except CheckError as exc:
        print(json.dumps({"status": "failed", "error": str(exc),
                          "execution_authorization": "none"}), file=sys.stderr)
        return 2
    except OSError:
        print('{"status":"failed","error":"io_failure","execution_authorization":"none"}',
              file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
