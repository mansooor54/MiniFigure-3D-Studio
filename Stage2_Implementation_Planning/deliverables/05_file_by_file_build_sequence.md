# MiniFigure 3D Studio — Stage 2 File-by-File Build Sequence

**Author:** Manus AI  
**Status:** Implementation sequence; no files listed here have been created in an application repository  
**Rule:** Each batch is completed, tested, documented, and reviewed before the next batch changes application behavior.

## 1. Sequence Rules

The implementation should create the smallest coherent batch of files that can be verified. Empty placeholder modules are avoided. A file is created when the immediately following test or behavior needs it. Every batch report lists files created, files modified, tests added, commands run, results, and unresolved defects.

Blender scripts remain in a separate GPL-compatible component because they use Blender's Python API.[1] The Three.js viewer source remains separate from its generated static bundle and uses a pinned local dependency rather than a CDN.[2]

## 2. Batch Index

| Batch | Milestone | Deliverable | Gate before continuing |
|---:|---:|---|---|
| B01 | M1 | Repository metadata and policy files | Static tool configuration parses. |
| B02 | M1 | Test foundation and synthetic-asset policy | Initial suite passes. |
| B03 | M1–M2 | Core domain primitives and schemas | Domain/schema tests pass. |
| B04 | M2 | Safe paths and atomic filesystem | Fault/path tests pass. |
| B05 | M2 | Project repository, artifacts, journal, recovery | Crash/recovery tests pass. |
| B06 | M2 | Structured logging, redaction, settings | Seeded-sensitive-data tests pass. |
| B07 | M3 | PySide6 bootstrap, theme, translations | Headless/startup UI tests pass. |
| B08 | M3 | Home, project creation, mode, recovery UI | Project UI integration passes. |
| B09 | M4 | Worker protocol and task state machine | Pure contract tests pass. |
| B10 | M4 | `QProcess` supervisor and fake workers | Process/fault tests pass. |
| B11 | M4 | Activity Center and error presentation | Responsiveness/redaction UI tests pass. |
| B12 | M5 | Image domain/import/decoder | Safe import tests pass. |
| B13 | M5 | Quality/duplicate/primary selection services | Deterministic fixture tests pass. |
| B14 | M5 | Import/view/quality UI | Drag/drop and persistence tests pass. |
| B15 | M6 | Background-remover contract and engine asset rules | Fake-model and manifest tests pass. |
| B16 | M6 | Real approved mask adapter and worker | Self-test/inference/cancel tests pass. |
| B17 | M6 | Non-destructive mask editor | Undo/restart/source-integrity tests pass. |
| B18 | M7 | Viewer source, lockfile, and deterministic bundle | Viewer unit/build tests pass. |
| B19 | M7 | Secure Qt WebEngine bridge | Offline/network/path tests pass. |
| B20 | M8 | Blender protocol, self-test, scene I/O, metrics | Real Blender protocol tests pass. |
| B21 | M8 | Blender cleanup, base, scale, previews | Synthetic mesh suite passes. |
| B22 | M9 | Generator contract, engine registry, preflight | Fake generator matrix passes. |
| B23 | M9 | One real approved generator adapter | Real success/failure/cancel tests pass. |
| B24 | M10 | Fast AI orchestration and generation UI | End-to-end processing/recovery passes. |
| B25 | M11 | Minimum validators and statuses | Known-good/bad fixtures pass. |
| B26 | M11 | Transactional STL/GLB export | Independent reopen tests pass. |
| B27 | M12 | Packaging smoke, docs, full evidence | Stage 2 candidate gate passes. |

## 3. B01 — Repository Metadata and Policy

Create these root files in order because later tooling depends on them.

