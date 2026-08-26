# MiniFigure 3D Studio — Implementation Roadmap

**Author:** Manus AI  
**Status:** Stage 1 proposal for approval  
**Delivery rule:** A stage does not advance until its acceptance tests run successfully, discovered defects are resolved or explicitly accepted, installation/run instructions are current, and every modified file is listed.

## 1. Roadmap Principles

Implementation should proceed through **risk-first vertical slices** rather than by building all screens before connecting real processing. Each milestone must produce an observable, testable behavior and a failure path. Synthetic images and generated mesh fixtures are used until the product owner explicitly supplies permitted test data outside the repository.

The desktop shell, AI engine, Blender scripts, COLMAP, viewer assets, model packs, and exporters have separate version manifests and tests. This prevents the core application from becoming inseparable from one GPU stack, license, or binary release.

## 2. Stage Gates

| Stage | Outcome | Entry condition | Exit condition |
|---|---|---|---|
| Stage 1 — Planning and Architecture | Approved design package | Complete requirements specification | Architecture, data flow, UI, dependencies/licenses, privacy/security, roadmap, risks, and repository structure approved. |
| Stage 2 — Working MVP | End-to-end Fast AI miniature workflow | Stage 1 approval and critical licensing decisions | Image import/validation, background mask/editing, one legally usable generation engine, local viewer, Blender cleanup, STL/GLB export, recovery, and relevant tests work on a supported Windows environment. |
| Stage 3 — Advanced Features | Production-oriented scan, color, report, localization, and installer | Stage 2 passes and unresolved platform spikes are closed | Accurate Scan, printable color/3MF, printability report, signed Windows installer, Arabic/English localization, and full release validation work. |

## 3. Stage 1 Completion Package

Stage 1 delivers only planning artifacts. No runtime test is claimed because application code is intentionally not created before approval.

| Deliverable | Artifact |
|---|---|
| Architecture | `architecture_document.md` and `system_architecture.png` |
| Data flow | `data_flow.png`, source diagram, and explanatory diagram document |
| UI design | `ui_ux_design.md` and `ui_workflow.png` |
| Dependencies and licenses | `dependency_license_register.md` |
| Security and privacy | `security_privacy_plan.md` |
| Implementation roadmap | This document |
| Risks | `risk_register.md` |
| Proposed structure | `proposed_project_structure.md` |

## 4. Pre-Stage 2 Decision Gate

The following decisions must be resolved or explicitly accepted before implementation begins.

| Decision | Required owner action | Recommended direction |
|---|---|---|
| Hunyuan3D territorial license | Confirm intended distribution territories and obtain qualified legal review | Treat Hunyuan as an optional territory-gated engine; identify a compliant alternative before worldwide claims. |
| Qt licensing path | Select open-source LGPL compliance or commercial Qt | Develop with dynamic LGPL-compatible packaging unless commercial terms are chosen; schedule formal release review. |
| Background model | Approve a model with suitable portrait quality and commercial redistribution rights | Benchmark several candidate weights behind a model-neutral adapter; forbid silent library-default selection. |
| Blender acquisition | Decide initial separate-install discovery versus managed runtime | Start with supported Blender LTS discovery; evaluate a managed package only after license/size/update spike. |
| COLMAP acquisition | Select a pinned Windows binary provenance | Use one reproducible or official package with complete dependency notices. |
| Product license | Choose application-shell license and distribution policy | Keep Blender scripts separately GPL-compatible; do not let the shell license obscure component obligations. |

## 5. Stage 2 — Working MVP Work Packages

### WP2.1 — Repository, Toolchain, and Quality Baseline

Create the Python 3.11 repository, packaging metadata, dependency groups, continuous integration, lint/type/test configuration, localization skeleton, asset manifests, and architecture decision records. Add a small PySide6 shell that starts without network access and displays its version and third-party notice entry point.

| Acceptance criterion | Verification |
|---|---|
| Clean Windows environment can create the development environment | Scripted setup on a clean Windows VM. |
| Core shell starts with outbound network denied | Automated smoke test. |
| Ruff, mypy, pytest, and license/SBOM checks run | CI evidence. |
| No secrets or real-person photos exist in the repository | Secret scan and asset manifest review. |
| Arabic path test workspace can be created | Automated filesystem test. |

### WP2.2 — Project Workspace and Recovery

Implement project creation/opening, schema-versioned manifest, generated safe filenames, immutable artifacts, atomic writes, job journal, interrupted-run detection, and deletion inventory. Build only the Home, New Project, and Recovery user interfaces necessary to verify these behaviors.

| Acceptance criterion | Verification |
|---|---|
| Project names and model names in Arabic round-trip correctly | Unit and integration tests on Windows. |
| Simulated process termination does not corrupt the last committed manifest | Fault-injection test. |
| Unexpected paths outside the project root are rejected | Path traversal and reparse-point fixtures. |
| Delete Project reports locked or remaining files honestly | Integration test with held file handle. |

### WP2.3 — Image Import and Quality Analysis

