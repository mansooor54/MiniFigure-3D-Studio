# Testing Strategy

## Purpose

MiniFigure 3D Studio uses evidence-driven milestone gates. A planned capability is not described as working until the relevant automated and controlled manual checks pass in the environment named by the claim. Portable macOS or Linux evidence cannot satisfy a Windows-only requirement.

## Result Vocabulary

| Result | Meaning |
|---|---|
| **Passed** | The check ran in its declared environment and met every acceptance criterion. |
| **Failed** | The check ran and at least one criterion was not met. The owning milestone remains open. |
| **Skipped** | The test runner intentionally skipped a collected test. This never satisfies a mandatory gate. |
| **Not Run** | The check was not executed. No conclusion may be inferred. |
| **Blocked** | A prerequisite, environment, license, engine, model, or owner decision prevents execution. |

## Test Tiers

| Tier | Scope | Normal environment | Gate use |
|---|---|---|---|
| Static quality | Formatting, lint, typing, schema and workflow syntax, secret patterns | Python 3.11 on every available development platform | Required for every batch. |
| Unit | Pure domain, services, validators, calculations, and deterministic adapters | Portable Python 3.11 | Required before integrating the owning behavior. |
| Contract | Versioned requests, results, manifests, ports, bridges, and provider boundaries | Portable Python 3.11 with fakes | Required before any real engine or process adapter. |
| Integration | Filesystem, project recovery, Qt processes, viewer, Blender, inference, and export boundaries | The real operating system/runtime named by the test | Required for the corresponding vertical slice. |
| UI | Qt startup, navigation, RTL, accessibility, responsiveness, errors, and progress states | Offscreen where sufficient; native interactive review where rendering matters | Required before describing a screen as working. |
| End to end | Import through validated export, including failure/cancel/recovery | Fully configured supported environment | Required for Stage 2 approval. |
| Packaging | Built application on a clean target system with offline and resource checks | Native Windows 10/11 | Required before any Windows package or support claim. |
| Security/privacy | Dependency audit, secret/log redaction, network denial, asset policy, consent, and diagnostics | Portable plus native platform tests where APIs differ | Required at every affected boundary. |

## Platform Labels

| Label | Interpretation |
|---|---|
| `portable` | Pure behavior expected to be independent of the operating system. |
| `macos-arm64` | Executed on the connected Apple Silicon development computer. |
| `windows-11-x64` | Executed on a real Windows 11 x64 system; unavailable evidence remains Not Run. |
| `windows-10-x64` | Executed on a real Windows 10 x64 system; required for that support claim. |
| `blender-<version>` | Executed by the named real Blender build in background mode. |
| `gpu-<runtime>` | Executed with the named GPU, driver, runtime, and model manifest. |
| `package-clean` | Executed from a produced package on a clean machine without the development environment. |

The temporary platform exception in `docs/platform_baseline_exception.md` permits portable implementation to proceed on macOS. It does not convert macOS results into Windows evidence.

## Synthetic Fixture Policy

Repository fixtures are generated deterministically by `scripts/create_synthetic_fixtures.py`. Every fixture has a manifest path, source, generator version, license, SHA-256 hash, size, purpose, expected result, and explicit flags declaring that it contains neither a real person nor EXIF.

`tests/fixtures/asset_manifest.yaml` is authoritative. `scripts/validate_assets.py` fails for a missing asset, hash/size mismatch, unsafe path, duplicate path, incomplete license/source record, real-person flag, EXIF-capable format without a dedicated audit, or an unmanifested fixture file. Real-person photographs and generated real-person likenesses are prohibited in Git, CI artifacts, reports, issues, and screenshots.

## Determinism

Tests use fixed clocks, deterministic identifier factories, generated names, and temporary roots. Fixture generation must produce byte-identical outputs on repeated runs. Tests may not depend on network availability, unordered filesystem output, the user's locale, current time, or a prior user project unless the test explicitly owns that dependency.

## Qt Tests

Qt tests run with a controlled platform plugin. The connected macOS environment required clearing an unexpected hidden file flag from the ignored PySide6 plugin tree; this repair is environment evidence, not repository content. UI tests must still exercise the event loop, keep long work outside the GUI thread, and use native review when visual layout or platform integration cannot be established offscreen.

## Failure and Fault Tests

Expected failure paths are first-class behavior. A process exit code of zero is not sufficient for success. Tests must independently validate current run and stage IDs, versioned schemas, expected artifacts, hashes, reopen checks, and semantic constraints. Cancellation, timeouts, missing tools, malformed/stale results, locked files, permission denial, disk-full behavior, and restart recovery are added with their owning adapters.

## Evidence Record

Every batch report records the following fields.

| Field | Required content |
|---|---|
| Source | Branch, commit, and clean/dirty state. |
| Environment | OS/version/architecture, Python, Qt, tool/runtime/model versions, and relevant hardware. |
| Command | Exact command or job identifier. |
| Result | Passed, Failed, Skipped, Not Run, or Blocked. |
| Counts | Collected, passed, failed, skipped, and duration where available. |
| Artifacts | Redacted logs, reports, screenshots, output hashes, and manifests. |
| Limitations | Every unavailable platform, model, engine, interaction, or performance gap. |
| Rollback | Commit or deterministic recovery procedure. |

## Local B02 Quality Sequence

From the repository root with the Python 3.11 environment active, the local portable lane runs the fixture generator, asset validator, Ruff, mypy, pytest, dependency audit, SBOM generator, and license collector. The GitHub workflow mirrors that lane on Linux and macOS. Native Windows jobs are added only when a Windows runner and Windows-specific implementation exist.
