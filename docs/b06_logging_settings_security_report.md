# B06 Logging, Redaction, Settings, and Secret Handling Report

**Milestone:** M2 — Domain and Project Persistence  
**Batch:** B06  
**Branch:** `stage2/m2-storage`  
**Date:** 2026-08-26  
**Gate result:** **Passed for the portable connected-desktop lane**

## Objective

B06 adds structured and bounded application logging, defense-in-depth redaction, versioned local settings without credentials, an optional protected `.env` import path, a closeable secret-value lifecycle, and a Windows Credential Manager adapter boundary. It preserves local/offline defaults and does not claim native Windows credential validation from macOS evidence.

## Files Created

| File | Purpose |
|---|---|
| `app/logging/event_ids.py` | Stable project, stage, engine, privacy, export, and deletion event catalog. |
| `app/logging/redaction_policy.py` | Recursive secret, header, cookie, environment, image, body, absolute-path, URL-query, size, depth, and collection redaction. |
| `app/logging/configure_logging.py` | UTF-8 structured JSON events, UTC time, rotation, safe formatting, flush, and close. |
| `app/logging/bounded_log_store.py` | Age/size pruning and safe bounded tail excerpts. |
| `app/logging/__init__.py` | Logging package boundary. |
| `app/config/settings.py` | Strict schema-v1 local settings and atomic store without credential values. |
| `app/ports/secret_store.py` | Credential-reference protocol and closeable/zeroizable in-memory secret value. |
| `app/adapters/security/dotenv_secret_source.py` | Optional no-interpolation `.env` import with file/name/prefix/permission policy. |
| `app/adapters/security/windows_credential_store.py` | Windows-only credential backend discovery plus injectable contract-tested backend. |
| `app/adapters/security/__init__.py` | Security adapter package boundary. |
| `tests/unit/test_event_ids.py` | Catalog uniqueness, format, and critical outcome coverage. |
| `tests/unit/test_log_redaction.py` | Seeded token, header, cookie, nested, path, URL, binary, size, and depth cases. |
| `tests/integration/test_logging_pipeline.py` | End-to-end JSON formatting and redaction. |
| `tests/unit/test_bounded_log_store.py` | Age/size pruning, malformed records, safe tail, child-path, and link tests. |
| `tests/unit/test_settings.py` | Offline defaults, Arabic path, atomic persistence, telemetry-off, duplicates, and unknown secret-field tests. |
| `tests/unit/test_dotenv_secret_source.py` | Prefix, permission, no interpolation, no environment mutation, link, and controlled import tests. |
| `tests/contract/test_secret_store.py` | Secret lifecycle and injected credential backend contract tests. |
| `docs/b06_logging_settings_security_report.md` | This completion evidence. |

## Privacy and Security Guarantees

| Area | Enforced behavior |
|---|---|
| Event IDs | Stable dotted lowercase catalog; callers do not invent free-form success states. |
| Field redaction | Authorization, tokens, keys, passwords, credentials, cookies, private keys, environment dumps, image/mask/texture data, and request/response bodies are replaced. |
| Text redaction | Bearer values, OpenAI-shaped tokens, AWS-shaped access IDs, key/value secrets, Windows and common POSIX absolute paths, URL user information, and sensitive query values are removed. |
| Bounds | Nested depth, item count, string length, excerpt bytes, excerpt entries, retention age, and total log storage are bounded. |
| Structured sink | One JSON object per line, UTC timestamp, level, event ID, redacted message and fields, UTF-8, rotating files, explicit flush/close. |
| Settings | Local/offline and telemetry-off defaults; enabled provider IDs and opaque credential references only; unknown fields rejected; atomic persistence. |
| `.env` compatibility | Explicit user-selected regular file, maximum 64 KiB, no symlink, POSIX group/other access denied, approved prefix/name only, interpolation disabled, process environment unchanged. |
| Secret lifecycle | Secret values use mutable buffers, explicit close/context lifecycle, and zeroize the managed buffer before release. Python/backend copies are not falsely claimed to be perfectly erasable. |
| Windows credentials | Runtime discovery is Windows-only and requires a backend whose identity is Windows Credential Manager; settings never store the value. |

## Quality Evidence

| Check | Result | Evidence |
|---|---|---|
| Ruff | Passed | Application, scripts, and tests have no lint findings. |
| mypy strict | Passed | 94 source files pass with no issues. |
| pytest | Passed | 169 tests pass; no failures or skips. |
| Redaction seeds | Passed | Seeded keys, tokens, cookies, environment values, image bytes, paths, and URL credentials are absent from serialized output. |
| Logging integration | Passed | Structured UTF-8 event retains safe Arabic and stage fields while removing secret/path/binary values. |
| Retention | Passed | Expired files and oldest over-limit files are removed deterministically; malformed lines are replaced without echoing content. |
| Settings | Passed | Offline/private defaults, Arabic paths, telemetry-off, atomic round trips, duplicate and unknown secret-field rejection. |
| `.env` | Passed | No interpolation or environment mutation; insecure permission, wrong prefix, and symlink cases fail. |
| Secret-store contract | Passed | Store/read/contains/delete and missing-reference behavior pass through an injected backend; secret context closes. |
| Architecture boundary | Passed | Domain models and ports do not depend on concrete security or logging adapters. |

## Failures Found and Repaired

| Failure | Repair |
|---|---|
| Ruff reported import ordering and a constructed default limits object | Sorted imports and introduced one immutable module-level default. |
| Direct keyring imports lacked portable stubs and made the non-Windows type path unreachable | Moved optional keyring discovery behind runtime `importlib` on Windows and retained an injected typed backend for portable contracts. |
| Retention test expected deletion chronology while the receipt promises sorted deterministic names | Corrected the test to the documented sorted order. |
| One macOS Qt test start encountered the known hidden-plugin loader state | Confirmed and cleared the plugin flag through the approved pre-pytest preparation; the repeated complete 169-test suite passed. |

## Platform Gaps

| Check | Status | Reason |
|---|---|---|
| Native Windows Credential Manager store/read/delete | Not Run | Contract passed with an injected backend; native Windows and actual backend identity remain required. |
| Windows `.env` ACL assessment | Not Run | POSIX mode policy passed; Windows ACL inspection is not implemented in this compatibility source. |
| Windows file rotation under sharing/antivirus locks | Not Run | Requires native Windows fault injection. |
| Windows absolute-path redaction variants | Partially tested | Windows-style text patterns pass portably; native path objects and UNC/device paths require Windows cases. |

## Gate Decision

B06 passes for portable implementation. Logging, redaction, bounded retention, secret-free settings, dotenv import, secret lifecycle, and credential-backend contract gates are satisfied on macOS ARM64 with Python 3.11.16. The complete M2 portable gate is ready for final verification. Native Windows credential, ACL, rotation, and path evidence remains explicitly Not Run.

## Rollback

The B06 commit is the rollback point on `stage2/m2-storage`. Reverting to B05 removes logging/settings/security behavior while preserving the passing project persistence, recovery, migration, and deletion foundation.
