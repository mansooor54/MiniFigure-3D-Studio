# MiniFigure 3D Studio — Stage 2 Execution Runbook

**Author:** Manus AI  
**Status:** Planned operating procedure; commands are templates to be validated after the workspace and Windows environment are confirmed

## 1. Purpose

This runbook governs how Stage 2 implementation should be executed after the product owner binds the development folder and supplies the remaining M0 decisions. It prevents uncontrolled scope growth, false test claims, unsafe engine enablement, and milestone progression while mandatory evidence is missing.

## 2. Start Authorization

Application source creation begins only when the following record is complete.

| Item | Required value |
|---|---|
| Workspace | Bound Manus Desktop folder or explicit existing repository path. |
| Repository | New/existing status, default branch, remote policy, current dirty/clean state. |
| Stage approval | Stage 1 approved; Stage 2 planning package accepted or revised. |
| Target environment | Windows 11 development environment and Windows 10 smoke strategy. |
| Product license | Selected shell license or private-development-only status. |
| Qt path | Dynamic LGPL-oriented development architecture or commercial Qt. |
| Blender | Discovery-first supported LTS policy accepted. |
| Background model | Candidate benchmark list and approval owner. |
| Real generator | Hunyuan eligibility/rights or approved alternative/provider path. |
| Test assets | Synthetic fixture policy accepted; no real-person repository assets. |

If a production engine/model decision is unresolved, core/fake-adapter batches may proceed, but the real integration batch remains blocked and Stage 2 cannot close.

## 3. Repository Initialization Procedure

The planned setup sequence on native Windows is shown below. Exact Python and dependency versions are substituted from the approved compatibility record.

```powershell
# Run from the bound parent folder after repository approval.
git status
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest --collect-only
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy app
```

These are templates, not executed results. The final setup guide records the exact Python patch, lock hashes, PowerShell policy assumptions, and commands actually proven on the clean environment.

## 4. Batch Execution Loop

Every batch B01–B27 follows the same loop.

| Step | Action | Required output |
|---:|---|---|
| 1 | Confirm prior batch gate is Passed | Link to prior batch report and commit. |
| 2 | Re-read owning requirements, architecture boundary, and test IDs | Batch scope statement; no unrelated files. |
| 3 | Record clean repository state and environment | Commit hash, branch, environment manifest. |
| 4 | Add or update tests/fixtures for the intended behavior | Failing or not-yet-implemented test evidence where practical. |
| 5 | Implement the smallest coherent files in the approved order | Focused typed modules; no speculative Stage 3 implementation. |
| 6 | Run focused tests | Command, result counts, duration. |
| 7 | Run regression lanes affected by the change | Unit, type, lint, contract, integration, UI, viewer, Blender, or generator as applicable. |
| 8 | Review security, privacy, license, localization, and artifact impacts | Checklist and changed manifests/notices. |
| 9 | Update documentation and exact file list | Batch report and changelog. |
| 10 | Commit or create a rollback checkpoint | Commit hash and rollback instructions. |
| 11 | Evaluate the milestone gate | Passed, Failed, Blocked, or requires rework. |

A failed mandatory test returns to Step 4 or Step 5. The next behavior-changing batch does not start.

## 5. Branch and Commit Discipline

| Practice | Rule |
|---|---|
| Branch | One milestone branch, with short-lived batch branches only if the repository workflow requires them. |
| Commit | Coherent behavior plus tests; generated runtime/model/project data never committed. |
| Message | Include milestone/batch and outcome, such as `M4 B10: supervise fake workers and validate results`. |
| Dirty state | Test reports record whether the tree is dirty; milestone evidence requires a clean identified revision. |
| Rebase/merge | Rerun affected mandatory tests after history/integration changes. |
| Tag/checkpoint | Tag or record a rollback commit after each milestone gate passes. |
| Generated files | Viewer distribution, translations, lock files, and reports follow an explicit generated-file policy; source remains authoritative. |

## 6. Definition of Ready for a File

A source file is ready to create when its responsibility is named in the approved structure, its dependencies already exist or are in the same small batch, at least one test or observable behavior owns it, its user-facing strings have message keys, and its security/license implications are known.

A file is not created simply to populate the future directory tree. Stage 3 modules remain absent until needed.

## 7. Coding and Review Standard

