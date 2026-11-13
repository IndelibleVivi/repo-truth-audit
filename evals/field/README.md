# Real consumer probes

[简体中文](README.zh-CN.md)

These optional probes execute pinned public projects in disposable copies.
They make no target-model call and never run during ordinary repository CI.
Prepare the inputs explicitly; the probes do not clone, contact an upstream
maintainer or change an observed repository or global environment. The
sampleproject probe builds and installs only inside disposable virtual
environments, using explicitly prepared offline inputs. They are evaluator
material and must stay outside target-agent workspaces.
Output receipts must be outside observed source/package directories; the probes
reject destinations that would overwrite their inputs. Python helpers support
the repository's Python 3.10+ syntax; the original field runs used 3.12.14.
Later dated observations state their own interpreter versions below.

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

## Python: selected installed package (predeclared constructed experiment)

Before execution, this case selects public `pypa/sampleproject` at
`621e4974ca25ce531773def586ba3ed8e736b3fc`. Its inspected backend is
`setuptools.build_meta`, with setuptools required. This is a constructed delivery
experiment, not an upstream defect report or a blind test of Skill benefit.
The concrete consumer imports `sample.simple.add_one(10)` from a selected venv.
Expected readings: baseline wheel 11; intentional source-only +2 leaves wheel
consumer 11 while source reads 12; rebuilt/reinstalled wheel 12; native pip
editable install reads 12; a later owner +3 source edit makes editable read 13,
while the regular wheel legitimately stays 12 until explicit rebuild delivers 13.
The frozen-wheel neighbor must not be classified as defective merely because
source changed. Actual module origin and PEP 610 direct_url metadata must establish
selection; a PYTHONPATH checkout shim is not editable-install evidence.

The wrapper will use exact Git-pin bytes in disposable copies, separate explicit
network-enabled seed preparation from offline wheel/editable operations, and
record selected Python/build-tool versions. Output/source/seed overlap, including
symlinks, is rejected before writes. Setup failures remain distinct from semantic
mismatches. This optional external run does not enter ordinary CI and invokes no
model; no canonical Skill change is presumed.

Reproduce with an explicitly prepared development seed (network is used only in
these setup commands; choose disposable paths outside the observed checkout):

```sh
git clone https://github.com/pypa/sampleproject.git /path/to/sampleproject
git -C /path/to/sampleproject checkout 621e4974ca25ce531773def586ba3ed8e736b3fc
uv venv --python python3 /path/to/seed
uv pip install --python /path/to/seed/bin/python pip==26.3 setuptools==84.2.1 wheel==0.48.0 packaging==26.3 peppercorn==0.6
/path/to/seed/bin/python -m pip download --dest /path/to/seed/wheelhouse pip==26.3 setuptools==84.2.1 wheel==0.48.0 packaging==26.3 peppercorn==0.6
python3 evals/field/probe_sampleproject.py --source /path/to/sampleproject \
  --seed /path/to/seed --output /path/to/observation.json
python3 -m unittest discover -s tests -p test_sampleproject_probe.py
```

The probe creates stdlib venvs without pip, then uses the seed's native
`pip --python` to install cached build tools and the real runtime dependency
`peppercorn`. It builds actual wheels with the inspected backend and performs a
native pip editable install. All project install/build commands disable dependency
fetch and build isolation; dependency setup in the target venvs selects only the
preseeded local wheelhouse. `PYTHONPATH` is removed. The source-only control
explicitly inserts the disposable checkout path; editable readings use isolated
Python with no such insertion. These pip restrictions are not OS network isolation;
the inspected backend runs trusted public code. Temporary paths are scrubbed in
successful receipts. A failed setup can contain local diagnostic paths, so keep raw
receipts private. Source/seed snapshots compare file names, sizes, mtimes and
symlink targets; they are write-detection evidence, not cryptographic identity.

Observed on 2026-11-14 with Python 3.13.5, pip 26.3, setuptools 84.2.1,
wheel 0.48.0, packaging 26.3 and peppercorn 0.6: all eight readings matched the
predeclared sequence **11 / 12 / 11 / 12 / 12 / 13 / 12 / 13**; all 22 subprocesses
succeeded, source/seed file names, sizes, mtimes and link targets stayed unchanged. Both installed
selection modes were established by module origin and direct_url metadata. The
nine offline tests cover value/origin/metadata rejection, the frozen-wheel
neighbor, symlink/overlap protection, input write detection and distinct failure
statuses (including nonzero/invalid-JSON ready consumers and retained portable setup-command evidence; `observed` 0, `expectation-mismatch` 1, `setup-blocked` 2).
Only this selected function and deployment sequence were tested; console-script
behavior, other Python/tool versions, naturally occurring agent mistakes and Skill
benefit remain unmeasured. No upstream mutation or canonical Skill change resulted.
