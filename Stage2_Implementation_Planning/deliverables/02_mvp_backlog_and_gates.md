# MiniFigure 3D Studio — Stage 2 MVP Backlog and Acceptance Gates

**Author:** Manus AI  
**Status:** Implementation plan; no application code is included  
**Planning model:** Sequential risk-first milestones with explicit entry, exit, and stop conditions

## 1. Delivery Strategy

Stage 2 should not be implemented as a screen-by-screen mockup followed by late engine integration. It should proceed as a series of **testable vertical slices** that establish truthful persistence and process behavior first, then connect image, viewer, Blender, generation, and export integrations one at a time.

A milestone is complete only when its mandatory automated tests run successfully in the stated environment, manual checks have evidence, documentation is updated, and all modified files are listed. A disabled, mocked, skipped, or unexecuted test is not evidence that a real integration works.

## 2. Milestone Sequence

| Order | Milestone | Primary outcome | Depends on |
|---:|---|---|---|
| M0 | Decisions and workspace readiness | Bound repository, approved development assumptions, selected test environments, license decisions recorded | Stage 1 approval |
| M1 | Repository and quality foundation | Python 3.11 project, CI/static checks, schemas, documentation skeleton, synthetic asset policy | M0 |
| M2 | Domain, project storage, and recovery | Immutable artifacts, atomic manifest, job journal, schema migration, safe deletion inventory | M1 |
| M3 | Minimal bilingual desktop shell | Responsive PySide6 shell, navigation, project creation/open/recovery, theme, translation infrastructure | M2 |
| M4 | Worker protocol and process supervision | Fake engines, structured progress, cancellation, retry, redacted errors, process-tree cleanup | M2–M3 |
| M5 | Image import, assignment, and quality | Drag/drop, safe managed copies, thumbnails, duplicates, blur/exposure/resolution, primary-image selection | M3–M4 |
| M6 | Background removal and mask editing | Approved model adapter, explicit installation, non-destructive revisions, manual editor | M5 |
| M7 | Offline 3D viewer | Local Three.js build, secure Qt bridge, synthetic GLB loading, camera/view controls, screenshots | M3–M4 |
| M8 | Blender cleanup vertical slice | Real Blender discovery/self-test, mesh backup/cleanup/base/scale/previews, structured result | M4 and M7 |
| M9 | One real Fast AI generation adapter | Legally usable adapter, hardware/license preflight, real success and failure, raw artifact validation | M4–M6; M0 engine decision |
| M10 | End-to-end pipeline orchestration | Primary image through generation, preview, Blender processing, recovery, and retry | M5–M9 |
| M11 | Minimum printability and transactional STL/GLB export | Blocking validation, staged writes, independent reopen, atomic finalize, export report | M8–M10 |
| M12 | MVP hardening and approval candidate | Windows evidence, offline/privacy/Arabic-path tests, setup/run docs, limitations, full file manifest | M1–M11 |

M7 and the early fixture portion of M8 can proceed before M9 because synthetic GLB and mesh fixtures do not depend on a licensed AI engine. M9 may begin as a fake-adapter contract earlier, but real engine enablement remains blocked until the relevant territory, model, credentials, and hardware gates pass.

## 3. Milestone M0 — Decisions and Workspace Readiness

M0 converts the conditional Stage 1 approval into an implementation-ready record. No production adapter is enabled before this gate.

| Backlog ID | Work item | Completion evidence |
|---|---|---|
| M0-01 | Bind the intended project folder or identify the existing repository and branch policy | Workspace path and repository status recorded. |
| M0-02 | Confirm intended development and distribution territories | Written territory decision; Hunyuan eligibility derived but not presented as legal advice. |
| M0-03 | Confirm product-shell license posture | Selected license or “private development only pending decision” recorded. |
| M0-04 | Confirm Qt development path | Dynamic LGPL-oriented architecture or commercial Qt choice recorded. |
| M0-05 | Select supported Windows development/test environments | OS editions/builds, GPU availability, disk/RAM, and clean-VM strategy recorded. |
| M0-06 | Select Blender acquisition baseline | Supported separately installed Blender LTS discovery approved for MVP. |
| M0-07 | Select candidates for background-removal benchmark | Candidate model IDs, licenses, revisions, and asset sources recorded. |
| M0-08 | Select the real generation adapter path | Hunyuan where eligible, compliant alternative local engine, or named external provider. |