| Area | Required practice |
|---|---|
| Python | Python 3.11, complete public type hints, dataclasses/value objects where suitable, explicit `if`/`else`, focused functions/classes. |
| Dependency injection | Composition root creates concrete adapters; domain/application code depends on ports. |
| Paths | `pathlib.Path`; generated internal names; canonical containment checks; no shell string interpolation. |
| Processes | `QProcess` executable plus argument list; minimal environment; generated safe working directory. |
| Errors | Stable code, human summary key, corrective-action key, retryability, technical cause, redacted context. |
| Logging | Structured events through mandatory redaction processors before every sink. |
| UI thread | No decoding, hashing, inference, process wait, mesh work, export, or unbounded filesystem traversal. |
| Artifacts | Raw/source immutable; stage → validate → atomic promote; current run/stage identity mandatory. |
| Localization | User-visible string keys from the first implementation; no English literals in services/adapters. |
| Privacy | No image pixels, EXIF payload, credentials, or unsafe full paths in logs/tests/reports. |
| Tests | Deterministic synthetic fixtures; expected failure paths are first-class tests. |

## 8. Planned Quality Commands

Exact flags are finalized in `pyproject.toml`, but the runbook expects these categories.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy app generators
.\.venv\Scripts\python.exe -m pytest tests\unit -q
.\.venv\Scripts\python.exe -m pytest tests\contract -q
.\.venv\Scripts\python.exe -m pytest tests\integration -q
.\.venv\Scripts\python.exe -m pytest tests\ui -q
.\.venv\Scripts\python.exe -m pytest tests\blender -q
.\.venv\Scripts\python.exe -m pytest tests\e2e -q
.\.venv\Scripts\python.exe -m pip_audit
```

A category that does not exist yet is not claimed. A test requiring Blender, GPU, or a clean VM is run only in its declared environment and cannot be replaced by a mock result.

## 9. Batch Report Template

```markdown
# Mx / Bxx Batch Report

**Revision:**
**Environment:**
**Objective:**

## Files Created
| File | Purpose |
|---|---|

## Files Modified
| File | Change |
|---|---|

## Dependencies and Licenses
| Change | Reason | License/notice effect |
|---|---|---|

## Tests
| Command/Job | Passed | Failed | Skipped | Not Run | Evidence |
|---|---:|---:|---:|---:|---|

## Manual Checks
| Check | Expected | Actual | Evidence |
|---|---|---|---|

## Known Defects and Limitations

## Gate Decision
Passed / Failed / Blocked

