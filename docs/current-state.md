# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-08-30

## Product

- Product form: standalone public repository and standalone Codex Skill.
- Naming: human-facing display name **Repo Truth Audit**; formal name
  **Repository Operational Truth Audit**; public repository slug
  `repo-truth-audit`; Skill invocation slug
  `repository-operational-truth-audit` remains unchanged.
- Version: public release `v0.1.0`; current `main` contains unreleased
  architecture-presentation, naming, eval-fidelity, public-evidence, and
  Windows checkout/digest portability corrections and does not retag that
  release.
- Scope: complete topology-first, decision-bounded, read-only audit contract.
- Canonical Skill: `skills/repository-operational-truth-audit/`.
- Public documentation: separate English and Simplified Chinese editions.
- Public forward evidence: the paired
  [`forward-behavior-receipt`](forward-behavior-receipt.md) records the tested
  subject identity, dirty and clean cases, material results, proof layers,
  overhead limits, `UNKNOWN` trace fields, and explicit external boundaries.
- Architecture on current `main`: one renderer-neutral semantic model plus one
  native Mermaid diagram in each localized README. Both diagrams retain six
  regions, 21 stable nodes, 30 semantic edges, exact connector-kind parity,
  and explicit read-only, external-proof, and fixed-point boundaries.
- Historical release architecture: immutable `v0.1.0` contains the earlier
  localized SVG pair and deterministic renderer. Those tagged bytes remain
  release evidence; the generated SVGs and renderer are retired from current
  source rather than maintained as a parallel active path.
- Softpowers relationship: optional companion/reference only; no generation,
  bundling, installation, or version ownership.

## Gates

- Current source: the localized README Mermaid blocks are the active public
  architecture views; `docs/architecture/audit-runtime-model.json` remains the
  semantic authority. The result examples precede the diagrams; the diagrams
  themselves are unchanged by the naming/eval/evidence patch. Architecture
  docs, product spec, AGENTS, changelog, validators, tests, and CI commands are
  reconciled to that split.
- Eval fidelity: the intentional-multiplicity clean canary now requires
  `Decision answer: ready` and rejects `Decision answer: not ready`; a focused
  regression test prevents the ambiguous `"ready"` substring assertion from
  returning.
- Windows source portability: tracked text files retain LF in ordinary
  checkouts, preserving exact pinned-license hashes, and Skill digest inventory
  ordering uses normalized POSIX relative paths. Bash remains required for the
  fixture self-test; broader Windows operator support is not claimed.
- Deterministic validation: local PASS on 2026-08-30 for repository/publication
  validation, architecture model and localized Mermaid parity, 17 unit tests,
  six fixture truth checks, fixture self-test, system Skill quick validation,
  ordinary Windows `core.autocrlf=true` checkout validation, and Git whitespace
  validation. The quick validator ran with PyYAML isolated from the repository
  because the host Python runtimes do not provide it; no dependency was added
  to the repository or Skill package.
- Mermaid render acceptance: PASS on 2026-08-30 for public `main` architecture
  commit `9805fa52f35a3635ee66e3f651ca891de4baad23`. GitHub rendered both localized
  blocks in light mode; all read-only, external-proof, fixed-point, and end
  re-pin boundaries were present, and the Chinese rendered surface exposed all
  30 localized edge labels. The native viewer supplied zoom and pan controls.
  Default fit remains compact because the complete topology is dense; this is
  not represented as large-text acceptance without using the native viewer.
- Independent forward behavior: PASS on 2026-08-30. An artifact-split case
  reached the stale distributed entrypoint and false-green source test; a clean
  control treated stable/development selection as intentional multiplicity.
  The public-safe receipt exposes the material result and proof boundary while
  preserving unavailable model, effort, command-count, and plan-count fields as
  `UNKNOWN`.
- Git release identity: canonical `0.1.0` Skill bytes entered at
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2`. Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peels to release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`. The tag remains immutable.
- Local install: PASS for immutable `v0.1.0`. Tagged and installed Skill digests
  equal `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`.
  Current source digest is
  `ca4fd01e20964c87884f4fe46a1ceb0864cf23b55061c90cd5bc24558a396a3a`
  because `agents/openai.yaml` now carries the shorter display name. Runtime
  `SKILL.md` remains byte-identical at SHA-256
  `cc16bad2960a3d0e315c055cf5ec244ec57c2f7cc51da12d5d480b603bf1c15f`.
  Current `main` has not been installed; installed/source digest equality is
  therefore not claimed for the unreleased metadata change.
- Next-turn Codex discovery: not observed.
- Current-main CI: PASS. Actions run `33300477192` passed all four Ubuntu/macOS
  and Python 3.10/3.13 jobs on substantive naming/eval/evidence commit
  `8ef4b960dfd4beefd15ede83f5575f2688630259`. Release run `33295744677`
  separately passed the same matrix on the peeled `v0.1.0` release commit.
  Workflow source and live CI remain separate facts.
- Release publication: PASS. GitHub Release `v0.1.0` was published on
  2026-08-30 and is neither draft nor prerelease. Anonymous tagged read-back,
  disposable public-tag installation, Skill validation, digest equality, and
  pinned SUL text were verified. After the repository rename, annotated tag
  object `235be6e...` still peels to `0180e4c...`, and the release remains
  available under the new canonical slug. No new release is implied by the
  current-main corrections.
- Current-main publication: PASS for substantive commit `8ef4b960...`. The
  canonical public remote is
  `https://github.com/IndelibleVivi/repo-truth-audit`; the previous repository
  URL returns an HTTP 301 to it. Public read-back exposed the new README title,
  formal-name line, unchanged Skill slug, and forward-behavior receipt. A later
  status-only reconciliation may move `main` without changing this substantive
  source identity. The accepted architecture identity remains `9805fa52...`.
- Licensing: functional materials are source-available under SUL-1.0;
  standalone documentation, the renderer-neutral architecture model, and the
  Mermaid diagrams embedded in the README files are under CC BY-NC-SA 4.0
  according to `LICENSING.md`. GitHub reports the layered repository license as
  `Other`; the path map, not a single-license badge, is authoritative.

Replace superseded status here; do not append a development diary.