| Order | File | Purpose | Immediate verification |
|---:|---|---|---|
| 1 | `README_EN.md` | Stage 2 development scope, current status, setup links | Markdown renders and does not claim implemented features. |
| 2 | `README_AR.md` | Arabic project introduction/status skeleton | UTF-8 and RTL content render correctly. |
| 3 | `LICENSE` | Owner-selected shell license or explicit private-development notice | M0 decision matches file. |
| 4 | `THIRD_PARTY_NOTICES.md` | Generated/maintained notice index | Empty sections are labeled “not yet redistributed,” not silently omitted. |
| 5 | `SECURITY.md` | Reporting, secret handling, supported-development status | No support address is invented. |
| 6 | `PRIVACY.md` | Local-first development policy | Matches Stage 1 privacy plan. |
| 7 | `CONTRIBUTING.md` | Type/test/file/report rules | Includes no-real-person-fixtures rule. |
| 8 | `CHANGELOG.md` | Stage and milestone change record | Initial entry identifies planning-to-implementation transition. |
| 9 | `.gitignore` | Exclude virtual env, caches, secrets, projects, engines, models, generated viewer, build output | Seed files under excluded paths are ignored. |
| 10 | `.gitattributes` | Text normalization and binary declarations | Arabic/JSON/Python remain UTF-8 text; model/images marked binary. |
| 11 | `.env.example` | Optional provider variable names only | Secret scanner finds no value. |
| 12 | `pyproject.toml` | Package/tool configuration | Build metadata parses; Ruff/mypy/pytest discover config. |
| 13 | `requirements.txt` | Direct core requirements synchronized with metadata | Resolver dry run succeeds in selected Windows environment. |
| 14 | `requirements-dev.txt` | Direct development requirements | Development resolver succeeds. |
| 15 | `.python-version` | Selected core Python 3.11 patch | Matches environment report. |

**Run after B01:** configuration parse, secret scan, repository ignored-file test, and dependency-resolution report. Do not freeze lock files until native smoke tests pass.

## 4. B02 — Test and Synthetic-Asset Foundation

| Order | File | Purpose | Immediate verification |
|---:|---|---|---|
| 1 | `tests/conftest.py` | Shared temporary project roots, deterministic clock/IDs, Qt fixture boundary | One empty smoke test collects. |
| 2 | `tests/fixtures/asset_manifest.yaml` | Source/license/hash/expected-result inventory | Schema validates and contains no real-person asset. |
| 3 | `scripts/create_synthetic_fixtures.py` | Generate patterns/images and mesh fixture inputs deterministically | Repeated run produces identical hashes where promised. |
| 4 | `scripts/validate_assets.py` | Reject unmanifested binaries, unexpected EXIF, real-person-risk extensions without record | Seeded unmanifested file fails. |
| 5 | `scripts/generate_sbom.py` | Produce development SBOM | Runs on resolved environment. |
| 6 | `scripts/collect_licenses.py` | Collect installed-package license metadata for review | Output includes all direct dependencies. |
| 7 | `.github/workflows/quality.yml` | Portable lint/type/unit/asset/security lane | Workflow syntax validates; local equivalent passes. |
| 8 | `docs/testing_strategy.md` | Test tiers and evidence format | Matches Stage 2 matrix. |

## 5. B03 — Domain Primitives and Schemas

Create schemas before persistence adapters and keep domain modules free of PySide6, HTTP, Blender, and engine imports.

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/__init__.py` | Package version export boundary | Import test. |
| 2 | `app/application_info.py` | Product ID/version/schema constants | Single-source version test. |
| 3 | `app/models/error_info.py` | Stable error code, category, retryability, safe details | `tests/unit/test_error_info.py` |
| 4 | `app/models/stage_result.py` | Terminal status and validated artifact references | `tests/unit/test_stage_result.py` |
| 5 | `app/models/pipeline_run.py` | Run/stage IDs, state, timing, engine/version references | `tests/unit/test_pipeline_run.py` |
| 6 | `app/models/mesh_artifact.py` | Immutable artifact/provenance metadata | `tests/unit/test_artifact_model.py` |
| 7 | `app/models/source_image.py` | Source/display identity without unsafe filename authority | `tests/unit/test_source_image.py` |
| 8 | `app/models/project.py` | Project identity, schema version, current artifacts, settings references | `tests/unit/test_project_model.py` |
| 9 | `app/models/generator_capabilities.py` | Adapter capabilities and device modes | `tests/unit/test_generator_capabilities.py` |
| 10 | `app/models/engine_manifest.py` | Version, license, territory, hashes, protocol, self-test | `tests/unit/test_engine_manifest.py` |
| 11 | `app/models/consent_record.py` | Purpose/provider/data/policy-scoped consent | `tests/unit/test_consent_record.py` |
| 12 | `app/config/schemas/project.schema.json` | Persistent project structure | `tests/unit/test_project_schema.py` |
| 13 | `app/config/schemas/engine_manifest.schema.json` | Engine package contract | `tests/unit/test_engine_manifest_schema.py` |
| 14 | `app/config/schemas/worker_request.schema.json` | Process request envelope | `tests/contract/test_worker_protocol_schema.py` |
| 15 | `app/config/schemas/worker_result.schema.json` | Terminal result/error envelope | Same contract test. |
| 16 | `app/config/schemas/validation_report.schema.json` | MVP finding/status report | `tests/unit/test_validation_schema.py` |
| 17 | `app/ports/clock.py` | Deterministic time boundary | Test fake clock. |
| 18 | `app/ports/project_repository.py` | Project load/commit/recovery interface | Interface/architecture test. |
| 19 | `tests/unit/test_architecture_boundaries.py` | Forbid improper imports | Must fail on seeded forbidden import. |

## 6. B04 — Safe Paths and Atomic Filesystem

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/config/paths.py` | Application/project roots and canonicalization policy | `tests/unit/test_paths.py` |
| 2 | `app/adapters/filesystem/safe_paths.py` | Generated names, root containment, Unicode-safe handling | `tests/unit/test_safe_paths.py` |
| 3 | `app/adapters/filesystem/reparse_point_guard.py` | Windows junction/symlink deletion boundary | `tests/integration/test_reparse_point_guard.py` |
| 4 | `app/adapters/filesystem/atomic_file_writer.py` | Temp-write, flush, replace, failure cleanup | `tests/integration/test_atomic_file_writer.py` |
| 5 | `app/adapters/filesystem/artifact_hasher.py` | Streaming file/directory hashes and size limits | `tests/unit/test_artifact_hasher.py` |
| 6 | `tests/integration/test_arabic_paths.py` | Arabic/spaces/quotes/long-path cases | Runs natively on Windows. |

