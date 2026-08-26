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
- Installed and verified an isolated Python 3.11.16 development environment with PySide6 6.9.3.

### Fixed

- Upgraded pytest from vulnerable 8.4.2 to 9.1.1 after `pip-audit` identified `PYSEC-2026-1845`; the repeated audit reports no known dependency vulnerabilities.
- Cleared an unexpected macOS hidden flag from the ignored PySide6 plugin tree so the offscreen Qt platform plugin could be discovered during the B01 smoke test.

### Not Yet Implemented

- Runnable PySide6 application.
- Project storage, recovery, image processing, masking, viewer, Blender, generator, validation, and export code.
- AI engines or model weights.
- Windows installer or supported release.

The changelog must never list a planned capability as implemented before its mandatory tests pass.
