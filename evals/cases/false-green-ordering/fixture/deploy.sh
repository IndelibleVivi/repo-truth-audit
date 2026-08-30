#!/usr/bin/env bash
set -eu

if [[ "${1:-}" == "--trace" ]]; then
  echo "REMOTE_WRITE"
  echo "ROLE_CHECK"
  exit 0
fi

remote_write() {
  : # synthetic fixture: no real remote effect
}

role_check() {
  [[ "$(cat /etc/faye-host-role)" == "release-primary" ]]
}

remote_write
role_check