## 7. B05 — Project Repository, Artifacts, Journal, and Recovery

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/services/artifact_service.py` | Stage/validate/promote immutable artifacts | `tests/unit/test_artifact_service.py` |
| 2 | `app/adapters/filesystem/local_project_repository.py` | Manifest load/commit/list/recovery | `tests/integration/test_project_repository.py` |
| 3 | `app/services/project_service.py` | Create/open/rename-display/delete inventory | `tests/unit/test_project_service.py` |
| 4 | `app/workers/checkpoint_manager.py` | Register and validate stage checkpoints | `tests/unit/test_checkpoint_manager.py` |
| 5 | `app/application/orchestration/recovery_coordinator.py` | Detect abandoned run and select safe recovery action | `tests/integration/test_interrupted_recovery.py` |
| 6 | `app/migrations/migration_registry.py` | Project schema migration dispatch | `tests/unit/test_project_migrations.py` |
| 7 | `app/migrations/project_v1_to_v2.py` | First demonstrative migration only when schema v2 exists | Same migration test. |
| 8 | `app/services/secure_deletion_service.py` | Inventory, stop/close preconditions, truthful deletion receipt | `tests/integration/test_delete_project.py` |

## 8. B06 — Logging, Redaction, and Settings

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/logging/event_ids.py` | Stable event catalog | Catalog uniqueness test. |
| 2 | `app/logging/redaction_policy.py` | Secret/path/header/token/image-data removal | `tests/unit/test_log_redaction.py` |
| 3 | `app/logging/configure_logging.py` | Structured processors and safe sinks | `tests/integration/test_logging_pipeline.py` |
| 4 | `app/logging/bounded_log_store.py` | Size/time retention and safe excerpts | `tests/unit/test_bounded_log_store.py` |
| 5 | `app/config/settings.py` | Versioned local settings without secrets | `tests/unit/test_settings.py` |
| 6 | `app/adapters/security/dotenv_secret_source.py` | Optional `.env` read/import only | `tests/unit/test_dotenv_secret_source.py` |
| 7 | `app/ports/secret_store.py` | Credential-reference interface | Contract test. |
| 8 | `app/adapters/security/windows_credential_store.py` | Windows Credential Manager adapter when needed | Native Windows integration test. |