Implement drag/drop, managed-copy import, decoding, orientation normalization, thumbnails, cryptographic duplicate detection, perceptual near-duplicate grouping, resolution, blur, exposure, and subject-coverage adapter. Implement view assignment and a mode-specific quality report.

| Acceptance criterion | Verification |
|---|---|
| Supported synthetic images import without UI blocking | Qt responsiveness test. |
| Corrupt and unsupported files produce understandable errors | Fixture tests. |
| Exact and near duplicates are distinguished | Synthetic transform fixtures. |
| Blur/exposure results expose measured values and thresholds | Deterministic tests. |
| No image pixels or EXIF values appear in logs | Seeded-sensitive-data scan. |

### WP2.4 — Background Removal and Manual Masking

Implement the background-removal port, one approved local model adapter, engine asset manifest, explicit model installation, mask revision store, and manual add/erase/edge-refine editor. Preserve source images and support undo/redo and checkpoints.

| Acceptance criterion | Verification |
|---|---|
| Selected model license and checksum are shown before installation | UI/manifest test. |
| No silent model download occurs | Network-deny test. |
| Mask failure leaves the user with retry, alternate adapter, or manual path | Fault injection. |
| Manual edits survive restart | Recovery test. |
| Source image hash is unchanged | Before/after checksum test. |

### WP2.5 — Process Supervisor and Protocol

Implement `QProcess` supervision, versioned request/result envelopes, progress events, cooperative cancellation, process-tree termination, redacted logs, capability-gated pause, retry rules, and checkpoint validation. Use fake executables before real engines.

| Acceptance criterion | Verification |
|---|---|
| GUI heartbeat remains responsive while a fake job runs | Automated Qt test. |
| Zero exit with missing/malformed result is a failure | Contract test. |
| Cancellation stops the process tree and discards uncommitted output | Process integration test. |
| A crash preserves the last committed checkpoint | Recovery test. |
| Copy Error contains no seeded secret or sensitive path | Redaction test. |

### WP2.6 — One Working Fast AI Adapter

Implement the generator port, capability declaration, primary-image selection, supplementary-reference analysis as a separate service, engine preflight, and one legally usable local or external adapter. If Hunyuan3D is used, run it in a separate environment, enforce the territory/license gate, report the upstream single-primary-image behavior honestly, and expose geometry versus texture resource requirements.

| Acceptance criterion | Verification |
|---|---|
| Adapter never receives supplementary images unless its declared capability supports them | Contract test. |
| Insufficient VRAM produces a specific recommendation rather than a native traceback | GPU/fake-capability test. |
| Engine/license block occurs before source-image staging | Integration test. |
| Raw mesh is non-empty, reopens, and has plausible bounds before commit | Artifact validator. |
| An actual failed generation never promotes an old or placeholder mesh | Run-ID/provenance test. |

A Stage 2 success requires one engine that is both technically functional and legally usable in the intended test environment. Hunyuan3D cannot be treated as universally available under the reviewed community license.

### WP2.7 — Offline Integrated 3D Viewer

Bundle a pinned Three.js build, GLTF loader, controls, and local viewer assets. Implement Qt WebChannel messages for loading a preview artifact, camera controls, view modes, part visibility, and screenshot export. Block remote requests and navigation.

| Acceptance criterion | Verification |
|---|---|
| Viewer works with outbound network denied | Integration test. |
| GLB loads from an Arabic project path through the controlled cache/bridge | Windows test. |
| Remote URL, popup, and arbitrary local-file requests are blocked | Security test. |
| Renderer crash can be recovered without losing project state | Fault injection. |

### WP2.8 — Blender Cleanup MVP

Implement separate GPL-compatible Blender scripts and a pipeline runner for import, backup, component cleanup, merge by distance, normals, hole/non-manifold analysis, conditional repair, conservative decimation, base union, Z=0 placement, millimeter scaling, and four previews. Start with synthetic mesh fixtures before an AI-generated mesh.

| Acceptance criterion | Verification |
|---|---|
| Supported Blender version passes a self-test and result-protocol test | Real Blender integration test. |
| Raw artifact is never overwritten | Hash verification. |
| Each operation records before/after metrics | Result-envelope inspection. |
| Boolean failure preserves pre-Boolean artifact and reports a useful error | Fixture test. |
| Requested height is achieved within tolerance and minimum Z is zero within tolerance | Geometry test. |
| Preview renders exist and correspond to the processed artifact hash | Reopen/report test. |

### WP2.9 — MVP Validation, STL, and GLB Export

Implement the minimum printability report needed to block clearly invalid export, transactional staging, independent reopen, and STL/GLB finalization. The Stage 2 report may be narrower than the complete Stage 3 report but must not mislabel failed geometry as ready.

| Acceptance criterion | Verification |
|---|---|
| Empty or malformed output cannot be finalized | Export fault tests. |
| STL and GLB reopen and retain expected dimensions | Independent parser tests. |
| GLB contains expected meshes and materials where supported | Scene inventory test. |
| Destination permission failure is explained and no empty success file remains | Filesystem test. |
| Export report records source hash, versions, dimensions, warnings, and file hashes | Schema test. |

