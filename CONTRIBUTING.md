# Contributing to MiniFigure 3D Studio

## Current Contribution Status

The repository is under private Stage 2 development. External contributions are not accepted until the owner selects a public license, contribution terms, and a security contact.

## Milestone Discipline

Work follows the approved Stage 2 milestones and file batches. A later behavior-changing batch does not begin while a mandatory prerequisite test fails. Each batch report lists files created and modified, dependencies, tests and environments, manual checks, known defects, rollback point, and gate result.

## Code Standards

| Area | Requirement |
|---|---|
| Python | Target Python 3.11; use complete public type hints, focused modules, dataclasses/value objects where suitable, and explicit `if`/`else`. |
| Boundaries | Domain and application layers depend on typed ports, not PySide6 widgets, HTTP clients, Blender, ONNX, or generator runtimes. |
| Dependency injection | Concrete adapters are assembled only in the composition root. |
| Long work | Never decode large inputs, hash unbounded data, infer, wait for processes, process meshes, or export on the GUI thread. |
| Paths/processes | Use `pathlib.Path`, generated safe names, containment checks, and executable-plus-argument-vector process launch. |
| Errors | Use stable codes, retryability, translated summary/action keys, redacted context, and causal technical details. |
| Artifacts | Preserve source/raw inputs; write to staging; validate result/provenance/hash/content; atomically promote. |
| Localization | User-facing text uses translation keys. English literals do not belong in services or adapters. |
| Logging | Structured and redacted before every sink. Never log secrets, images, masks, EXIF payloads, or unsafe full paths. |

## Tests

Add or update tests with every behavior change. Unit tests do not replace required native Windows, Qt, Blender, GPU, viewer, clean-package, or fault-injection evidence. Results are recorded as Passed, Failed, Skipped, Not Run, or Blocked; only Passed satisfies a mandatory gate.

## Test Assets

Real-person photographs and generated real-person likenesses are prohibited in source control and CI. Fixtures must be synthetic or have documented redistribution rights. Every binary fixture requires an asset-manifest record containing its source/generator, license, checksum, purpose, and expected findings.

## Dependencies

Before adding a package, document the owning requirement, alternatives, Windows/Python support, direct and transitive footprint, license/notice impact, native binaries/codecs, security posture, and removal plan. Resolve and test in a clean Windows environment before locking it.

## Change Checklist

1. Confirm the owning milestone/batch and prerequisite gate.
2. Record the clean starting revision and environment.
3. Add deterministic tests or a test plan for the intended behavior.
4. Implement the smallest coherent change.
5. Run focused and affected regression lanes.
6. Review security, privacy, localization, licensing, and artifact implications.
7. Update documentation, changelog, and exact file list.
8. Create a rollback checkpoint and record the gate decision.

## Commit Messages

Use concise milestone/batch context, for example: `M4 B10: supervise fake workers and validate results`. Do not include secrets, personal paths, or real-person names in commit messages.
