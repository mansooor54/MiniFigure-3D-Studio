# B04 Safe Paths and Atomic Filesystem Report

**Milestone:** M2 — Domain and Project Persistence  
**Batch:** B04  
**Branch:** `stage2/m2-storage`  
**Date:** 2026-08-26  
**Gate result:** **Passed for the portable connected-desktop lane**

## Objective

B04 provides the filesystem safety primitives required before project manifests, artifacts, journals, recovery, or deletion are implemented. All managed operations use generated or validated project-relative paths, reject root escapes and link traversal, write committed files atomically, and hash artifacts deterministically with caller-controlled limits.

## Files Created

| File | Purpose |
|---|---|
| `app/config/paths.py` | Platform-default application roots and human-inspectable project workspace layout. |
| `app/adapters/__init__.py` | Concrete adapter package boundary. |
| `app/adapters/filesystem/__init__.py` | Filesystem adapter export boundary. |
| `app/adapters/filesystem/safe_paths.py` | Unicode-safe display filenames, Windows reserved names, UUID names, portable relative paths, containment, and symlink-aware resolution. |
| `app/adapters/filesystem/reparse_point_guard.py` | Lexical root checks plus symlink and Windows reparse-attribute detection. |
| `app/adapters/filesystem/atomic_file_writer.py` | Same-directory temporary write, flush, `fsync`, validation, atomic replace, directory sync, and cleanup. |
| `app/adapters/filesystem/artifact_hasher.py` | Streaming file hashes and deterministic directory hashes with size limits and link rejection. |
| `tests/unit/test_paths.py` | Application/project layout and no-side-effect tests. |
| `tests/unit/test_safe_paths.py` | Arabic names, reserved names, path normalization, containment, and symlink escape tests. |
| `tests/unit/test_artifact_hasher.py` | File/directory hash, limit, path-sensitivity, and link rejection tests. |
| `tests/integration/test_reparse_point_guard.py` | Managed-file, outside-root, component-link, and leaf-link tests. |
| `tests/integration/test_atomic_file_writer.py` | Success, deterministic JSON, validator failure, replace failure, cleanup, and outside-root tests. |
| `tests/integration/test_arabic_paths.py` | Arabic roots/files, UTF-8 atomic round trip, quote sanitization, and long portable paths. |
| `docs/b04_safe_filesystem_report.md` | This completion evidence. |

## Safety Guarantees

| Area | Enforced behavior |
|---|---|
| Display names | NFKC normalization, invalid Windows-character replacement, trailing dot/space removal, reserved-name escaping, bounded segment length, optional validated extension. |
| Generated names | Stable prefix plus UUID hex and validated lowercase extension; no user display name becomes path authority. |
| Relative paths | Reject empty, absolute, drive/colon, backslash, NUL, raw empty/dot/dot-dot, oversized segment, and overlong relative paths. |
| Root containment | Resolve against the canonical project root and reject any result outside it. |
| Link traversal | Reject existing symbolic links and Windows reparse attributes in managed path components. |
| Atomic write | Check containment before directory creation, stage in the destination directory, flush and sync, optionally validate, atomically replace, sync the directory where supported, and remove temporary files on every outcome. |
| Failure preservation | Validation or replace failure leaves the prior committed file unchanged and removes the candidate. |
| Artifact hash | SHA-256 streams bounded chunks; directory hashes include sorted relative paths, sizes, and bytes; symlinks are rejected. |
| Size limits | File and aggregate directory byte ceilings raise a specific error before an over-limit result is accepted. |

## Quality Evidence

| Check | Result | Evidence |
|---|---|---|
| Ruff | Passed | Application, scripts, and tests have no lint findings. |
| mypy strict | Passed | 58 source files pass with no issues. |
| pytest | Passed | 113 tests pass; no failures or skips. |
| Path traversal | Passed | Relative, nested, absolute, drive, slash-direction, raw dot, dot-dot, and symlink escapes are rejected. |
| Arabic/Unicode | Passed | Arabic project/file names, spaces, UTF-8 JSON, quote sanitization, and long bounded paths round-trip. |
| Atomic fault injection | Passed | Seeded validation and replace failures preserve the old file and leave no temporary files. |
| Hash determinism | Passed | Equivalent directory trees hash equally; content/path changes alter the result. |
| Architecture boundary | Passed | Domain and port packages remain independent of concrete filesystem adapters. |

## Failures Found and Repaired

| Failure | Repair |
|---|---|
| Ruff flagged an intentionally repeated Arabic character as visually confusable | Expressed the repeated path test characters with explicit Unicode code points while retaining the same runtime filename. |
| `PurePosixPath` normalized `inputs/./file.txt` before validation | Added raw segment checks before path construction so empty, dot, and dot-dot segments cannot disappear during normalization. |
| Atomic writer originally created the target parent before proving containment | Moved and repeated the reparse/root guard before and after directory creation. |

## Security and Privacy Review

No source image, likeness, user project, secret, model, engine, or network operation was added. Paths derived from display values are bounded and sanitized. Project-relative references cannot authorize access outside the managed root. The atomic writer never treats successful temporary creation as committed success, and the hasher never follows a linked artifact tree.

## Platform Gaps

| Check | Status | Reason |
|---|---|---|
| Native Windows junction/reparse behavior | Not Run | macOS symlink evidence cannot prove Windows junction and reparse semantics. |
| Native Windows replace behavior with antivirus, locks, and permission denial | Not Run | Requires Windows fault injection. |
| Windows long-path policy and drive-letter/case behavior | Not Run | Portable validation passed; native behavior remains required. |
| Windows directory durability semantics | Not Run | Directory sync is intentionally skipped on Windows; manifest recovery must tolerate the platform boundary. |

## Gate Decision

B04 passes for portable implementation. Safe path, root containment, reparse/symlink, atomic replacement, failure cleanup, hashing, Unicode, lint, type, and test gates are satisfied on macOS ARM64 with Python 3.11.16. B05 project repository, artifact promotion, journal, checkpoint, recovery, migration, and deletion implementation may begin. Windows-only evidence remains explicitly Not Run.

## Rollback

The B04 commit is the rollback point on `stage2/m2-storage`. Reverting to B03 removes the concrete filesystem safety layer while retaining the validated domain and schema contracts.
