# Setup recovery and preserved first cohort

[简体中文](setup-recovery.zh-CN.md)

The first cohort used frozen commit `03e37060f5da720aa318d9021c03a73809fe5404`.
Independent review without campaign access reproduced three evaluator/fixture defects:

- isolated Python removed the selected application's own import directory, rejecting a legitimate declared helper;
- text newline normalization accepted a protected owner file changed from LF to CRLF;
- both generated range self-tests referenced `os.environ` without importing `os`.

All eleven experiment tests and 169 repository tests had passed. Those checks did
not establish the missing guarantees. The ordinary helper-import, exact byte
comparison and supplied-self-test counterexamples were checked independently.

The coordinator stopped this cohort for setup validity, before reading final
reports or product outcomes. All twelve slots had launched by the successful
stop: nine host processes finished, one timed out and two were interrupted.
These are host statuses, not task verdicts. All twelve outcomes remain unjudged
in [aborted observations](aborted-observations.json), outside comparable costs.
Raw reports, subjects, logs, original inputs and independent reproductions remain
private and are not overwritten. No Agent success-rate conclusion uses this cohort.

The corrected consumer retains `-I` while inserting only the selected entry's
parent for local imports. Protected Task/owner/Cedar inputs compare bytes, and
both supplied test scripts import their dependency. Fourteen focused tests and
independent before/after checks accept legal single-file/helper bundles, reject
CRLF owner mutation and run both fresh supplied tests successfully.

A separate [recovery registration](recovery-preregistration.json) uses seed
`consumer-first-2026-11-14-setup-repair-v2`, corrected fresh subjects and the same
three treatments. [Recovery settings](recovery-execution-settings.json) freeze
its inputs and controls. It permits at most twelve new fresh Agent sessions,
180 seconds each, three concurrent, no retries; the two cohorts total at most
24 subject sessions. Existing native ChatGPT login is used without new paid
credentials. An Agent session can contain multiple model API requests.

Only first-cohort host statuses, not reports or product verdicts, were read before
this recovery registration. The independent reviewer had no campaign access.
The recovery is a setup repair with different initial objects; cohorts must not
be pooled. Human review remains voluntary and untimed; no productivity gain is
inferred from repaired instruments or green tests.