## 9. B07 — Bootstrap, Theme, and Localization

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/main.py` | Minimal process entry point | Startup smoke test. |
| 2 | `app/bootstrap.py` | Exception boundary, app metadata, Qt initialization | `tests/ui/test_bootstrap.py` |
| 3 | `app/composition_root.py` | Dependency wiring only | Construction test with fakes. |
| 4 | `app/ui/theme.py` | Navy/white/gold tokens and scalable typography | `tests/ui/test_theme.py` |
| 5 | `app/localization/translator.py` | Translation loading/switching | `tests/unit/test_translator.py` |
| 6 | `app/localization/bidi_helpers.py` | Mixed-direction path/identifier presentation | `tests/unit/test_bidi_helpers.py` |
| 7 | `app/localization/en_US.ts` | English message source | Catalog coverage test. |
| 8 | `app/localization/ar.ts` | Arabic critical-shell strings/skeleton | UTF-8/catalog key parity test. |
| 9 | `app/ui/navigation_model.py` | Five phases/fifteen step states | `tests/unit/test_navigation_model.py` |
| 10 | `app/ui/main_window.py` | Shell regions and state binding | `tests/ui/test_navigation.py` |

## 10. B08 — Project UI

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/controllers/application_controller.py` | Startup/recent/recovery coordination | Controller unit test. |
| 2 | `app/controllers/project_controller.py` | Create/open/delete UI commands | Controller unit test. |
| 3 | `app/ui/pages/home_page.py` | Recent projects and create/open actions | `tests/ui/test_home_page.py` |
| 4 | `app/ui/pages/new_project_page.py` | Name/folder/language/permission acknowledgment | `tests/ui/test_new_project.py` |
| 5 | `app/ui/pages/mode_selection_page.py` | Fast AI enabled, Accurate Scan deferred honestly | `tests/ui/test_mode_selection.py` |
| 6 | `app/ui/dialogs/delete_project_dialog.py` | Category inventory and remaining-item result | `tests/ui/test_delete_dialog.py` |
| 7 | `app/ui/widgets/collapsible_error_panel.py` | Shared safe error presentation | `tests/ui/test_error_details.py` |

## 11. B09 — Worker Contract and State Machine

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/workers/progress_event.py` | Structured stage progress/log event | Contract tests. |
| 2 | `app/workers/cancellation_token.py` | Cooperative cancellation file/event model | Unit test. |
| 3 | `app/workers/task_state_machine.py` | Queued/preflight/running/cancelling/success/failure transitions | `tests/unit/test_task_state_machine.py` |
| 4 | `app/workers/worker_protocol.py` | Serialize/validate request/result/events | `tests/contract/test_worker_protocol.py` |
| 5 | `app/ports/process_runner.py` | Process invocation/signal interface | Fake contract test. |
| 6 | `docs/engine_protocol.md` | Human-readable protocol and compatibility rules | Schema examples validate. |

## 12. B10 — `QProcess` Supervisor and Fake Workers

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/adapters/processes/engine_result_reader.py` | Validate terminal result and artifact references | Contract test. |
| 2 | `app/adapters/processes/qt_process_runner.py` | Safe executable/argument-vector launch and event capture | `tests/integration/test_qprocess_runner.py` |
| 3 | `app/workers/process_tree.py` | Child-process tracking and Windows termination | `tests/integration/test_process_tree.py` |
| 4 | `app/workers/process_supervisor.py` | Timeout/cancel/grace/kill/result-validation orchestration | `tests/integration/test_task_cancellation.py` |
| 5 | `tests/fixtures/fake_engines/fake_worker.py` | Deterministic success/failure/hang/malformed/child/secret modes | All process integration tests. |
| 6 | `tests/contract/test_worker_failure_modes.py` | Zero-exit missing/stale/empty result rules | Must pass every mode. |

## 13. B11 — Activity Center and Error UI

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/ui/widgets/progress_stage_row.py` | Numeric/indeterminate/terminal stage display | UI state test. |
| 2 | `app/ui/widgets/activity_drawer.py` | Overall task state and controls | `tests/ui/test_progress_controls.py` |
| 3 | `app/ui/dialogs/error_details_dialog.py` | Redacted causal chain and copy action | `tests/ui/test_error_details.py` |
| 4 | `app/controllers/processing_controller.py` | Bind supervisor state to UI | UI heartbeat and cancellation test. |

## 14. B12–B14 — Image Vertical Slice

### B12 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/models/view_assignment.py` | View enum and assignment confidence/source | Unit test. |
| 2 | `app/models/quality_finding.py` | Metric/status/impact/action finding | Unit test. |
| 3 | `app/ports/image_quality_analyzer.py` | Analyzer interface | Contract test. |
| 4 | `app/adapters/imaging/pillow_decoder.py` | Bounded decode, orientation, thumbnail | `tests/unit/test_image_decoder.py` |
| 5 | `app/validators/image_input_validator.py` | Type/size/dimension/pixel policy | `tests/unit/test_image_input_validator.py` |
| 6 | `app/services/image_import_service.py` | Managed copy and normalized derivative | `tests/integration/test_image_import.py` |