**M0 exit gate:** Workspace is usable, no unresolved decision is being silently assumed, and any integration still blocked is represented by a fake adapter and a visible disabled capability rather than a partial production path.

## 4. Milestone M1 — Repository and Quality Foundation

M1 establishes enforceable engineering controls before feature code.

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M1-01 | Create the approved repository directories and package metadata | Importable package skeleton; no unused giant module or generated engine assets. |
| M1-02 | Configure Python 3.11 development dependencies | Reproducible environment instructions work on the first native Windows machine. |
| M1-03 | Configure Ruff, mypy, pytest, pytest-qt, coverage, pip-audit, and SBOM tooling | All commands run; any baseline exception is explicit and narrow. |
| M1-04 | Add `.gitignore`, `.gitattributes`, `.env.example`, security/privacy templates, and contribution rules | Secret/model/project/cache patterns excluded; no credential values. |
| M1-05 | Add JSON schemas for project, engine manifest, worker request/result, and validation report | Schema validation tests pass with valid/invalid fixtures. |
| M1-06 | Add application version and build metadata | Shell and diagnostic output can report one canonical version. |
| M1-07 | Add synthetic asset manifest policy and generator entry point | Repository binary scan finds no unmanifested real-person image. |
| M1-08 | Add architecture boundary tests | Domain/models cannot import PySide6, HTTP clients, Blender, or engine packages. |

**M1 exit gate:** Static checks and the initial test suite pass on Windows; no user data, engine weights, secret, or real-person photo exists in the repository.

## 5. Milestone M2 — Domain, Project Storage, and Recovery

M2 proves that state can survive crashes before long-running engines exist.

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M2-01 | Implement project, source image, artifact, run, stage result, error, engine, and consent value objects | Type/invariant tests cover valid and invalid construction. |
| M2-02 | Implement safe project names and generated internal IDs | Arabic display names round-trip; filesystem paths do not use untrusted display names directly. |
| M2-03 | Implement atomic manifest writer and replace-on-success commit | Forced interruption leaves the prior manifest readable. |
| M2-04 | Implement immutable artifact records with hash, producer, run ID, stage ID, and parent links | Artifact mutation or provenance mismatch is detected. |
| M2-05 | Implement staging directories and checkpoint registry | Uncommitted staging is never listed as a valid project artifact. |
| M2-06 | Implement job journal and interrupted-run detection | Startup identifies a simulated abandoned running stage and offers recovery. |
| M2-07 | Implement schema versioning and migration registry | Unknown future versions open read-only; tested old version migrates deterministically. |
| M2-08 | Implement deletion inventory and canonical-root/reparse-point guards | Outside-root paths are rejected; locked files produce a remaining-items report. |
| M2-09 | Implement redacted structured logging and bounded local retention | Seeded secrets, full sensitive paths, and image content markers never appear. |

**M2 exit gate:** Crash, path, Unicode, schema, and deletion tests pass without a GUI. The project repository is the only authority for artifact promotion.

## 6. Milestone M3 — Minimal Bilingual Desktop Shell

M3 exposes only the UI needed to exercise M2 safely.

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M3-01 | Application bootstrap and dependency composition root | Startup errors are caught and displayed without a raw traceback. |
| M3-02 | Navy/white/gold theme tokens and high-DPI behavior | UI remains usable at 100%, 125%, 150%, and 200% scaling on the test machine. |
| M3-03 | Main window, grouped navigation, title/save state, and activity drawer shell | Keyboard navigation and accessible labels exist. |
| M3-04 | English translation catalog and Arabic catalog skeleton | Runtime language switch changes direction and strings that exist. |
| M3-05 | Home/recent projects and New Project flow | Project can be created and reopened through UI. |
| M3-06 | Mode selection with Fast AI enabled and Accurate Scan visibly deferred | Deferred mode is explained; no fake reconstruction button. |
| M3-07 | Recovery and Delete Project dialogs | Interrupted project and partial deletion states are truthful. |
| M3-08 | Third-party notices and dependency settings entry points | User can reach current development manifests. |

**M3 exit gate:** Shell startup, project create/open/recover/delete, RTL direction, keyboard focus, and Arabic path tests pass; no long task blocks the GUI thread.

## 7. Milestone M4 — Worker Protocol and Process Supervision

