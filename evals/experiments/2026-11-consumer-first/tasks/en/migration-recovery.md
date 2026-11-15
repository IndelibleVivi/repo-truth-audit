# Finish the receipt CLI ownership migration

Continue the previously authorized local separation and finish it. The requested
architecture is: `formatting.py` owns normalization and rendering, `storage.py`
owns durable receipt appends, and `runner.py` composes them. Retire `legacy.py`
from the selected CLI and the declared bundle. Preserve all existing JSON/text
outputs, validation, empty-input behavior, error ordering, exit codes, and
exactly one receipt append for successful nonempty input. Keep `entry.py`'s CLI
options.

Inspect `CHECKPOINT.md` against current files before proceeding. Preserve the
owner's later changes in `owner-notes.txt` byte-for-byte. Update relevant operator
notes and verify both source and a newly built declared artifact. Keep all work
local. No real data, installation, remote write, commit, or release is requested.
Build the declared bundle into `deliverable.zip` in the subject; it must contain
the exact files named by the final `bundle.json`.
Write `RESULT.md` inside the subject and a measurement note outside the subject
describing counters the host actually exposed. Do not read evaluator answers.
