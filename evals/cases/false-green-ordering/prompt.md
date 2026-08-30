Use `$repository-operational-truth-audit` to decide whether the current operator
surface is ready for release handoff. The runbook's pre-write role invariant is
decision-critical. Check what the green operator gate actually proves. Do not
perform any remote action. Keep the target read-only except for `AUDIT.md`, and
lead the report with `Decision answer:`.