M4 is the reliability backbone for all engines.

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M4-01 | Define versioned worker request, progress-event, result, and error envelopes | Schema and backward-compatibility tests pass. |
| M4-02 | Implement task state machine | Illegal transitions are rejected; terminal states cannot return to running. |
| M4-03 | Implement `QProcess` argument-vector runner and minimal environment builder | Spaces, quotes, metacharacters, and Arabic paths pass without a shell. |
| M4-04 | Implement fake success, failure, malformed-result, hang, child-process, and secret-echo workers | Each behavior has a deterministic integration test. |
| M4-05 | Implement real/indeterminate progress and Activity Center binding | UI heartbeat remains responsive and progress never invents percentages. |
| M4-06 | Implement cooperative cancellation, grace period, and process-tree termination | Parent and child processes end; no staged output is promoted. |
| M4-07 | Implement capability-gated Pause and retry policy | Pause is absent/disabled for non-resumable fake engine; retry states are explicit. |
| M4-08 | Implement redacted simplified log, technical details, and Copy Error | Seeded secrets and unsafe paths are removed from all three views. |
| M4-09 | Validate result file, run/stage identity, hashes, and expected artifacts after exit | Zero exit with missing, stale, malformed, or empty result is Failure. |

**M4 exit gate:** All fake-engine failure modes pass on Windows, and a deliberate kill/restart preserves the last committed project state.

## 8. Milestone M5 — Image Import, Assignment, and Quality

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M5-01 | Supported-image validator and safe decoder boundary | Corrupt/oversized/unsupported fixtures fail with stable codes. |
| M5-02 | Drag/drop and file/folder picker import | UI remains responsive; skipped files and reasons are listed. |
| M5-03 | Immutable managed copy, source hash, normalized working copy, and thumbnail | External original hash and timestamp are not modified. |
| M5-04 | EXIF orientation and metadata inventory | Orientation is correct; sensitive metadata is not logged. |
| M5-05 | Exact hash duplicate and perceptual near-duplicate grouping | Synthetic duplicate transforms produce expected groups. |
| M5-06 | Resolution, blur, exposure, and visible-subject coverage findings | Each finding reports measurement, threshold, impact, and action. |
| M5-07 | View assignment model and Front/Back/Left/Right/Front Left/Front Right UI | Assignment persists and keyboard alternative works. |
| M5-08 | Primary-image selector and manual override | One front/45-degree candidate is selected with explained signals; user choice persists. |
| M5-09 | Fast AI photo-count and blocking-quality policy | 1–6 input rules and no-primary conditions are tested. |

**M5 exit gate:** Synthetic image fixture suite passes, import/analysis does not freeze the UI, and project logs contain no pixels, EXIF thumbnails, or unsafe personal metadata.

## 9. Milestone M6 — Background Removal and Mask Editing

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M6-01 | Background-remover port and model capability/manifest schema | Fake model contract passes before real weights. |
| M6-02 | Candidate-model benchmark and rights record | Selected model has version, source, hash, license hash, quality notes, and explicit owner approval. |
| M6-03 | Explicit model installation and self-test | No silent first-use download; checksum mismatch blocks installation. |
| M6-04 | Local worker inference with CPU baseline | Progress/cancel/failure paths work; UI process memory remains bounded. |
| M6-05 | Original/Mask/Cutout review | Result is linked to source/model revision and cannot replace the source. |
| M6-06 | Non-destructive brush add/remove, zoom/pan, undo/redo | Deterministic mask revision tests pass. |
| M6-07 | Autosave/checkpoint and restart recovery | Manual edits survive application restart. |
| M6-08 | Manual-only fallback | User can produce an approved mask when automatic removal is unavailable or fails. |

**M6 exit gate:** Automatic or manual mask produces a valid, approved revision; source hash is unchanged; no model was downloaded or executed without a validated manifest.

## 10. Milestone M7 — Offline 3D Viewer

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M7-01 | Pin and vendor Three.js, loader, and controls source | Exact version/license recorded; build does not require a CDN at runtime. |
| M7-02 | Build local viewer bundle and asset manifest | Deterministic build output is validated. |
| M7-03 | Qt WebEngine host and request interceptor | HTTP/HTTPS, popup, navigation, and arbitrary file requests are blocked. |
| M7-04 | Narrow schema-validated WebChannel bridge | Unknown messages and paths outside viewer cache are rejected. |
| M7-05 | Load synthetic GLB through generated read-only viewer cache | Arabic project path works without exposing original path to JavaScript. |
| M7-06 | Rotate, zoom, pan, standard views, material/solid/wireframe, fit | Automated state tests plus manual interaction evidence. |
| M7-07 | Part tree visibility/isolation and screenshot export | Part state matches scene inventory; screenshot requires user action. |
| M7-08 | Renderer/process crash recovery | Project remains open and viewer can be recreated. |