### B13 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/adapters/imaging/opencv_quality_analyzer.py` | Blur/exposure/resolution metrics | `tests/unit/test_blur_detection.py`, `test_exposure_detection.py` |
| 2 | `app/adapters/imaging/perceptual_duplicate_detector.py` | Exact/perceptual grouping | `tests/unit/test_duplicate_detection.py` |
| 3 | `app/services/image_quality_service.py` | Aggregate findings and mode policy | `tests/unit/test_image_quality_service.py` |
| 4 | `app/services/primary_image_selector.py` | Explainable front/45-degree candidate ranking | `tests/unit/test_primary_image_selector.py` |
| 5 | `app/ports/view_estimator.py` | Optional estimator interface; fake/manual baseline | Contract test. |

### B14 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/controllers/image_controller.py` | Import/assign/analyze coordination | Controller test. |
| 2 | `app/ui/widgets/image_drop_zone.py` | Drag/drop and skipped-file feedback | `tests/ui/test_drag_drop.py` |
| 3 | `app/ui/widgets/image_thumbnail_card.py` | Thumbnail, metadata, quality, selection | UI test. |
| 4 | `app/ui/widgets/view_slot.py` | Assigned view and keyboard actions | UI test. |
| 5 | `app/ui/pages/image_import_page.py` | Import workspace | Integration UI test. |
| 6 | `app/ui/pages/view_assignment_page.py` | View slots and primary marker | Integration UI test. |
| 7 | `app/ui/pages/quality_report_page.py` | Findings/filters/preview/actions | Integration UI test. |

## 15. B15–B17 — Background and Mask Vertical Slice

### B15 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/models/mask_revision.py` | Immutable mask lineage and approval | Unit test. |
| 2 | `app/ports/background_remover.py` | Capability/install/infer contract | `tests/contract/test_background_remover_contract.py` |
| 3 | `app/services/engine_registry.py` | Validated engine/model registrations and readiness state | Unit test. |
| 4 | `app/services/engine_installation_service.py` | Stage/verify/install/self-test/rollback | Integration test with fake package. |
| 5 | `packaging/engine_manifests/background_model.template.json` | Required model fields | Schema test. |

### B16 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/adapters/imaging/onnx_background_remover.py` | Approved ONNX inference adapter | Real model self-test/inference tests. |
| 2 | `app/workers/image_worker.py` | Out-of-GUI-process inference entry point | Process/cancel/failure test. |
| 3 | `app/services/mask_service.py` | Request, validate, store initial mask revision | Unit/integration test. |
| 4 | `tests/contract/test_background_model_manifest.py` | Hash/license/capability cases | Manifest gate test. |

### B17 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/adapters/imaging/manual_mask_renderer.py` | Deterministic stroke/raster composition | Unit test. |
| 2 | `app/ui/widgets/mask_canvas.py` | Brush/erase/zoom/pan/undo/redo | `tests/ui/test_mask_editor.py` |
| 3 | `app/controllers/mask_controller.py` | Revisions/autosave/approval | Controller/restart test. |
| 4 | `app/ui/pages/background_removal_page.py` | Model/progress/result review | UI test. |
| 5 | `app/ui/pages/mask_editor_page.py` | Manual correction workflow | UI/recovery test. |

## 16. B18–B19 — Offline Viewer

### B18 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `viewer/package.json` | Pinned direct viewer dependencies | Lock validation. |
| 2 | `viewer/package-lock.json` or approved package-manager lock | Exact graph | Clean install/build. |
| 3 | `viewer/tsconfig.json` | Strict TypeScript settings | Type check. |
| 4 | `viewer/vite.config.ts` | Deterministic local bundle | Build hash test. |
| 5 | `viewer/src/main.ts` | Bootstrap and bridge handshake | Viewer unit test. |
| 6 | `viewer/src/scene_controller.ts` | Scene lifecycle | Unit test. |
| 7 | `viewer/src/model_loader.ts` | GLB load and scene inventory | Synthetic GLB test. |
| 8 | `viewer/src/camera_controller.ts` | Rotate/pan/zoom/standard views | State test. |
| 9 | `viewer/src/view_modes.ts` | Material/solid/wireframe | State test. |
| 10 | `viewer/src/part_tree.ts` | Part visibility/isolation | Unit test. |
| 11 | `viewer/src/screenshot.ts` | User-requested capture | Unit/manual test. |
| 12 | `viewer/src/webchannel.ts` | Versioned narrow bridge | `viewer/tests/protocol.test.ts` |
| 13 | `viewer/src/styles.css` | Offline viewer styling | Visual smoke. |
| 14 | `scripts/build_viewer.py` | Controlled build and copy to assets | Deterministic manifest test. |

