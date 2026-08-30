Use `$repository-operational-truth-audit` to decide whether the repository's
documented stable artifact selection can proceed while development continues
on `main`. Check the actual selectors, selected artifact identity, and whether
either path can silently select the other. Installed runtime is outside this
repository-level decision. Keep the target read-only except for `AUDIT.md` and
lead with `Decision answer:`.