**M7 exit gate:** Viewer operates with outbound networking denied and passes malformed model/metadata security fixtures.

## 11. Milestone M8 — Blender Cleanup Vertical Slice

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M8-01 | Discover and validate one supported Blender LTS executable | Self-test records version, executable hash/path alias, Python/API capability, and script protocol. |
| M8-02 | Create separate GPL-compatible script component and protocol | Source/license notices exist; request/result fixtures pass. |
| M8-03 | Import supported raw mesh and create backup | Raw artifact hash remains unchanged and backup reopens. |
| M8-04 | Measure components, dimensions, polygons, boundary/non-manifold counts, and bounds | Known synthetic fixtures produce expected metrics. |
| M8-05 | Remove small disconnected artifacts with protected-main-component policy | Main object retained; fixture islands removed according to threshold. |
| M8-06 | Merge by Distance, recalculate normals, and conservative hole repair | Before/after metrics and unchanged protected cases verified. |
| M8-07 | Conditional non-manifold repair/remesh and conservative decimation | Operations run only when triggered; surface-deviation limit is recorded. |
| M8-08 | Add simple circular/square base and Boolean union with preserved fallback | Success and deliberate failure fixtures retain correct checkpoints. |
| M8-09 | Place bottom at Z=0, convert/interpret units, and scale to 40–250 mm | 40, 100, and 250 mm cases pass defined tolerance. |
| M8-10 | Render front/back/left/right previews | Four non-empty images are tied to the processed artifact hash. |
| M8-11 | Return structured operation metrics and errors | Missing artifact or zero exit with invalid result fails. |

**M8 exit gate:** Real Blender integration tests pass using synthetic meshes; no AI-generated asset is needed to prove cleanup mechanics.

## 12. Milestone M9 — One Real Fast AI Adapter

M9 has a mandatory eligibility preflight. If Hunyuan is ineligible or unavailable, another approved local adapter or an explicitly selected external provider must satisfy the same port.

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M9-01 | Generator port and capability model | Fake adapters prove single/multi-image, texture, local/remote, CPU/GPU/Auto, pause, and resource declarations. |
| M9-02 | License/territory/capability gate | Block occurs before copying an image to engine staging. |
| M9-03 | Isolated engine environment and manifest | Python/runtime/dependency/model hashes and protocol range are recorded. |
| M9-04 | CPU/GPU/Auto selection semantics | Unsupported choices are disabled or fail preflight with an actionable explanation. |
| M9-05 | VRAM/RAM/disk/runtime self-test | Insufficient resource condition maps to stable error and documented fallback where truly supported. |
| M9-06 | Primary-image-only request for single-image adapter | Contract test proves supplementary images do not enter engine request/staging. |
| M9-07 | Run local or consented remote generation | Real success produces a non-empty raw mesh; real controlled failure produces no promoted artifact. |
| M9-08 | Validate result provenance, geometry inventory, bounds, and optional PBR resources | Stale, empty, implausible, or malformed outputs are rejected. |
| M9-09 | Preserve raw result and generation report | Engine/model versions, request parameters, timing, warnings, and hashes recorded without secrets. |

**M9 exit gate:** At least one legally usable engine succeeds in the intended test environment and also passes actual failure, cancellation, resource, and stale-output tests.

## 13. Milestone M10 — End-to-End Fast AI Orchestration

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M10-01 | Define Fast AI stage graph and invalidation rules | Changing primary image/mask/style/dimensions invalidates only dependent artifacts. |
| M10-02 | Generation review summary | Shows local/external status, exact primary input role, engine/device, dimensions, and consent requirement. |
| M10-03 | Orchestrate approved mask → generation → raw preview → Blender → processed preview | Real artifact lineage is visible and recoverable. |
| M10-04 | Connect Activity Center to every stage | Progress, indeterminate states, cancel, retry, and error details reflect current stage. |
| M10-05 | Implement checkpoint/resume policy | Retry clearly states whether it restarts or resumes; unsupported Pause is not offered. |
| M10-06 | Compare raw and processed artifacts | Viewer switches only between validated current-run artifacts. |
| M10-07 | Prevent concurrent invalidating edits | Settings lock or explicit cancel/restart behavior is tested. |

