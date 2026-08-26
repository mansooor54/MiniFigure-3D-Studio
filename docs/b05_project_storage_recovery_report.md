# B05 Project Storage, Artifacts, Journal, Recovery, Migration, and Deletion Report

**Milestone:** M2 — Domain and Project Persistence  
**Batch:** B05  
**Branch:** `stage2/m2-storage`  
**Date:** 2026-08-26  
**Gate result:** **Passed for the portable connected-desktop lane**

## Objective

B05 turns the B03 domain contracts and B04 filesystem primitives into a recoverable local project store. It creates and opens projects, atomically commits validated manifests, stages and promotes immutable artifacts, durably journals run transitions, validates checkpoints, detects abandoned work, exposes explicit recovery actions, dispatches schema migrations truthfully, and deletes closed projects without claiming physical media sanitization.

## Files Created

| File | Purpose |
|---|---|
| `app/services/artifact_service.py` | Stage, validate, hash, promote, describe, and logically freeze immutable mesh artifacts. |
| `app/adapters/filesystem/local_project_repository.py` | Workspace creation, strict manifest load, atomic commit, recent listing, journal append, and recovery detection. |
| `app/services/project_service.py` | Permission-gated create/open/display rename/recent/inventory use cases. |
| `app/workers/checkpoint_manager.py` | Atomic checkpoint registration, hash validation, identity validation, and journal linkage. |
| `app/application/orchestration/recovery_coordinator.py` | Abandoned-run inspection and explicit resume/restart/discard/fail decisions. |
| `app/migrations/migration_registry.py` | Stepwise migration dispatch and truthful no-route/newer-schema errors. |
| `app/services/secure_deletion_service.py` | Identity/active-use/link preflight, quarantine rename, non-following removal, and deletion receipts. |
| `app/services/__init__.py` | Service-layer package boundary. |
| `app/workers/__init__.py` | Worker package boundary. |
| `app/application/__init__.py` | Application-layer package boundary. |
| `app/application/orchestration/__init__.py` | Recovery orchestration exports. |
| `app/migrations/__init__.py` | Migration registry exports and explicit no-v2 statement. |
| `tests/unit/test_artifact_service.py` | Promotion, rollback, tamper, size, metadata, and read-only tests. |
| `tests/integration/test_project_repository.py` | Create/load/commit/list/corruption/future-schema/recovery tests. |
| `tests/unit/test_project_service.py` | Permission, generated path, rename, open, and inventory tests. |
| `tests/unit/test_checkpoint_manager.py` | Checkpoint round-trip, tamper, journal, and rollback tests. |
| `tests/integration/test_interrupted_recovery.py` | Abandoned-run, resume eligibility, invalid resume, and terminal recovery tests. |
| `tests/unit/test_project_migrations.py` | Current, future, missing route, valid step, invalid output, and no-fake-v2 tests. |
| `tests/integration/test_delete_project.py` | Active/identity/link blocks, read-only content deletion, external target preservation, and truthful receipt tests. |
| `docs/b05_project_storage_recovery_report.md` | This completion evidence. |

`app/migrations/project_v1_to_v2.py` is intentionally absent because no schema v2 contract exists. Creating a pretend migration would violate the requirement not to report unsupported compatibility.

## Persistence Guarantees

| Area | Enforced behavior |
|---|---|
| Project creation | UUID directory names, complete managed layout, subject-permission acknowledgment, validated initial manifest, durable creation event. |
| Project manifest | Maximum size, UTF-8 JSON object, schema v1 check, strict Pydantic validation, atomic replacement, project-ID immutability. |
| Display rename | Updates project/model display fields and timestamp only; workspace path does not change. |
| Recent projects | Valid projects only, deterministic ordering by update time, recovery-required flag. |
| Artifact staging | Regular non-empty bounded source, private staging path, caller validator, flush/sync, SHA-256 and size record. |
| Artifact promotion | Revalidate staged hash/size, atomic move to immutable role/UUID path, rehash, write provenance metadata, logical read-only permission, rollback on failure. |
| Checkpoints | Atomic JSON envelope, exact project/run/stage/checkpoint identity, hash/size, durable journal registration, remove on journal failure. |
| Recovery | A run is recoverable only when started without a terminal event; resume is offered only for a readable identity-matching checkpoint. No abandoned output is promoted as success. |
| Migrations | Copy-on-migrate, exact one-version steps, declared output-version check, explicit future/missing-route errors. |
| Deletion | Load and match project identity; require closed project and zero active jobs; reject any link/reparse point; atomically quarantine; remove without following; report remaining items. |
| Deletion truth | Receipt states logical application deletion and warns that snapshots, backups, flash remapping, or storage recovery may retain copies. |

## Quality Evidence

| Check | Result | Evidence |
|---|---|---|
| Ruff | Passed | Application, scripts, and tests have no lint findings. |
| mypy strict | Passed | 77 source files pass with no issues. |
| pytest | Passed | 142 tests pass; no failures or skips. |
| Repository corruption | Passed | Missing, malformed, oversized/future, and domain-invalid manifests are not accepted as projects. |
| Artifact integrity | Passed | Validation failure rolls back; post-validation tamper blocks promotion; promoted content is rehashed and described. |
| Recovery integrity | Passed | Checkpointless runs cannot resume; valid checkpoints enable resume; terminal events clear recovery state. |
| Migration truthfulness | Passed | Missing and newer routes fail; no v1-to-v2 module exists before schema v2. |
| Deletion safety | Passed | Active/open, identity mismatch, and linked-tree cases do not delete; external linked content remains unchanged. |
| Architecture boundary | Passed | Domain and ports remain independent of concrete services, filesystem adapters, and orchestration. |

## Failure Found and Repaired

| Failure | Repair |
|---|---|
| The first artifact test supplied a validator that returned an integer instead of the declared `None` contract | Replaced it with an explicit validator function; strict typing then passed. |

## Security and Privacy Review

Manifests and checkpoint envelopes reject unknown or invalid domain state. Display names never select workspace directories. Artifact candidates cannot be accepted solely because a file exists; validation and hashes are required before promotion. Recovery never treats an interrupted stage as successful. Deletion refuses active projects and any tree containing a link or reparse point, preventing traversal into external data. Receipts contain identifiers, counts, status, and a storage limitation notice rather than source image content or secrets.

No image, likeness, model weight, generator, provider call, credential, analytics, or network behavior was added.

## Platform Gaps

| Check | Status | Reason |
|---|---|---|
| Native Windows atomic manifest replacement under locks/antivirus | Not Run | Requires Windows fault injection. |
| Native Windows junction/reparse deletion preflight | Not Run | macOS symlink tests cannot prove Windows junction behavior. |
| Windows crash/power-loss durability | Not Run | Portable fsync/journal tests passed; forced Windows termination is pending. |
| Windows long-path and permission-denial recovery | Not Run | No Windows runner is available. |
| Physical media sanitization | Not Claimed | Logical deletion is implemented; media sanitization depends on storage and OS facilities outside the application. |

## Gate Decision

B05 passes for portable implementation. Project, artifact, manifest, journal, checkpoint, recovery, migration, and logical deletion gates are satisfied on macOS ARM64 with Python 3.11.16. B06 logging, redaction, bounded retention, settings, and secret-source implementation may begin. Windows-only evidence remains explicitly Not Run.

## Rollback

The B05 commit is the rollback point on `stage2/m2-storage`. Reverting to B04 removes project persistence and recovery services while retaining the tested safe filesystem primitives and all earlier architecture contracts.