### B19 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/ports/viewer_bridge.py` | Viewer message contract | Contract test. |
| 2 | `app/adapters/viewer/viewer_cache.py` | Generated read-only model cache | Arabic/path containment test. |
| 3 | `app/adapters/viewer/viewer_request_interceptor.py` | Deny remote/unapproved schemes | `viewer/tests/network_denial.test.ts` plus Qt integration. |
| 4 | `app/adapters/viewer/webchannel_gateway.py` | Schema validation and dispatch | Integration test. |
| 5 | `app/adapters/viewer/webengine_viewer.py` | Qt host and recovery | `tests/integration/test_offline_viewer.py` |
| 6 | `app/controllers/viewer_controller.py` | Load/view/part/screenshot coordination | Controller test. |
| 7 | `app/ui/pages/model_preview_page.py` | Viewer page shell | UI test. |

## 17. B20–B21 — Blender Vertical Slice

### B20 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `blender_scripts/LICENSE` | GPL-compatible script license | Compliance check. |
| 2 | `blender_scripts/README.md` | Supported Blender/protocol/run/source instructions | Documentation review. |
| 3 | `blender_scripts/protocol.py` | Request/result validation usable inside Blender | Blender contract test. |
| 4 | `blender_scripts/scene_io.py` | Import/save/export staging | Reopen fixture test. |
| 5 | `blender_scripts/geometry_metrics.py` | Components/bounds/polygons/non-manifold metrics | Known fixture metrics. |
| 6 | `blender_scripts/pipeline_runner.py` | Operation dispatch and terminal result | Real Blender self-test. |
| 7 | `app/adapters/processes/blender_cli_adapter.py` | Discovery/version/self-test/request invocation | `tests/integration/test_blender_protocol.py` |
| 8 | `packaging/engine_manifests/blender.template.json` | Discovery registration fields | Schema test. |

### B21 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `blender_scripts/operations/connected_components.py` | Main/component classification | `tests/blender/test_remove_disconnected.py` |
| 2 | `blender_scripts/operations/merge_by_distance.py` | Local duplicate merge | Fixture test. |
| 3 | `blender_scripts/operations/normals.py` | Recalculate/inspect normals | Fixture test. |
| 4 | `blender_scripts/operations/holes.py` | Conservative boundary analysis/repair | Fixture test. |
| 5 | `blender_scripts/operations/boolean_union.py` | Body/base union and failure capture | `tests/integration/test_base_creation.py` |
| 6 | `blender_scripts/operations/unit_scale.py` | Unit interpretation and target height | `tests/unit/test_millimeter_conversion.py` plus Blender test. |
| 7 | `blender_scripts/operations/build_plate.py` | Z=0 placement/contact | Fixture test. |
| 8 | `blender_scripts/cleanup_mesh.py` | Compose cleanup operations | Blender pipeline test. |
| 9 | `blender_scripts/repair_non_manifold.py` | Conditional repair policy | `tests/blender/test_manifold_validation.py` |
| 10 | `blender_scripts/voxel_remesh.py` | Conditional remesh with metrics | Trigger/non-trigger fixture. |
| 11 | `blender_scripts/decimate_mesh.py` | Conservative target and deviation report | `tests/blender/test_face_preservation.py` |
| 12 | `blender_scripts/add_base.py` | Circular/square MVP base | Base fixture. |
| 13 | `blender_scripts/render_previews.py` | Four fixed views | `tests/blender/test_preview_rendering.py` |
| 14 | `app/application/orchestration/blender_pipeline.py` | Application-side stage graph | Integration test. |
| 15 | `app/ports/mesh_processor.py` | Blender-independent processing contract | Contract test. |
| 16 | `app/ui/pages/repair_page.py` | Before/after metrics and accept/revert | UI test. |