### WP2.10 — MVP Hardening and Approval Demonstration

Run the complete Fast AI workflow on the supported Windows test matrix using synthetic or approved non-repository inputs. Validate recovery, cancellation, offline behavior, Arabic paths, installation instructions, and known limitations. Do not begin Stage 3 until the owner approves the working MVP and accepts open limitations.

## 6. Stage 2 Definition of Done

Stage 2 is complete only when all required tests have actually run and their results are recorded. The file list, installation guide, run guide, dependency/engine versions, known limitations, unresolved defects, and licensing status must accompany the demonstration.

| Required outcome | Completion evidence |
|---|---|
| Image import and validation | Automated results plus UI demonstration. |
| Background removal and mask correction | Approved model manifest, automated tests, and editor demonstration. |
| One generation engine | Real successful and real failing runs with truthful reports. |
| Integrated preview | Offline viewer test and screenshot. |
| Blender cleanup | Fixture metrics and processed model demonstration. |
| STL/GLB export | Reopen validation reports. |
| Responsiveness/cancel/recovery | Process and UI test evidence. |
| Arabic paths | Windows integration results. |

## 7. Stage 3 — Advanced Features Work Packages

### WP3.1 — Accurate Scan Preflight and Capture Coverage

Add the 24–80 photo workflow, capture guide, quality thresholds for reconstruction, angle bins, disk estimate, COLMAP discovery/install, and preflight self-test. Estimated pre-reconstruction coverage must be labeled separately from reconstructed camera coverage.

### WP3.2 — COLMAP Sparse Reconstruction

Implement feature extraction, matching strategy, sparse mapper, camera/point-cloud parsing, registration thresholds, real progress/log mapping, and missing-angle visualization from reconstructed cameras. A sparse failure blocks dense stages.

### WP3.3 — COLMAP Dense Reconstruction and Meshing

Add undistortion, dense stereo, fusion, meshing, checkpointing, disk cleanup, and actual failure categorization. Benchmark CPU/GPU paths and do not expose options that are unsupported in the selected COLMAP build.

### WP3.4 — Advanced Styles and Printable Features

Implement and test Chibi, Cartoon, Bobblehead, Bust, Keychain, Bas-Relief, custom presets, fragile-feature strengthening, name emboss/engrave, hollowing, and resin drain holes. Each operation requires geometric fixtures and before/after metrics.

### WP3.5 — Complete Printability Report

Add watertight, non-manifold, disconnected, dimensions, polygons, wall thickness, floating parts, internal geometry, overhang, build-plate contact, recommended orientation, and support-estimate validators. Connect every location-aware finding to a red viewer overlay.

### WP3.6 — Printable Color Separation

Implement semantic/material/texture-assisted regions, palette quantization for 4/8/16 slots, manual reassignment, merging similar colors, tiny-region control, independent part lists, and profile-specific minimums. Document uncertainty and require user review.

### WP3.7 — 3MF Export and Slicer Interoperability

Use lib3mf for creation and validation. Add synthetic golden fixtures and write-read round trips for 1/4/8/16 colors. Test exact supported releases of Orca Slicer and Creality Print and record recognized objects, material slots, transforms, and units.

### WP3.8 — Full Export Suite

Complete OBJ/MTL/textures and BLEND exports, independent reopen checks, relative-resource packaging, and reports. Ensure PBR texture mode and printable filament mode remain separate.

### WP3.9 — Arabic and English Completion

Translate every user-facing string, help page, error/remediation message, report label, capture instruction, and installer string. Run RTL/LTR screenshots, keyboard navigation, display scaling, mixed-direction text, and Arabic-path tests.

### WP3.10 — Windows Installer and Engine Packages

Create native Windows PyInstaller builds, installer project, code signing, upgrade/repair/uninstall, license/notice bundle, optional engine/model packages, checksums, rollback, and clean-machine tests. The release must include SBOM and source/offer materials required by shipped licenses.

### WP3.11 — Privacy, Security, and Release Hardening

Run dependency audits, secret scans, network-deny tests, viewer security tests, malformed-file/resource-limit tests, deletion tests, external-consent tests, and release manifest verification. Conduct a qualified license/compliance review before public distribution.

## 8. Stage 3 Definition of Done

The product is not release-ready until both generation modes, complete validation, color separation, 3MF interoperability, localization, installer, and privacy/security gates pass on supported Windows configurations. The release notes must state hardware limits, supported engine/slicer versions, territorial availability, known reconstruction limitations, and the exact meaning of “Ready to Print.”

## 9. Test Execution and Reporting Policy

Every milestone report contains the command or test job identifier, environment, engine/model versions, counts of passed/failed/skipped tests, failure details, and artifact links. A skipped test is not a pass. A manual test must identify the tester, steps, expected result, actual result, and evidence.

After each stage, the project must provide installation and run instructions, list every created or modified file, explain unresolved or unsupported features, and stop for approval. This roadmap explicitly preserves the user's requirement not to continue automatically into the next stage.
