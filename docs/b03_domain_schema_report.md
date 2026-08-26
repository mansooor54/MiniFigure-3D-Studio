# B03 Core Domain Primitives and Schemas Report

**Milestone:** M1–M2 — Domain and Project Foundation  
**Batch:** B03  
**Branch:** `stage2/m0-b01`  
**Date:** 2026-08-26  
**Gate result:** **Passed for the portable connected-desktop lane**

## Objective

B03 establishes strict domain values and versioned JSON contracts before filesystem, process, UI, engine, and network adapters. Domain and port modules remain independent of PySide6, Blender, subprocesses, HTTP clients, concrete storage, services, controllers, and widgets.

## Files Created

| Area | Files | Purpose |
|---|---|---|
| Identity | `app/__init__.py`, `app/application_info.py` | Single product/version/schema/protocol source. |
| Model foundation | `app/models/_base.py`, `app/models/__init__.py` | Strict immutable Pydantic configuration and shared validators. |
| Errors/results | `app/models/error_info.py`, `app/models/stage_result.py` | Stable localized errors and terminal stage-result invariants. |
| Runs/artifacts | `app/models/pipeline_run.py`, `app/models/mesh_artifact.py` | Run/stage state, engine/settings provenance, immutable mesh lineage. |
| Projects/images | `app/models/project.py`, `app/models/source_image.py` | Project aggregate, permission timeline, managed source identity, current-artifact references. |
| Engines/consent | `app/models/generator_capabilities.py`, `app/models/engine_manifest.py`, `app/models/consent_record.py` | Truthful adapter capabilities, hashed/license/territory engine packages, explicit transfer consent. |
| Ports | `app/ports/__init__.py`, `app/ports/clock.py`, `app/ports/project_repository.py` | Deterministic time and persistence/recovery abstractions. |
| Configuration | `app/config/__init__.py`, `app/config/schemas/*.json` | Five strict Draft 2020-12 contracts. |
| Tooling | `scripts/generate_json_schemas.py`, `scripts/run_tests.py` | Deterministic schema generation and pre-pytest Qt environment repair. |
| Tests | `tests/unit/test_application_info.py`, `test_architecture_boundaries.py`, `test_artifact_model.py`, `test_clock.py`, `test_consent_record.py`, `test_engine_manifest.py`, `test_engine_manifest_schema.py`, `test_error_info.py`, `test_generator_capabilities.py`, `test_pipeline_run.py`, `test_project_model.py`, `test_project_schema.py`, `test_source_image.py`, `test_stage_result.py`, `test_validation_schema.py`, `tests/contract/test_worker_protocol_schema.py` | Domain, schema, contract, deterministic generation, and architecture rules. |

## Files Modified

| File | Change |
|---|---|
| `pyproject.toml` | Added `types-jsonschema`; application/domain remains included in package discovery. |
| `requirements-dev.txt` | Synchronized the jsonschema typing dependency. |
| `.github/workflows/quality.yml` | Regenerates schemas, checks `app`, and uses the verified test launcher. |
| `docs/testing_strategy.md` | Names the required macOS-safe test command. |
| `docs/b02_test_foundation_report.md` | Corrected the Qt repair description to the verified pre-pytest mechanism. |

## Domain Invariants

| Contract | Enforced behavior |
|---|---|
| `Project` | Schema v1, aware timestamps, permission acknowledgment within project timeline, unique references, current artifacts limited to committed artifacts, display names separate from paths. |
| `SourceImage` | Portable managed paths, lowercase SHA-256, bounded dimensions/orientation, derivative cannot overwrite imported original. |
| `MeshArtifact` | Immutable provenance, safe path, hash/size, positive finite dimensions, millimeter unit, coordinate convention, run/stage producer, no self-parenting. |
| `PipelineRun` | Settings hash, aware timeline, unique stage and engine IDs, stage timing, checkpoint/result references. |
| `StageResult` | Supported protocol, distinct success/warning/failure/cancel/block states, structured error requirements, no artifact promotion from cancelled work. |
| `ErrorInfo` | Uppercase stable code, category, localization key, bounded technical summary, retryability, remediation keys, typed safe details, bounded causal chain. |
| `GeneratorCapabilities` | Explicit input cardinality, no false multi-image claim, unique device/style/format sets, texture/seed/pause/cancel declarations, resource floors. |
| `EngineManifest` | Schema/protocol version, source URL, package/model hashes, portable executable/file inventory, license text hash, commercial/redistribution flags, ISO territory scope, capabilities, resources, and bounded self-test. |
| `ConsentRecord` | Provider/purpose/data categories/policy/adapter version, decision, endpoint region, aware time, and exact single-operation or bounded remembered scope without secrets. |