## Rollback
Commit or procedure.
```

## 10. Dependency-Change Procedure

A developer does not add a package directly because it simplifies one function. The change first records the owning requirement, why standard library/current dependencies are insufficient, Windows/Python support, direct and transitive footprint, license/notice implications, native DLL/codecs, security posture, alternative considered, and removal plan.

The dependency is installed in a clean Windows environment, probed, tested, inventoried, audited, and then locked. An update follows the same process and reruns all affected tests.

## 11. Engine Integration Procedure

| Step | Action | Stop condition |
|---:|---|---|
| 1 | Implement and pass fake adapter contract | Contract failure. |
| 2 | Create candidate decision record and manifest | Missing source/license/territory/hashes. |
| 3 | Verify package/model offline before execution | Hash/schema/signature failure. |
| 4 | Run self-test without user images | Self-test or protocol failure. |
| 5 | Run resource and eligibility preflight | Ineligible territory/license or unsupported hardware. |
| 6 | Run controlled synthetic/permitted success | Missing, empty, stale, or implausible output. |
| 7 | Run controlled failure/cancel/timeout | Any false success or leaked resource. |
| 8 | Reopen and validate output independently | Geometry/resource/provenance failure. |
| 9 | Enable feature state for the tested environment only | Any mandatory test unsatisfied. |

For an external adapter, credential storage, disclosure, consent, metadata minimization, timeout, duplicate-submission safety, and remote cancellation truth are implemented before Step 6 can make a network request.

## 12. Blender Execution Procedure

Blender supports background execution and Python-script invocation by command-line arguments.[1] The application should conceptually launch the validated executable with background mode, a known script, and application-specific arguments after `--`.

```text
<validated-blender.exe> --background --python <pipeline_runner.py> -- --request <request.json>
```

The implementation must use an executable and argument list rather than constructing this displayed text as a shell command. A Blender run is accepted only when the result schema, run/stage identity, expected outputs, hashes, reopen checks, dimensions, and operation metrics pass.

## 13. UI Responsiveness Procedure

For every operation that may exceed a short UI action, the developer identifies the execution boundary before implementation. External/native/AI/Blender tasks use processes. Pure Python calculations use a bounded worker where appropriate. The UI owns presentation state only.

The batch test runs a heartbeat timer during the operation, triggers cancel where applicable, changes safe UI panels, and confirms that close/recovery behavior is explicit. Any freeze blocks the milestone.

## 14. Error and Failure Triage

| Failure class | First action | Evidence retained |
|---|---|---|
| Test regression | Stop new work; isolate smallest failing revision/fixture | Full command, environment, diff, failure log. |
| Native process crash | Preserve last checkpoint; inspect exit/result/log without promoting output | Exit code, versions, bounded redacted stderr, stage files. |
| Malformed/stale result | Mark protocol/artifact failure; retain invalid staging for developer review if safe | Request/result hashes and schema errors. |
| UI freeze | Capture thread/task/process state; move work out of GUI thread before proceeding | Reproduction steps and timing. |
| License/territory uncertainty | Disable production feature; continue with fake adapter only | Decision record and source links. |
| Secret/privacy leak | Block milestone; quarantine bundle/log; repair redaction and rerun seeded scans | Safe incident record without repeating secret. |
| Geometry damage | Revert to pre-operation artifact; compare metrics; revise threshold/operation | Before/after fixture hashes, metrics, screenshots. |
| Export invalid | Leave final destination untouched; retain/report staging status | Reopen error, format/version, expected/actual inventory. |

## 15. Rollback Procedure

Every successful batch ends at a known commit. Runtime migrations and engine updates keep the previous valid project schema/artifact or engine version until the new path succeeds. Rollback never deletes the only raw input, raw generated mesh, or last readable manifest.

When a batch must be reverted, record the failed batch, affected revisions, reason, data/schema impact, rollback command or commit, environment cleanup, and tests rerun after rollback.

## 16. Security and Privacy Review per Milestone

| Milestone | Mandatory review |
|---:|---|
| M1 | Secrets, assets, dependencies, licenses, CI artifacts. |
| M2 | Path traversal, reparse points, atomicity, logs, deletion truth. |
| M3 | Accessible/RTL strings, recent-project privacy, safe errors. |
| M4 | Command injection, minimal child environment, process-tree cleanup, redaction. |
| M5 | Image decoder limits, EXIF/log exclusion, source immutability. |
| M6 | Model rights/hashes, silent download denial, inference isolation. |
| M7 | CSP/request interception, local-file denial, bridge schema, metadata escaping. |
| M8 | Blender executable trust, script license, safe working paths, output validation. |
| M9 | Engine license/territory, secrets/consent if remote, resource preflight, provenance. |
| M10 | Cross-stage stale-artifact prevention, cancellation/recovery. |
| M11 | Transactional export, overwrite, malformed files, path limits. |
| M12 | SBOM/notices, package inventory, network deny, seeded-sensitive-data scan. |

## 17. MVP Demonstration Script

The Stage 2 candidate demonstration follows the real implemented workflow rather than screenshots of disconnected screens.

| Step | Demonstrated behavior |
|---:|---|
| 1 | Start the development package offline and open the bilingual shell. |
| 2 | Create a project in an Arabic-containing path and select Fast AI. |
| 3 | Import synthetic/permitted images, show skipped/quality/duplicate findings, assign views, and confirm the primary image. |
| 4 | Run approved local background removal or demonstrate manual fallback, correct the mask, and restart to prove persistence. |
| 5 | Show generator eligibility/device/resource summary and run a real approved generation. |
| 6 | View the raw artifact offline; rotate/zoom/pan/wireframe/material and inspect parts. |
| 7 | Run Blender cleanup, show real progress, metrics, four previews, and raw-versus-processed comparison. |
| 8 | Show minimum validation status and qualified wording. |
| 9 | Export STL and GLB, reopen/validate, and inspect report/hashes. |
| 10 | Demonstrate at least one actual controlled failure, cancellation, and restart recovery. |
| 11 | Show redacted logs/technical details and the exact versions/manifests. |

## 18. Stage 2 Closeout Checklist

| Category | Required artifact |
|---|---|
| Source | Clean identified revision and exact created/modified file list. |
| Setup | Proven clean Windows setup instructions and lock hashes. |
| Run | Development application and engine discovery/setup instructions. |
| Tests | Complete matrix summary with Passed/Failed/Skipped/Not Run/Blocked. |
| Models/engines | Decision records, licenses, manifests, hashes, self-tests, hardware. |
| Outputs | Validated synthetic/permitted STL/GLB, four preview renders, reports. |
| Privacy/security | Network-deny, secret/log scan, package inventory, known risks. |
| Localization | Arabic-path evidence and current Arabic translation coverage. |
| Limitations | Deferred Stage 3 features, unsupported environments, performance, defects. |
| Approval | Explicit request to approve/reject Stage 2; no automatic Stage 3 work. |

## 19. Immediate Next Action After Planning Approval

After the owner approves this Stage 2 implementation plan, the owner binds the intended folder or provides the repository path. The implementation then performs M0 workspace reconnaissance and creates only B01. B02 does not begin until B01's configuration and secret/ignore checks pass.

## References

[1]: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html "Blender Command-Line Arguments"
