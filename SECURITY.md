# Security Policy

## Project Status

MiniFigure 3D Studio is in Stage 2 development and is **not production-ready**. No public security-support period or stable release channel is currently offered.

## Reporting a Security Issue

Do not open a public issue containing credentials, private photographs, project files, generated likeness data, local paths, or exploit details that expose users. Contact the repository owner privately through an owner-approved channel. No dedicated security email is published yet; the owner must add one before public release.

## Security Principles

| Area | Development rule |
|---|---|
| Secrets | Never hard-code, commit, log, place on command lines, or store in project manifests. Windows Credential Manager or DPAPI is preferred; `.env` is compatibility input only. |
| Images and likeness data | Local by default; never included in logs, diagnostics, fixtures, analytics, or remote requests without explicit operation-specific consent. |
| External processes | Launch validated executables with argument vectors and minimal environments. Never build shell command strings from user input. |
| Paths | Use generated internal names and canonical root-containment checks. Deletion must not follow unexpected reparse points outside a managed root. |
| Artifacts | Write to staging, validate schema/provenance/hash/content, then atomically promote. Process exit code alone is not success. |
| Dependencies | Pin after native compatibility tests, generate an SBOM, collect notices, audit vulnerabilities, and verify engine/model hashes. |
| Viewer | Bundle assets locally, deny remote requests/navigation/popups, and expose only a narrow schema-validated bridge. |
| Logging | Apply redaction before every sink. Exclude credentials, authorization headers, image data, EXIF payloads, and unsafe full paths. |
| Test data | Use synthetic or explicitly licensed fixtures only. Real-person photos are prohibited in the repository and CI artifacts. |

## Supported Development Branch

Security fixes apply only to the current active Stage 2 branch until a release-support policy is published. No version should be represented as supported merely because it exists in the repository.

## Handling a Confirmed Issue

The implementation must preserve a safe incident record, remove or rotate exposed credentials, quarantine unsafe artifacts, add a deterministic regression test, rerun affected security and privacy gates, update notices/advisories where needed, and avoid repeating sensitive data in commits or reports.