## Generated Schemas

| Schema | Source | Gate |
|---|---|---|
| `project.schema.json` | `Project` model | Draft 2020-12 valid; valid model serialization passes; unknown property rejected. |
| `engine_manifest.schema.json` | `EngineManifest` model | Draft valid; hashed generator manifest passes; unknown property rejected. |
| `worker_request.schema.json` | Explicit protocol v1 builder | UUIDs, safe paths, inputs, outputs, parameters, cancellation token, and redaction version required. |
| `worker_result.schema.json` | `StageResult` model | Terminal model serialization passes. |
| `validation_report.schema.json` | Explicit MVP report builder | Three printability states, findings, export blocker, orientation, and support level. |

A deterministic regeneration test compares every generated byte with the committed schema files. The quality workflow performs the same regeneration and fails on a diff.

## Quality Evidence

| Check | Result | Evidence |
|---|---|---|
| Ruff | Passed | All application, script, and test files passed. |
| mypy strict | Passed | 45 source files passed with no issues. |
| pytest | Passed | 80 tests passed; no failures or skips. |
| Architecture boundary | Passed | Domain/ports contain no Qt, Blender, HTTP, subprocess, adapter, controller, service, or UI imports; seeded forbidden import was detected. |
| Schema validity | Passed | All five schemas passed `Draft202012Validator.check_schema`. |
| Schema/model parity | Passed | Valid serialized models pass the matching schemas; unknown fields and unsafe paths are rejected. |
| Dependency audit | Passed | No known vulnerabilities; unpublished local project skipped as expected. |
| SBOM | Passed | 76 installed components inventoried, including all direct dependencies. |
| License inventory | Passed for development review | 76 packages and 18 direct dependencies inventoried; no `UNKNOWN` entry remained. |
| Asset/secret checks | Passed | Synthetic fixture policy remains valid; no suspected committed secret detected. |

## Failures Found and Repaired

| Failure | Repair |
|---|---|
| mypy rejected dynamic constants inside `Literal[...]` | Literal-typed the shared schema/protocol constants and retained a single source of truth. |
| Display-name validation used a nonexistent string API | Replaced it with a printable-character invariant. |
| Strict typing lacked jsonschema stubs | Added and resolved `types-jsonschema` for Python 3.11. |
| AST base type did not guarantee `lineno` | Narrowed through a safe `getattr` in the architecture checker. |
| Direct schema-script execution did not consistently resolve the editable package | Standardized deterministic generation as `python -m scripts.generate_json_schemas`. |
| A refreshed `uv` environment restored hidden macOS Qt plugin flags before pytest loaded | Added `scripts/run_tests.py`, which repairs the plugin tree before importing pytest; the full 80-test suite then passed. |

## Security and Privacy Review

The new models reject unknown fields, project path escapes, invalid hashes, unbounded error chains, overlapping license territories, generator capability mismatches, and ambiguous consent scopes. No image, likeness, secret, engine, model weight, network call, executable invocation, or external provider was added. Engine manifests contain hashes and license facts, never credentials.

## Platform Gaps

| Check | Status | Reason |
|---|---|---|
| Native Windows model/schema lane | Not Run | No Windows runner or connected Windows computer is available. |
| Windows filesystem, reparse-point, atomic-replace, credential, process, and package behavior | Not Run | These belong to later adapters and require native Windows. |
| Real engine manifest and territory decision | Blocked | No production generator/background model has been approved. |

## Gate Decision

B03 passes. The portable domain, port, schema, deterministic-generation, architecture, security, type, and test gates are satisfied on macOS ARM64 with Python 3.11.16. B04 safe paths and atomic filesystem implementation may begin. Windows-only evidence remains explicitly Not Run.

## Rollback

The B03 commit is the rollback point. Reverting to the preceding B02 commit removes all application domain code and schemas while preserving the tested repository foundation and Stage 1 materials.
