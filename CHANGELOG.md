# Changelog

All notable project changes will be documented in this file. The project does not yet publish stable semantic versions.

## Unreleased — Stage 2 Foundation

### Added

- Recorded Stage 1 and Stage 2 planning approval.
- Established the owner-provided GitHub repository as the implementation workspace.
- Created the M0 decision record with unresolved engine, model, territory, license, hardware, and publishing gates.
- Added English and Arabic status documentation.
- Added private-development license status, third-party notice index, security policy, privacy policy, and contribution rules.
- Completed B01 repository metadata and quality configuration on the isolated Stage 2 branch.
- Added the connected-desktop platform exception that preserves all Windows-only test gaps.
- Installed and verified an isolated Python 3.11.16 development environment with PySide6 6.10.3.
- Added deterministic person-free image and mesh fixtures with a hash, license, source, privacy, and expected-result manifest.
- Added portable Ruff, mypy, pytest, asset, dependency-audit, SBOM, and license-evidence tooling plus a read-only Linux/macOS quality workflow.
- Added the B02 testing strategy and completion report with explicit Windows-only gaps.
- Added strict immutable project, source-image, artifact, pipeline, stage-result, error, generator-capability, engine-manifest, and consent domain models.
- Added deterministic clock and project-repository ports plus five generated Draft 2020-12 schemas.
- Added domain/schema/contract/architecture tests and a pre-pytest macOS Qt repair launcher; the B03 gate passes 80 tests.
- Added portable project layouts, Unicode/Windows-safe generated names, strict root containment, and symlink/reparse-point guards.
- Added validated atomic file replacement and deterministic bounded artifact hashing with injected-failure coverage.
- Added Arabic, long-path, traversal, link, hash, and atomic-write tests; the B04 portable gate passes 113 tests.
- Added validated local project manifests, UUID workspaces, recent-project discovery, immutable artifact promotion, and categorized inventory.
- Added durable checkpoint/journal recovery, explicit recovery decisions, and truthful schema-migration dispatch without a fake v2 route.
- Added identity- and active-use-gated logical project deletion with reparse refusal and storage-limitation receipts; the B05 portable gate passes 142 tests.
- Added stable structured event IDs, recursive secret/path/image redaction, rotating JSON logs, and bounded retention/excerpts.
- Added strict offline-first local settings with opaque secret references, protected no-interpolation `.env` import, and closeable secret values.
- Added a Windows Credential Manager adapter boundary with portable injected-backend contracts; the B06 portable gate passes 169 tests.

### Fixed

- Upgraded pytest from vulnerable 8.4.2 to 9.1.1 after `pip-audit` identified `PYSEC-2026-1845`; the repeated audit reports no known dependency vulnerabilities.
- Rejected PySide6 6.9.3 after a reproducible macOS QtTest/platform-plugin abort and upgraded to PySide6 6.10.3, then cleared an unexpected hidden flag from the ignored plugin tree so offscreen tests could run reliably.

### Not Yet Implemented

- Runnable PySide6 application.
- Project storage, recovery, image processing, masking, viewer, Blender, generator, validation, and export code.
- AI engines or model weights.
- Windows installer or supported release.

The changelog must never list a planned capability as implemented before its mandatory tests pass.
