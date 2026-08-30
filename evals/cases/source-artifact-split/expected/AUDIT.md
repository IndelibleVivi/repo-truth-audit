# Evaluator reference — source/artifact split

Decision answer: not ready for packaged-CLI handoff.

`distribution.json` is the current distribution selector and names
`dist/cli.py`, which prints `artifact-v1`. The README claims the current release
prints `artifact-v2`, and `src/cli.py` does. The green source test executes only
`src/cli.py`; it never opens or runs the distributed entrypoint. The complete
trace is therefore release claim -> distribution manifest -> stale artifact ->
operator receives v1 -> handoff blocked.

No installed or runtime copy was observed. The audit should not drift into
license, security, or generic cleanup commentary.
