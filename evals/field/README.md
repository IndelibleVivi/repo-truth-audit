# Real consumer probes

[简体中文](README.zh-CN.md)

These optional probes execute pinned public projects in disposable copies.
They make no target-model call and never run during ordinary repository CI.
Prepare the inputs explicitly; the probes do not install, clone, contact an
upstream maintainer or change an observed repository. They are evaluator
material and must stay outside target-agent workspaces.
Output receipts must be outside observed source/package directories; the probes
reject destinations that would overwrite their inputs. Python helpers support
the repository's Python 3.10+ syntax; the actual field runs used 3.12.14.

## Python: configuration inherited by a real child

Use an existing Python environment with Click available. The recorded observation
used Python 3.12.14 and Click 8.4.2. The source checkout must contain both pinned
commits; only temporary archives are mutated.

```sh
git clone https://github.com/theskumar/python-dotenv.git /path/to/python-dotenv
python3 evals/field/probe_dotenv.py --repo /path/to/python-dotenv --output /path/to/dotenv.json
```

The historical task comes from [issue #697](https://github.com/theskumar/python-dotenv/issues/697)
and [repair #698](https://github.com/theskumar/python-dotenv/pull/698).
`a00cb2eed0704cd6d2071b2004c37e95ccc86ee5` is the before state;
`e0310e5bb3f2b701b11bbc007ca0c82c1bd56f38` is the upstream repair.
The executable entry is `python -m dotenv`; a child process reports its final
environment. The probe covers preserved values, preserved empty values and the
valid override mode, with wrong-layer, overbroad, incomplete and misleading-README
controls. The existing API is a positive control. All 19 processes can exit zero
while their semantic outcomes differ. This is source-entry evidence, not a wheel
or user-installed console-script test.

## TypeScript: the published declaration and runtime

```sh
git clone https://github.com/developit/mitt.git /path/to/mitt
git -C /path/to/mitt checkout 6b41670516ed8e8b738612f60491995470aa63b3
npm install --ignore-scripts --no-audit --no-fund --prefix /path/to/mitt-consumer mitt@3.0.1 typescript@4.9.5
python3 evals/field/probe_mitt.py --source /path/to/mitt --consumer-seed /path/to/mitt-consumer --output /path/to/mitt.json
```

The task is to remove wildcard subscribers while preserving named subscribers.
The real package's declaration blocks the supported one-argument operation.
Controls reject a source-only repair, broadening the type contract, and a runtime
change that removes named subscribers too. The source-only check and consumer
check intentionally select different entry surfaces. See the maintained semantic
clarifications in [issue #150](https://github.com/developit/mitt/issues/150#issuecomment-1024417195)
and [issue #70](https://github.com/developit/mitt/issues/70#issuecomment-361379190).

The source-only variant reads pinned `git show` bytes, so unrelated working-tree
edits cannot silently change the source attributed to that commit. Package
versions, actual declaration hashes and compiler observations are recorded.

## Go: selected environment-to-struct configuration

Provide a real Go compiler satisfying the pinned module's Go 1.23 requirement.
Dependency preparation is explicit; the Python probe itself disables Go proxy
lookup and automatic toolchain downloads. Use an existing populated module cache,
or prepare one with the normal Go tooling before the offline observation:

```sh
git clone https://github.com/spf13/viper.git /path/to/viper
git -C /path/to/viper checkout 528f7416c4b56a4948673984b190bf8713f0c3c4
/path/to/go/bin/go version
/path/to/go/bin/go -C /path/to/viper mod download
python3 evals/field/probe_viper.py --repo /path/to/viper --go /path/to/go/bin/go \
  --output /path/to/viper-observation.json
```

`--module-cache` can select a separately prepared Go module cache;
`--build-cache` can select a scratch compiler cache outside the observed checkout.
The default compiler cache is disposable. `viper_consumer.go` must remain beside
the wrapper. The actual observation used Go 1.27.4 on Linux, compiled the consumer,
and verified that its module replacement selected the pinned source. This is not
a separately installed release-package test.

Seven variants/twelve readings compare default `AutomaticEnv`, key binding,
default-key registration, the explicit experimental struct mode, a stale snapshot
workaround and two legitimate empty-value policies. Each successful API call is
checked for its actual decoded value. The case was selected after the candidate
Skill freeze; no new runtime rule was needed. See
[issue #761](https://github.com/spf13/viper/issues/761) and the
[v1.18.2 compatibility explanation](https://github.com/spf13/viper/releases).

The wrapper records compilation separately from consumer execution: `observed`
exits 0, `expectation-mismatch` exits 1, and `setup-blocked` exits 2. Missing cached
dependencies are not a Viper defect. The environment options restrict Go module
resolution; they are not OS network isolation.

## Node/ACP: progress before the final result

The CWR field observation uses a public owner repository, a real pinned
`acpx@0.15.1` runtime and a synthetic ACP server. The current test observes durable
activity from a second CLI while the final response is held:

```sh
git clone https://github.com/IndelibleVivi/codex-worker-routing.git /path/to/cwr
git -C /path/to/cwr checkout 18774c0628789b554db10e01189a367a21aad7fb
cd /path/to/cwr/integrations/acpx
npm ci --ignore-scripts --no-audit --no-fund
node --test --test-name-pattern='REAL activity:' test/real-acpx.integration.mjs
node --test --test-name-pattern='prompt with no events|live status requires|live phase distinguishes|ended observation stream' test/cli.test.mjs
```

For the paired old-source observation, extract
`efc9613769960577f148c8e457a41f8c9e4ca234` into a separate disposable checkout.
Copy `test/real-acpx.integration.mjs`, `test/helpers.mjs` and
`test/fixture-acp-agent.mjs` from the current `integrations/acpx` tree, and use the
same dependency tree there. Run the identical held-final command. The old source
fails the live-progress assertion; the current source passes. The current test
is deliberately copied to the old source; it is not represented as a historical
test already shipped with the old tree.

The observed boundary is Linux producer → persisted activity → status CLI.
Windows/OpenCode rendering is a separate unobserved consumer boundary. A retained
zero legacy sequence and absent legacy event log do not invalidate the new
status path. See [the full case reasoning](../../docs/user-outcomes-study.md).

These are deliberately selected mechanisms. The upstream repair and constructed
variants are evaluator evidence, not natural model outputs or representative
failure-frequency estimates. Temporary directories model deployment boundaries
for inspected code; they are not hostile-code isolation.
