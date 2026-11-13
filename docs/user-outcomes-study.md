# Where engineering fails its user — research and implementation

[简体中文](user-outcomes-study.zh-CN.md)

Observed: 2026-11-13. This is an unreleased research branch, based on main
`9fd099b6c9e88be2d7c809b021add51a5c8d6b8f`. The public `v0.3.0` release,
its installation pin and `VERSION=0.3.0` remain unchanged. The candidate is the
same nine-file Skill payload, digest
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`.

## Decision

The most concrete improvement is a repaired evaluator: eight implementations
that silently depended on the exporting machine passed the previous Cedar
repair gate. The new gate rejects all eight while accepting genuine portable
packets. Actual compiler, child-process and cross-process consumer probes then
showed how to apply the same reasoning beyond JSON handoffs.

The natural Agent experiment has a different purpose. Four matched tasks compare
no RTA with explicit use of the frozen candidate. They test typed-package repair,
packet repair, a valid summary-only workflow and continuation of a partial
migration. Their independent results and cost provenance are in the
[experiment receipt](../evals/experiments/2026-11-user-outcomes/README.md).
This small, selected experiment does not establish a productivity gain. A stronger
oracle is a useful research result even when both Agents already solve the task.

The product remains a finite intervention for a concrete decision or change.
There is no repository score, new model runner, mandatory audit stage, installed
evaluation dependency or automatic host integration.

## Local continuation — 2026-11-14

The research branch resumed at `89e3ec6ca668233925b45b3a5d215ce572a86df2`,
with no uncommitted owner edits. The original 147-test baseline and named
repository gates passed locally. The original remote matrix remains evidence
for its own commits rather than this continuation.

Three explicit native Codex 0.159.1 tasks closed the previously unobserved
Audit/Plan/Operate smoke boundary. Completed tool traces read the exact project
Skill; Audit and Plan preserved their targets. Operate repaired the selected
distribution and passed a manifest-only consumer, with a stale-artifact negative
control. Discovery and a transient disable override also passed without model
calls. This supports the existing installer default on this build, not universal
host support or a causal benefit. See [host evidence](host-compatibility.md).

A [new installed-package experiment](../evals/field/README.md) uses pinned PyPA
sampleproject source and real pip wheel/editable installations in disposable
environments. It distinguishes source-only completion from actual installed
selection and retains a frozen regular wheel after a later owner edit as a valid
neighbor. The eight expected readings passed. This is a constructed deployment
scenario, not a discovered upstream defect. It exposed no gap requiring another
canonical Skill rule.

Review of the offline comparator found that a supposedly `without-skill` arm
could record loaded exposure and still produce a measured delta. The repair
retains such runs but excludes them in either comparison direction; independent
review reproduced the reverse-direction hole in the first patch. Explicit
comparisons of two loaded treatments remain supported. The original four task
pairs retain their verdicts. A stronger comparator, successful host smoke and
installed-package matrix do not establish a new productivity result.

The finite shorter-instruction follow-up is now closed at 24 launched subject
sessions, including two invalidated cohorts. Setup corrections and a common
prompt scope error are retained rather than counted as model failures. The final
ordinary-repair pair succeeded in both arms; full and short migration arms each
reached a consumer-verified checkpoint without the required report before the
180-second cap. This does not resolve the original balanced comparison or show
review/coordination costs are repaid. See [the separated receipts and decision](../evals/experiments/2026-11-consumer-first/results.md).
Keep the canonical method unchanged; the short instruction remains an
experimental comparison, not a second installable product. The next useful
question is still whether either instruction improves a difficult completed
outcome enough to offset measured owner work.

## Starting state and retained contract

The published release at `6de6dae92f17efbef3cf8ad4e9e98eb6bdd5a61b` already
reconstructs adopted intent and separates source, artifact, installation, runtime
and owner acceptance. Unreleased main had added concrete task-effectiveness
questions and Cedar's revision-versus-summary contrast. Its 128 repository tests
passed before this work. The [earlier receipt](task-effectiveness-followup.md)
remains historical evidence; it is not rewritten as stronger evidence from this round.

Audit is read-only. Plan defines a finite outcome without target edits. Operate
uses the host's real tools and authority to complete the accepted outcome, with
Behavior, Structure, Delivery and Usefulness checked where applicable. Historical
intent requires adoption and scope evidence; a presently impossible task can be
shown directly without inventing a historical promise. Deliberate professional
judgment, valid simpler uses and compatibility remain legitimate.

No architecture region or edge changed in this round. The existing seven-region,
31-node, 46-edge model still describes the method. The change makes several of
its evidence edges executable and challenges the evaluator itself.

## Case selection and evidence classes

These are purposively selected mechanisms, not a random sample of repositories.
Historical issues help identify cases, so their reproduction is not blind defect
discovery. Upstream repairs and local experimental mutations are labeled separately.

| Case | Language and boundary | Actual observation | Research use |
| --- | --- | --- | --- |
| Cedar | Synthetic Python CLI; producer, packet, recipient | Previous gate accepts cache-dependent repairs; new independent recipient rejects them | Repair an RTA defect; test task-dependent information sufficiency |
| python-dotenv | External Python CLI; option, interpolation, inherited environment, child process | Old `--no-override` preserves one value but derives another from the losing source | Policy propagation and valid opposite-mode control |
| mitt | External TypeScript library; source, published declarations, compiler, runtime | Runtime supports `off('*')`; published declaration blocks a typed user | Admission gate, source-only false repair, semantic preservation |
| Codex Worker Routing | Public owner repository; ACP process, durable activity, separate status CLI, host UI | Old source lacks live progress; repaired source reaches status CLI before final output | Distinguish producer repair from downstream host adoption |
| Viper | External Go configuration library; lazy lookup, key enumeration, feature selection, decoded struct | Default decoding omits environment-only keys; supported and experimental paths work | Post-freeze transfer; reconcile compatibility intent and reject a stale snapshot workaround |
| Partial receipt-CLI migration | Synthetic Python; checkpoint, selected module, bundle, owner edits | Fresh Agents continue from a misleading completion label | Continuation and an over-strict reused evaluator |

The synthetic cases carry no private conversation data. Real repository clones
remain observation inputs. All mutations and package copies are disposable;
nothing is submitted to those upstream projects. Fresh agents receive a task and
subject, with evaluator answers withheld. Their files share the host filesystem:
directory instructions provide scope, not an OS security boundary.

## Cycle 1 — audit the repair oracle

### Failure

Cedar's accepted revision-review task needs each affected claim's complete record,
source and revision relations, original order and no duplicate answers. The
summary-only task needs only ordered identifiers and text. Both reserve judgment
about the claims for a professional reader.

The previous repair checker exported and queried in a producer context. Removing
`store.json` still left many channels available. We constructed eight working
local round trips: a relative producer cache, an absolute source-directory cache,
a packet sidecar, a HOME cache, a temporary cache, a pointer embedded in the
packet, an input-sidecar pointer, and an artifact missing necessary configuration
but recovering from a producer cache. Every one passed the old repair checker.

These are executable counterexamples, not string matches for suspicious code.
Each cache variant first demonstrates a successful local export/read/affected
cycle. It then faces the independent recipient. This avoids counting syntax or
setup failures as proof that the oracle detects the intended mistake.

### Repair

The checker now prepares recipients before export. Producer and recipient child
processes receive separate HOME, profile, cache and temporary directories. After
export, the disposable producer tree and input/output directory are removed.
Only the promised packet bytes cross into the recipient. Both source and the
declared reconstructed bundle are checked.

Two histories have identical displayed summaries but different citation
relations. The same recipient consumes them in order 0 → 1 → 0. The expected
full records come from evaluator-owned inputs; reads must not mutate the packet
or source store. This catches constant answers, leaked previous results and a
cache shared between source and artifact runs.

The new gate rejects all eight previously accepted cache repairs. Its full
self-challenge at that stage has twelve candidates: two valid encodings accepted and ten
negative candidates rejected. One negative works from source and fails only in
the declared artifact, preserving the reason to check both layers.

This is process-and-resource separation within a disposable experiment. It is
not a network sandbox, hostile-code isolation, a proof against all channels, or
a general demand for offline operation. If an accepted product retains an online
service, that service belongs in the recipient contract and must be tested there.

### Information sufficiency

A small formal test helps decide whether more implementation can rescue a handoff.
Let `s` be product state, `h(s)` everything the recipient is entitled to receive
or query, and `q(s)` the required answer. An exact recipient function `g` can
exist only if:

`h(s1) = h(s2)  ⇒  q(s1) = q(s2)`.

Otherwise `g` receives the same input and would have to return two different
answers. Conversely, on reachable handoffs this condition permits defining `g`
by the answer shared by each equivalence class. It establishes information
sufficiency, not an efficient implementation, interface usability or accepted
product intent.

Cedar's identical-summary/different-citation pair violates this condition for
revision review. It satisfies the condition for the summary meeting. The same
export format can therefore be adequate for one accepted job and inadequate for
another. Adding citation machinery to the summary-only product would require a
new reason; the presence of a richer imaginable task supplies none.

## Cycle 2 — real consumers challenge local success

### python-dotenv: a late filter cannot repair earlier interpretation

The pinned old source is `a00cb2eed0704cd6d2071b2004c37e95ccc86ee5`; the
upstream repair is `e0310e5bb3f2b701b11bbc007ca0c82c1bd56f38`.
The [issue](https://github.com/theskumar/python-dotenv/issues/697) and
[merged repair](https://github.com/theskumar/python-dotenv/pull/698) define the
actual task and historical provenance.

Given an inherited base of `environment` and file values `BASE=file` and
`DERIVED=${BASE}/suffix`, the old CLI child receives `environment` alongside
`file/suffix` under `--no-override`. Every process exits successfully. The API
`load_dotenv(override=False)` already handles this correctly; the core `main.py`
bytes are identical across the selected before/after revisions. The defect is
the selected CLI's propagation of the policy into interpolation.

Three child-process observations distinguish the repairs: inherited nonempty and
empty values under `--no-override`, and the valid opposite `--override` mode.

| Variant | Nonempty no-override | Empty no-override | Override |
| --- | --- | --- | --- |
| Historical old CLI | Fail | Fail | Pass |
| Upstream repaired CLI | Pass | Pass | Pass |
| Change an unselected constructor default | Fail | Fail | Pass |
| Force environment precedence globally | Pass | Pass | Fail |
| Drop the final precedence filter | Fail | Fail | Pass |
| Add a misleading README claim | Fail | Fail | Pass |

The matrix plus the working API control gives nineteen process observations.
The probe exits nonzero if the expected discrimination changes or any process
fails to execute. The lesson is specific: final selection cannot undo an earlier
interpretation made under the wrong policy. Trace a mode through every stage
where it affects values; preserve the supported opposite mode.

### mitt: the type declaration is part of the usable product

Source main is `6b41670516ed8e8b738612f60491995470aa63b3`; tag `3.0.1` is
`b240473b5707857ba2c6a8e6d707c28d1e39da49`. The selected source, package
metadata and README match across these revisions. The independent consumer uses
the real npm package `mitt@3.0.1` and TypeScript `4.9.5`.

A typed emitter with `{foo: string}` rejects `off('*')`: the wildcard overload
requires a handler even though the runtime permits omission. Existing runtime
tests and direct JavaScript calls can pass while the typed application cannot
reach that capability. The documented omission behavior and maintainer
[wildcard clarification](https://github.com/developit/mitt/issues/150#issuecomment-1024417195)
support the narrow repair. The
[older all-listeners discussion](https://github.com/developit/mitt/issues/70#issuecomment-361379190)
guards against clearing named listeners as well.

| Candidate | Source type check | Actual package type check | Named listener retained |
| --- | --- | --- | --- |
| Original package | Not needed | Fail | Yes |
| Source overload fixed; package declaration stale | Pass | Fail | Yes |
| Delivered declaration fixed | Not the deciding layer | Pass | Yes |
| Declaration fixed plus `all.clear()` | Not the deciding layer | Pass | No |

The compiler must still reject invalid event names and wrong handler types.
The exact runtime trace after removing wildcards is a named callback before,
wildcard callback before, and named callback after. No new emitter runtime is
required. This is also an activation control: an ordinary localized type fix can
be solved directly; it need not automatically invoke the whole RTA method.

### CWR: preserve a real repair without overstating the user's outcome

The comparison uses old source `efc9613769960577f148c8e457a41f8c9e4ca234`
and repaired main `18774c0628789b554db10e01189a367a21aad7fb`, with the
same actual `acpx@0.15.1` runtime and current held-final regression. A synthetic
ACP server emits reasoning/tools while withholding its final answer. A separate
status CLI must observe durable progress before that final answer arrives.

Old source fails that check; current source passes. Four focused tests cover
unavailable/corrupt activity, an ended stream and exact process/request identity.
The successful current regression deliberately retains legacy `last_seq == 0`
and the absent legacy event-log path. The new activity contract has a different
owner. Treating those old fields as proof of failure would prescribe a redundant
or incorrect repair.

[PR #12](https://github.com/IndelibleVivi/codex-worker-routing/pull/12) is merged;
[Issue #11](https://github.com/IndelibleVivi/codex-worker-routing/issues/11)
remained open/reopened when inspected. Linux producer → activity → independent
CLI is observed. The reporter's Windows/OpenCode rendering of the new fields is
unobserved. That exact consumer adoption check remains; the source repair should
neither be erased nor promoted to whole-UI acceptance.

## Cycle 3 — a new Go case after the candidate was frozen

Viper was selected after freezing the candidate, without changing the Skill.
It is an issue-directed, researcher-selected transfer case, not blind discovery
or another natural A/B pair. The actual Go consumer selects source
`528f7416c4b56a4948673984b190bf8713f0c3c4` through a verified local module
replacement. It uses Go 1.27.4; the checkout stays clean. No claim is made about
independently downloaded Viper release bytes.

The task is to decode an environment-only configuration into a struct and reread
it after a value changes. With only `AutomaticEnv()`, direct lookup sees alpha
then beta, but `Unmarshal` returns an empty field both times without an error.
Explicit `BindEnv`, a registered default key and `ExperimentalBindStruct` each
decode alpha then beta. A tempting `Set(key, Get(key))` workaround succeeds once
and retains alpha after the environment changes. Separate empty-value controls
confirm both fallback-by-default and explicitly permitted empty values.

Seven variants and twelve readings match the exact matrix. The upstream
`TestUnmarshalWithAutomaticEnv` also passes, but it explicitly enables the
experimental mode. The [umbrella issue](https://github.com/spf13/viper/issues/761)
explains lazy lookup versus known-key enumeration; the
[v1.18.2 release history](https://github.com/spf13/viper/releases) records why
struct binding was disabled by default after a pointer-decoding regression.
The existing capability, incomplete default task and compatibility rationale
must all survive the audit. The current single-field probe cannot justify
globally enabling an experimental feature or declaring all environment support
broken. A fixed application's `BindEnv` integration may simply be ordinary work.

The offline probe builds before running so a missing compiler/cache is recorded
separately from a failed consumer. It rejects output/cache destinations inside the
observed checkout. Six instrument controls cover protected paths, symlink paths,
compiler failure, a real compiled panic and invalid JSON. The original executable
named `go` on PATH was not a Go compiler; it is retained as a setup control, not
as a Viper defect. No user PATH or system installation was changed.

## Natural Agent behavior and intervention cost

The four task pairs use fresh native sessions and the same task/initial subject
within each pair. The treatment explicitly loads the frozen Skill; the control
has no RTA. There is one run per arm per task, no randomized ordering, and no
stable-release treatment arm. Exact backend model identity, token use, wall time
attributable to a task and actual human review time are unavailable. Explicit
loading is not host discovery evidence.

Both arms passed all four independently judged tasks. Self-reported executor
counts, control/candidate, were mitt 15/15, Cedar 6/13, summary 8/10 and continuation
6/10. These observations show no success-rate improvement and identify plausible
extra tool effort in three cases; they do not estimate a causal slowdown. The
candidate did not earn an activation requirement for simple known repairs.

Subjects can add meaningful tests and local operator documentation within the
task. Independent evaluation uses protected consumer probes, not the Agent's own
success statement. A summary audit's product-byte check is deterministic; its
scope judgment requires a separately identified human/Agent review. Reports and
commands can indicate effort but cannot be converted into minutes of human labor.

The continuation trial exposed an applicability error in reusing an oracle. Its
task retires `legacy.py` from the selected CLI and bundle. The original operation
lab's stricter architecture check prohibits the file anywhere and scans every
root Python file for file I/O. The no-Skill repair leaves a forwarding compatibility
shim and adds a build/verification utility. Those files can trigger the old
checker without preserving a competing production writer. The new trial verifier
keeps that raw rejection and separately evaluates the actual selected graph and
bundle against TASK.md. It does not rewrite the original lab's narrower contract.

`scripts/compare_trials.py` accepts offline receipts with matched subject, prompt,
harness, settings and environment identities. It retains failed, blocked and
unjudged runs; refuses duplicate arms and mismatched comparisons; separates loaded
from unread Skills; and distinguishes observed measurements, proxies and unavailable
values. Only paired observed measurements produce deltas. Evidence locators are
provenance, not authenticated truth, and the tool executes no referenced evidence.

## What changed in the product

| Surface | Change | Why it earns its maintenance cost |
| --- | --- | --- |
| Canonical router and progressive references | Identify the actual recipient, available inputs, admission gate and one valid neighboring use | Turns broad proof-layer advice into a short discriminating observation |
| Intent guidance | Preserve task-dependent information, accepted manual judgment and explicit retained services | Avoids imposing richer workflows or universal offline requirements |
| Operate guidance | Verify the selected compiler/artifact after the final edit; retire duplicate responsibilities by reachability | Rejects source-only repairs without demanding indiscriminate deletion |
| Cedar repair oracle and fourteen challenges | Remove producer context, interleave histories, check source and declared artifact | Fixes eight original false acceptances and two platform-cache counterexamples found in review |
| Optional field probes | Execute pinned real package/compiler and child-process matrices | Reproducible transfer evidence without a general benchmark engine |
| Optional trial comparator and preparation/verifier scripts | Record outcomes and costs with explicit provenance | Makes missing data and evaluator mismatch visible |
| Host and continuation guides | Separate packaging, explicit use, discovery and downstream adoption | Prevents host compatibility claims from outrunning observations |

The installed payload still contains nine files. Research scripts are not copied
into it. No target repository receives a lasting audit service or mandatory
measurement file. The architecture diagram is unchanged because its topology is
unchanged; fresh graph validation is not represented as fresh visual review.

## Methods to retain, revise and stop

### Cycle 4 — independent review of the new instruments

Review found that the first recipient implementation still inherited
`XDG_DATA_HOME`. A packet containing only summaries and a random cache key could
retrieve complete records from that shared directory even under the interleaved
history check. The same mechanism works with `APPDATA`. Both first demonstrate
successful local round trips; both were falsely accepted before the follow-up.
Ordinary XDG data/config/state/cache and Windows application-data roots now differ
per producer and recipient. The final fourteen-candidate challenge accepts two
valid encodings and rejects twelve negatives. Arbitrary environment variables,
absolute external paths and network channels remain outside the trusted-fixture
separation claim.

The reviewer also reproduced an unjudged run appearing comparable and faster,
an output receipt overwriting observed mitt source, a dirty source incorrectly
attributed to a clean commit, and an otherwise correct Cedar repair failing in
an ASCII locale. Corrections respectively gate comparisons on resolved matching
methods, reject protected output paths, read pinned Git bytes, and make evaluator
and fixture-process UTF-8 boundaries explicit. Final checks retain the before
observations and rerun the exact cases. During integration, the dotenv archive
portability edit briefly shadowed its variant name and raised a `KeyError`; the
real matrix rerun caught it, and the corrected probe passed before delivery.

The first remote PR CI run then exposed a fixture-initialization race on macOS
with Python 3.10 and Git 2.56; the other three jobs passed. Background maintenance
launched by a fixture baseline commit left `.git/objects/maintenance.lock` in a
before-snapshot, then removed it before the after-snapshot, failing two Cedar
preservation subchecks. A real Git Trace2 probe reproduced the detached maintenance launch and verified
the finite correction: both fixture initializers now pass
`-c maintenance.auto=false -c gc.auto=0` only to their commit command. Complete
snapshot assertions remain intact; local/global Git configuration, product
fixture bytes and the canonical Skill are unchanged. A focused regression was
added. The correction's remote matrix supplies cross-platform confirmation;
the local trace alone is not macOS acceptance.

These corrections change the research machinery, not the frozen natural-trial
treatment. No natural Agent success is retroactively attributed to them.

### Method decisions

Retain a concrete user task, the actual consumer, one symptom witness and one
valid-neighbor preservation witness. Use two histories that look identical at a
suspect handoff when information loss is plausible. Challenge the oracle with a
working local false completion before claiming that its rejection is meaningful.
Keep changed semantics, old requirements, unavailable environments and accepted
manual work as different adjudications.

Revise broad retirement checks to the task's actual ownership and delivery
contract. A file name or `.open` search can find candidates; it does not settle
responsibility. Reconcile checkpoints against current files and later owner
changes. Consolidate one owner-facing decision and evidence set instead of
requiring users to combine multiple worker reports.

Stop adding routines when a short ordinary fix and consumer check already settle
the task. Do not reward report length, test count, Skill vocabulary, deletion
volume or the number of agents. Do not rerun unrelated suites to compensate for
one missing host observation. Do not report unknown human effort as zero.

## Research basis and limits

[UTBoost](https://aclanthology.org/2025.acl-long.189/) shows that inadequate
tests can accept incorrect SWE-bench patches and change rankings. It motivates
auditing outcome oracles; it does not validate this Skill's model effect.
[OpenAI's coding-evaluation audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
distinguishes strict tests, underspecified tasks, low coverage and misleading
prompts. The continuation mismatch demonstrates why these categories need actual
contract review. [SWE-Bench Pro V2](https://arxiv.org/abs/2610.24206v2) uses
independent reimplementation and clean-environment regrading as repair methods;
this study adopts the separation of implementation and judgment without claiming
its scale. [METR's 2026 update](https://metr.org/blog/2026-02-24-uplift-update/)
explains selection and time-measurement difficulties when developers choose AI
use and run agents concurrently. Our missing human-time values remain missing.

The real cases cover Python, TypeScript and a Node process integration, with a
later transfer case recorded separately. They do not establish coverage of large
monorepos, distributed migrations, real production data or every host. Known
historical defects may already be familiar to the model. Instruction-scoped
subjects are not sealed sandboxes. Self-reported tool counts are proxies. New
natural runs can be compared descriptively, with exact model and harness logging
improved before any causal efficiency claim.

## Reproduce and continue

Use the [experiment protocol](../evals/experiments/2026-11-user-outcomes/README.md)
for tasks, candidate identity, independent regrading and receipts;
[field probes](../evals/field/README.md) for pinned real cases;
[host compatibility](host-compatibility.md) for what each observation proves;
and the [local Codex commission](codex-handoff.md) for a complete next work order.
The [current-state record](current-state.md) owns the final fresh validation
counts and source/release distinction. Raw experimental evidence stays outside
the source tree; public reports contain reproducible inputs and screened results.