## 18. B22–B23 — Generator Vertical Slice

### B22 Files

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/models/generation_request.py` | Primary image, mask, style, dimensions, device, adapter | Unit test. |
| 2 | `app/ports/generator.py` | Adapter/preflight/run/cancel/result contract | `tests/contract/test_generator_contract.py` |
| 3 | `generators/base_generator.py` | Worker-side contract helpers | Contract test. |
| 4 | `app/services/device_capability_service.py` | CPU/GPU/VRAM/RAM/disk facts | Fake and native probe tests. |
| 5 | `app/services/primary_image_selector.py` | Update only if generator contract needs explicit export method | Regression tests. |
| 6 | `app/services/reference_color_service.py` | Separate supplementary-photo color report | Unit test proves no generator staging. |
| 7 | `tests/fixtures/fake_engines/fake_generator.py` | Capability/resource/license/success/failure cases | Generator matrix. |
| 8 | `packaging/engine_manifests/hunyuan.template.json` | Optional Hunyuan fields | Schema test. |

### B23 Files

Create only the files for the selected real path.

| Path option | Files | Mandatory evidence |
|---|---|---|
| Hunyuan | `generators/hunyuan_generator.py`, `generators/hunyuan_worker_entry.py` | Territory/license gate, isolated environment, resource preflight, one-image staging, real success/failure/cancel. |
| Alternative local | `generators/<engine>_generator.py`, `generators/<engine>_worker_entry.py` | Same contract and engine decision record. |
| External provider | `generators/external_api_generator.py`, `generators/provider_http_client.py`, `generators/provider_response_validator.py`, `app/services/consent_service.py`, `app/ui/dialogs/external_consent_dialog.py` | Secret storage, exact disclosure/consent, minimized upload, timeout/cancel/duplicate safety, result validation. |

All paths add `tests/integration/test_real_generator.py` in the controlled environment and `docs/generator_decision_record.md`.

## 19. B24 — End-to-End Fast AI Orchestration

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/models/figure_style.py` | MVP style parameters and deferred styles | Unit test. |
| 2 | `app/models/print_profile.py` | 40–250 mm, default 100 mm, base, polygon target | `tests/unit/test_dimension_calculations.py` |
| 3 | `app/services/style_service.py` | Validate available/deferred style capabilities | Unit test. |
| 4 | `app/services/dimension_service.py` | Range/profile validation | Property tests. |
| 5 | `app/application/orchestration/stage_definition.py` | Stage IDs, inputs, outputs, cache/invalidation | Unit test. |
| 6 | `app/application/orchestration/stage_cache.py` | Provenance-based reuse only | Stale-cache test. |
| 7 | `app/application/orchestration/pipeline_orchestrator.py` | Shared execution/recovery/cancel | Integration tests. |
| 8 | `app/application/orchestration/fast_ai_pipeline.py` | Mask→generate→preview→Blender flow | `tests/e2e/test_fast_ai_workflow.py` |
| 9 | `app/controllers/generation_controller.py` | Review/start/cancel/retry binding | UI integration. |
| 10 | `app/ui/pages/style_selection_page.py` | MVP and deferred style cards | UI test. |
| 11 | `app/ui/pages/print_settings_page.py` | Height/base/polygon/device controls | UI test. |
| 12 | `app/ui/pages/generation_page.py` | Review and Activity Center integration | UI/process test. |

