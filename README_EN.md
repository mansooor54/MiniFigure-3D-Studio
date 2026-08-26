# MiniFigure 3D Studio

**MiniFigure 3D Studio** is a planned Windows desktop application for converting permitted photographs of a person into a small 3D figure that can be reviewed, processed in Blender, and prepared for 3D printing.

## Current Status

The project is in **Stage 2 foundation implementation**. The architecture and implementation plan are approved, but the application is not yet runnable and no AI engine, model weights, Blender runtime, installer, or external provider is bundled.

The Stage 2 MVP will implement a local-first Fast AI workflow with project recovery, image validation, background masking, one legally usable generation adapter, an offline 3D viewer, Blender cleanup, minimum printability checks, and validated STL/GLB export. Accurate Scan, full printable-color/3MF support, advanced styles, complete Arabic localization, and the production installer remain Stage 3.

## Engineering Principles

The desktop shell targets Python 3.11 and PySide6. Heavy AI engines and Blender run outside the GUI process through versioned requests and validated results. Source photographs and raw generated meshes are immutable project artifacts. Long operations never run on the GUI thread. Exported files are reopened and validated before success is reported.

The application is local-first. External transfer requires a named provider, explicit consent, and credential handling that excludes API keys from source code, projects, logs, and command lines.

## Repository Safety

Do not commit real-person photographs, API keys, `.env` files, model weights, downloaded engines, project workspaces, build output, or diagnostic bundles. Test fixtures must be synthetic or have documented redistribution rights and an asset-manifest entry.

## Stage Documents

| Document | Purpose |
|---|---|
| [`docs/m0_decision_record.md`](docs/m0_decision_record.md) | Approved baseline and unresolved implementation gates. |
| [`SECURITY.md`](SECURITY.md) | Security reporting and development controls. |
| [`PRIVACY.md`](PRIVACY.md) | Local-first data handling and consent policy. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Code, testing, fixture, and milestone rules. |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | Dependency and redistributed-asset notice index. |

## Setup and Running

Setup commands, exact dependency locks, and run instructions will be added only after B01 dependency resolution and the first native Windows checks pass. Until then, no setup or runtime success is claimed.

## License Status

The application-shell license has not yet been selected by the owner. The repository is currently under private-development status; no public license grant should be inferred. Third-party components retain their own licenses and notices.
