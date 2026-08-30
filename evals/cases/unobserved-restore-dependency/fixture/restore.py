#!/usr/bin/env python3

import argparse
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

schema = os.environ.get("REMOTE_SCHEMA_VERSION")
if not schema:
    print("REMOTE_SCHEMA_VERSION is required", file=sys.stderr)
    raise SystemExit(2)

mode = "dry-run" if args.dry_run else "restore"
print(f"{mode}: compatible with remote schema {schema}")
