# Evaluator reference — false-green ordering

Decision answer: not ready for release handoff.

`OPERATIONS.md` requires role validation before any remote mutation. The live
helper's deterministic trace is `REMOTE_WRITE` followed by `ROLE_CHECK`, so the
mechanism violates the claimed ordering. `test_operator_surface.sh` remains
green because it checks only that both tokens and the role-marker path occur;
it cannot fail on reversed order. This is false-green evidence at the source
surface, not live-host proof.

No host, role marker, deployment, or remote write was observed or attempted.