**M10 exit gate:** One real image-to-processed-model run succeeds end to end, a forced failure at each external boundary remains truthful, and restart/recovery preserves the last committed artifact.

## 14. Milestone M11 — Minimum Validation and Transactional Export

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M11-01 | Minimum topology, disconnected-object, dimensions, polygons, and build-plate validators | Known-good/bad fixtures produce expected findings. |
| M11-02 | Derive Ready, Warning, and Repair Required with qualified wording | Blocking findings cannot be overridden without an explicit unsupported-development mode that is absent from normal UI. |
| M11-03 | Export option resolver for STL and GLB | Invalid combinations or missing materials are explained. |
| M11-04 | Transactional export directory and naming | Failure leaves no empty final file and does not overwrite an existing file silently. |
| M11-05 | STL write and independent reopen | Geometry non-empty, dimensions within tolerance, and source run ID in report. |
| M11-06 | GLB write and independent structure/scene/material reopen | Mesh and material inventory matches the processed artifact where supported. |
| M11-07 | Export report and hashes | Versions, input/output hashes, dimensions, warnings, and validation status recorded. |
| M11-08 | Unwritable path, disk-full simulation, cancellation, stale output, and malformed output tests | Every condition ends in failure with cleanup/remaining-item details. |

**M11 exit gate:** Valid STL/GLB exports reopen and pass defined checks; invalid outputs never become final successes.

## 15. Milestone M12 — MVP Hardening and Approval Candidate

| Backlog ID | Work item | Acceptance |
|---|---|---|
| M12-01 | Run complete automated suite on the designated Windows environment | Report includes passed, failed, skipped, duration, versions, and environment. |
| M12-02 | Run Windows 10/11 smoke matrix as available | Unsupported/unavailable matrix entries are disclosed, never marked passed. |
| M12-03 | Run outbound-network-denied local workflow | No unexpected connection attempt. |
| M12-04 | Run Arabic path and RTL critical-flow matrix | Create/import/process/view/export paths pass; known untranslated strings listed. |
| M12-05 | Run secrets/logs/diagnostic scan | No seeded secret, image content, or unsafe full path appears. |
| M12-06 | Produce development packaging smoke artifact | Starts on a clean supported machine; not represented as the production installer. |
| M12-07 | Prepare setup, run, troubleshooting, architecture, license, and known-limitations documents | Instructions are executed from a clean environment. |
| M12-08 | Produce exact created/modified file list and Stage 2 test evidence | Every file and result is attached to the approval package. |
| M12-09 | Demonstrate successful and failing end-to-end runs | Screenshots/log excerpts are redacted and tied to report IDs. |

**M12 exit gate:** The product owner receives a working MVP, installation/run instructions, evidence, limitations, unresolved defects, and the exact file list. Work stops for Stage 2 approval; Stage 3 does not begin automatically.

## 16. Global Stop Conditions

| Condition | Required action |
|---|---|
| Required workspace is not bound or path is not confirmed | Do not create application source. Continue planning only. |
| A production model/engine lacks clear permitted use | Keep adapter disabled; use fake contract tests; escalate decision. |
| UI heartbeat fails | Stop feature progression and move blocking work out of the GUI thread. |
| A process returns success without valid current-run artifacts | Treat as failure and fix result validation before continuing. |
| A test is skipped due to missing environment | Report it as skipped; do not satisfy the gate. |
| A change breaks previously passed milestone tests | Stop and restore the regression suite before advancing. |
| A log or bundle leaks seeded sensitive data | Block milestone and release; repair redaction and rerun scans. |
| Blender operation exceeds deviation or corrupts fixture geometry | Revert to checkpoint and revise the operation; do not accept visual plausibility alone. |
| Real generator cannot be legally or technically operated | Select another approved adapter; Stage 2 cannot close with only a fake generator. |

## 17. Stage 2 Approval Evidence Index

The Stage 2 closeout package should contain the final test report, environment manifest, engine/model manifests, SBOM, license/notice snapshot, screenshots of the critical flow, validated sample STL/GLB derived from synthetic or permitted inputs, generated Blender preview renders, redacted successful/failing job records, setup and run instructions, known limitations, unresolved risks, and the exact changed-file inventory.
