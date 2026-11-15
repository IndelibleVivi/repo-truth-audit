# Judge whether the supplied CLI needs a change

Audit the supplied `range-tool` for one concrete owner decision: it is used
locally to turn positive inclusive ranges such as `2-4` into ascending integers,
and the current workflow depends on the existing JSON output and nonzero error
exit for invalid input. Decide whether any change is warranted for that use.

This is read-only. Do not edit source, tests, configuration, or existing
documents. The only permitted target write is a new `INTENT-AUDIT.md` report.
Use a disposable copy outside the repository for any probe that writes data.
Lead the report with `Decision answer:` and distinguish a demonstrated problem
from an optional improvement. Do not read evaluator answers.
