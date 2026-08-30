#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--channel", required=True, choices=("stable", "development"))
parser.add_argument("--ref")
args = parser.parse_args()
root = Path(__file__).resolve().parent

if args.channel == "stable":
    payload = json.loads((root / "releases/stable.json").read_text(encoding="utf-8"))
    if args.ref is not None and args.ref != payload["install_ref"]:
        raise SystemExit("requested ref is not the selected stable release")
    artifact_root = root / payload["artifact_dir"]
    artifact = json.loads((artifact_root / "artifact.json").read_text(encoding="utf-8"))
    if artifact != {"channel": "stable", "version": payload["install_ref"]}:
        raise SystemExit("stable artifact identity does not match its selector")
    print(payload["artifact_dir"])
else:
    if args.ref is not None:
        raise SystemExit("development channel does not accept a release ref")
    payload = json.loads((root / "development/current.json").read_text(encoding="utf-8"))
    workspace_root = root / payload["workspace"]
    workspace = json.loads((workspace_root / "workspace.json").read_text(encoding="utf-8"))
    if workspace != {"branch": payload["channel"], "channel": "development"}:
        raise SystemExit("development workspace identity does not match its selector")
    print(payload["workspace"])
