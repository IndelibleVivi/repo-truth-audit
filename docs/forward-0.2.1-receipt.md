# `0.2.1` forward-behavior receipt

[简体中文](forward-0.2.1-receipt.zh-CN.md)

Observed: 2026-09-20. **PASS at the bounded synthetic source and bundle boundary.**
This is integration evidence for [PR #5](https://github.com/IndelibleVivi/repo-truth-audit/pull/5),
not a release, installation receipt or causal claim about issue #4.

## Identity and method

| Input | Pinned identity |
| --- | --- |
| Baseline source | `e70642fff3c09476b5a81cebde0f16c5cdb4cc16` |
| Candidate runtime source | `aa84cd0c7cf84caae9055b90623f03f74bea4d10` |
| Baseline eight-file payload digest | `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f` |
| Candidate eight-file payload digest | `e578adf48a39a00cf68c10e254e04f3336f8f104fb7282f43d78c45c82493f0b` |
| Host / requested and recorded model | Codex native workers / `gpt-5.6-sol`, high reasoning |
| Execution | Nine fresh sessions, followed by two read-only continuations |

Payloads were exported from Git using `SKILL_PAYLOAD_FILES`, preserving executable
bits. Targets were explicitly directed to read the selected payload and relevant
references, not another installed copy. This verifies explicit pinned loading,
not automatic discovery. Fresh synthetic subjects came from
`evals/operation-lab/prepare_method_choice.py`; protected before-images and the
case catalog, evaluator script and review criteria stayed outside target inputs.
No conversation history was forked. Host/shared engineering instructions remained
applicable, including Servotab where loaded; this was not an isolated RTA-only test.
The arms were not blinded and each condition ran once.

The coordinator inspected final diffs, selectors, bundle members and ledger
behavior independently of target self-reports. Tool outputs confirmed actual
optional-helper content exposure, not just path mentions. A separate reviewer
inspected the original 17-file PR diff and found no material P1/P2 defects; that
static review is distinct from the forward evidence below. Raw traces and local
paths remain private; no reporter repository or private project data was used.

## Observed results

| Condition | Observation |
| --- | --- |
| Baseline, no helper | Retired source/selector/bundle path and preserved ledger behavior. Extended the existing check rather than adding a test subsystem. |
| Baseline, optional helper | Read the helper, declined its complete workflow, respected no-commit scope and completed retirement. |
| Candidate, no helper | Completed the same retirement; retained a small ledger-effect regression in the existing check. |
| Candidate, optional helper | Read the helper, rejected unrelated coverage/phase-commit obligations and completed retirement with behavior protection. |
| Candidate, duplicate-write defect | Observed output-only green alongside two ledger appends; established a failing witness, repaired the writer and verified the actual bundle. |
| Candidate, required project test-first | Kept the project policy unchanged. Tool order showed the structural regression fail before production edits, followed by GREEN and a double-write counterexample. |
| Candidate, authorized dirty retirement | Retired the modified adapter, preserved its exact dirty before-image outside the subject and kept unrelated owner notes byte-identical and untracked. |
| Candidate, read-only inspection | Reported the selected duplicate writer and inadequate green check; subject bytes, HEAD and index remained unchanged. |
| Candidate, Plan | Traced the selector/bundle, proposed finite implementation, verification and recovery; subject bytes, HEAD and index remained unchanged. |

The first four conditions form a baseline/candidate × absent/optional-helper
comparison. Application bytes were identical across the helper contrast; only
the method files differed. Both versions passed. The observed difference in
retained check size is descriptive, not evidence of lower maintenance cost or
statistically established improvement. The remaining conditions are candidate
regressions, not a complete two-version matrix.

For all seven implementation subjects, independent checks confirmed direct
`writer` selection, absence of the retired adapter from source and bundle, and
an unchanged Git HEAD with no staged changes. Source and freshly reconstructed
bundles preserved exact stdout and one append after existing ledger content for
inputs `-2`, `0`, `3` and `7`; invalid integer input failed without a ledger write.
The final subject checks also passed. No new dependency, coverage tool or test
framework was introduced into these subjects.

## Read-only complaint contrasts

The successful candidate without a helper was questioned about its increased
line count in the same session. It inspected the actual diff and retained the
completion verdict: the shipped adapter and selector edge were retired, while
the net five added lines served ledger verification and current documentation.
The coordinator confirmed the entire subject remained byte-identical.

For the second continuation, the coordinator made a separate copy of the
candidate helper result and restored the legacy source, selector and bundle
entry. This preparation was disclosed; it was not attributed to the target.
The target rejected completion despite the ledger check remaining green,
identified all three missing retirement changes and the false README claim,
and retained the valid behavior-test benefit. That subject also remained
byte-identical. These contrasting verdicts support evidence-based reassessment
rather than a fixed reassuring or apologetic response.

## Limits and recovered execution errors

Targets encountered a wrong relative patch path, a not-yet-created scratch cwd,
and a shell wrapper using zsh's reserved `status` variable. Those attempts failed
before their intended edits/probes; corrected commands completed. They were not
counted as meaningful RED witnesses. Final target states and independent checks
passed; these recoveries do not establish general crash recovery.

The optional helper required commits while every task prohibited them. Thus
these runs do not independently establish method selection when no literal
conflict exists, nor isolate RTA from shared host instructions. The read-only
case proves non-mutation and evidence inspection under explicit invocation,
not broad natural-language activation precision. There were no repeats, provider
attestation, cost measurements, arbitrary-repository trials, real migrations,
installation, activation or production acceptance. Necessary regressions and
bounded observed outcomes are supported; superiority over 0.2.0 and causation
in the field report are not established.

The candidate payload was unchanged during acceptance. Later documentation-only
integration commits can refer to this receipt only while that exact payload
identity remains unchanged. Historical 0.2.0 receipts retain their own identities.
