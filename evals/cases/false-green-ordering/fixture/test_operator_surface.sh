#!/usr/bin/env bash
set -eu

grep -q '/etc/faye-host-role' deploy.sh
grep -q 'ROLE_CHECK' deploy.sh
grep -q 'REMOTE_WRITE' deploy.sh
echo "operator surface: PASS"