## 20. B25 — Minimum Validation

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/models/validation_finding.py` | Code/severity/measurement/threshold/location/action | Unit test. |
| 2 | `app/models/validation_report.py` | Findings and derived three-state result | Unit test. |
| 3 | `app/ports/printability_validator.py` | Validator interface | Contract test. |
| 4 | `app/validators/artifact_validator.py` | File/hash/provenance/non-empty checks | Fixture test. |
| 5 | `app/validators/mesh_topology_validator.py` | Watertight/non-manifold/disconnected MVP checks | Known mesh fixtures. |
| 6 | `app/validators/dimension_validator.py` | X/Y/Z/height/range | Known mesh fixtures. |
| 7 | `app/validators/build_plate_validator.py` | Bottom/contact at Z=0 | Fixture test. |
| 8 | `app/application/commands/validate_model.py` | Aggregate validators and persist report | Integration test. |
| 9 | `app/controllers/validation_controller.py` | Report/viewer selection binding | UI test. |
| 10 | `app/ui/widgets/finding_card.py` | Metric/threshold/action display | UI test. |
| 11 | `app/ui/pages/printability_page.py` | Three states and qualified wording | UI test. |

## 21. B26 — Transactional STL and GLB Export

| Order | File | Purpose | Paired test |
|---:|---|---|---|
| 1 | `app/ports/model_exporter.py` | Format capability and result contract | Contract test. |
| 2 | `app/validators/export_result_validator.py` | Reopen, dimensions, inventory, current-run checks | Fault fixtures. |
| 3 | `app/exporters/transactional_exporter.py` | Stage/validate/atomic-finalize and overwrite policy | `tests/integration/test_export_validation.py` |
| 4 | `app/exporters/stl_exporter.py` | STL path through approved engine/library | STL reopen test. |
| 5 | `app/exporters/glb_exporter.py` | GLB path and material/resource inventory | GLB reopen test. |
| 6 | `app/exporters/export_report_writer.py` | Provenance, metrics, warnings, hashes | Schema test. |
| 7 | `app/exporters/export_manager.py` | Format option resolution and coordination | Unit/integration test. |
| 8 | `app/application/orchestration/export_pipeline.py` | Validation-before-export stage graph | Fault test. |
| 9 | `app/controllers/export_controller.py` | Selection/destination/progress/result UI | UI test. |
| 10 | `app/ui/pages/export_page.py` | Texture versus printable grouping and STL/GLB options | UI test. |

## 22. B27 — Hardening, Packaging Smoke, and Closeout

| Order | File | Purpose | Verification |
|---:|---|---|---|
| 1 | `packaging/pyinstaller/MiniFigure3DStudio.spec` | Directory-based development build | Native Windows build and manifest. |
| 2 | `packaging/pyinstaller/runtime_hook.py` | Minimal validated runtime setup | Clean-machine startup. |
| 3 | `packaging/pyinstaller/hooks/` | Only required custom hooks | Qt plugin/WebEngine resources verified. |
| 4 | `packaging/windows/build.ps1` | Reproducible development package command | Clean build. |
| 5 | `packaging/windows/smoke_test.ps1` | Startup/resource/offline/basic path checks | Clean VM report. |
| 6 | `.github/workflows/windows-build.yml` | Native Windows integration/package lane | CI report. |
| 7 | `.github/workflows/blender-integration.yml` | Supported Blender fixture lane | CI/manual controlled report. |
| 8 | `.github/workflows/security.yml` | Secret, dependency, SBOM, asset checks | Security report. |
| 9 | `docs/architecture.md` | Implemented Stage 2 architecture and divergences | Review against code. |
| 10 | `docs/project_format.md` | Schema/artifact/recovery contract | Fixtures validate examples. |
| 11 | `docs/troubleshooting_en.md` | Real error codes and corrective steps | Walkthrough. |
| 12 | `docs/troubleshooting_ar.md` | Critical Arabic troubleshooting coverage | Language review status disclosed. |
| 13 | `docs/export_compatibility.md` | Tested STL/GLB behavior and limitations | References actual test versions. |
| 14 | `docs/stage2_test_report.md` | All commands/environments/results/skips | Evidence links resolve. |
| 15 | `docs/stage2_changed_files.md` | Exact created/modified file inventory | Git diff matches. |
| 16 | `docs/stage2_known_limitations.md` | Deferred/unsupported items and risks | No planned feature is described as working. |

## 23. Files Explicitly Deferred to Stage 3

The Stage 2 repository may define ports or deferred navigation states, but it should not create unused production modules merely to match the full tree. The following stay unimplemented until Stage 3 unless needed by a chosen real adapter: `accurate_scan_pipeline.py`, `colmap_cli_adapter.py`, `photogrammetry_generator.py`, full color-separation modules, 3MF exporter, wall/internal/overhang/support validators, advanced style scripts, hollow/drain/name/keychain operations, OBJ/BLEND production exporters, and final signed installer definitions.

## 24. Batch Completion Template

Each batch closes with a report containing the batch ID, objective, files created, files modified, dependency changes, commands run, passed/failed/skipped counts, manual checks, screenshots/artifacts, security/license changes, known defects, rollback point, and approval to enter the next batch. If a mandatory test fails, the next behavior-changing batch does not start.

## References

[1]: https://www.blender.org/about/license/ "Blender License"
[2]: https://github.com/mrdoob/three.js "Three.js Repository"
