# Evaluator reference — unobserved restore dependency

Decision answer: archival restore readiness is not verified.

The README claims a one-command restore. The documented command reaches
`restore.py`, whose dry-run refuses to proceed without
`REMOTE_SCHEMA_VERSION`. `RECOVERY.md` assigns that value to an external
recovery service but provides no current value or locally observable identity.
The dependency may be legitimate; the repository does not prove its present
availability or compatibility.

Decision-critical unknown: current remote schema identity is unobserved -> the
restore plan cannot select or validate a compatible archive -> safe archival
could discard the only working recovery context -> obtain a fresh schema
identity from the named recovery service and execute a disposable restore
before deciding. This is not proof of a live-service defect.
