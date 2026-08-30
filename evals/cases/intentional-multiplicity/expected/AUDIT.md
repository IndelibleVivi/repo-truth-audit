# Evaluator reference — intentional multiplicity

Decision answer: ready to use the documented stable artifact selector.

This is intentional multiplicity. README pins installation with `--ref v1.0.0`;
`releases/stable.json` maps that selector to `releases/v1.0.0`. Development is
explicitly selected with `--channel development`, maps to `development/main`,
and is recorded under `Unreleased`. Each selected directory exists and carries
matching channel/version identity. `selector.py` rejects any unnamed channel,
rejects identity mismatch, and neither named route falls through to the other.

The audit reaches repository artifact identity only; it does not claim an
installed or running copy was observed. No additional traversal can change the
repository-level selection decision, so the result should stay short and clean.
