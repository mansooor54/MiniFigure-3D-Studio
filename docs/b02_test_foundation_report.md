# B02 Test and Synthetic-Asset Foundation Report

**Milestone:** M1 — Repository and Quality Foundation  
**Batch:** B02  
**Branch:** `stage2/m0-b01`  
**Date:** 2026-08-26  
**Gate result:** **Passed for the portable connected-desktop lane**

## Objective

B02 establishes deterministic tests, synthetic person-free fixtures, asset-policy enforcement, portable CI configuration, dependency evidence generation, and a documented result model. It does not implement application domain behavior or make a Windows support claim.

## Files Created

| File | Purpose |
|---|---|
| `tests/conftest.py` | Deterministic clocks/IDs, Arabic project roots, and in-suite Qt environment preservation. |
| `tests/test_smoke.py` | Python fixture, Arabic path, and live Qt widget smoke tests. |
| `tests/unit/test_asset_foundation.py` | Determinism, manifest, tamper, unmanifested-file, and real-person-policy tests. |
| `tests/unit/test_project_metadata.py` | Runtime/dev requirement synchronization and Python-version pin tests. |
| `tests/unit/test_workflow_config.py` | Read-only workflow permissions, platform matrix, and safe pull-request trigger tests. |
| `tests/fixtures/asset_manifest.yaml` | Source, generator, license, SHA-256, size, privacy flags, purpose, and expected results. |
| `tests/fixtures/generated/checker_64.ppm` | Deterministic high-frequency synthetic image. |
| `tests/fixtures/generated/gradient_64.ppm` | Deterministic exposure/intensity synthetic image. |
| `tests/fixtures/generated/unit_cube.obj` | Deterministic closed synthetic mesh. |
| `tests/fixtures/generated/open_plane.obj` | Deterministic open negative mesh. |
| `scripts/__init__.py` | Unambiguous development-tool package boundary for type checking. |
| `scripts/create_synthetic_fixtures.py` | Byte-deterministic fixture and manifest generator. |
| `scripts/validate_assets.py` | Manifest, hash, size, path, source/license, privacy, EXIF-policy, and coverage validator. |
| `scripts/generate_sbom.py` | Reproducible CycloneDX development SBOM wrapper with direct-component checks. |
| `scripts/collect_licenses.py` | Installed package inventory and available license-text collector. |
| `.github/workflows/quality.yml` | Python 3.11 Linux/macOS portable lint, type, test, audit, asset, SBOM, and license lane. |
| `docs/testing_strategy.md` | Test tiers, evidence vocabulary, platform labels, privacy, determinism, and gate format. |
| `docs/b02_test_foundation_report.md` | This completion evidence. |

## Files Modified

| File | Change |
|---|---|
| `.gitignore` | Narrowly unignored the two manifested synthetic OBJ fixtures. |
| `pyproject.toml` | Added pytest repository import path; raised PySide6 to 6.10 and pytest to fixed 9.x. |
| `requirements.txt` | Synchronized PySide6 6.10 requirement. |
| `requirements-dev.txt` | Synchronized fixed pytest 9.x requirement. |
| `CHANGELOG.md` | Recorded environment, security, and Qt repairs. |
| `docs/b01_foundation_report.md` | Synchronized the repaired PySide6 6.10.3 baseline. |

## Fixture Evidence

The generator produces four assets with stable bytes. The manifest records a fixed generator version, CC0-1.0 declaration, SHA-256, byte size, purpose, expected measurements, and explicit `contains_real_person: false` and `contains_exif: false` flags. The committed hashes are:

| Fixture | SHA-256 |
|---|---|
| `checker_64.ppm` | `42eb71c4f3d3db789c9fa72b905f1574ec74d6c8d32d5a7b8ba9bef57129bc1e` |
| `gradient_64.ppm` | `09d89889b6af0ed01f8850e5bd72d82dd382f427dd889647123259ef93bd5778` |
| `unit_cube.obj` | `8e764408a29828c1619c7dfd04559f911ae67784bfed6aa306968f414ae0a116` |
| `open_plane.obj` | `4202400853a2c2bd6567508e4beb94061d922d4a1e9c560891d15ef90a942ce6` |

Repeated generation produced identical file hashes. Seeded unmanifested files, tampered content, and a real-person manifest flag were rejected by tests.

## Quality Evidence

| Check | Result | Evidence |
|---|---|---|
| Ruff | Passed | All B02 scripts and tests passed with no findings. |
| mypy strict | Passed | Ten source files passed with no issues. |
| pytest | Passed | Sixteen tests passed; no failures or skips. |
| Asset validation | Passed | All committed fixtures and manifest entries validated. |
| Dependency audit | Passed | `pip-audit --local` reported no known vulnerabilities; the unpublished local project was skipped as expected. |
| SBOM | Passed | Reproducible CycloneDX JSON validated and contained all direct dependencies within 75 environment components. |
| License inventory | Passed for development review | Seventy-five installed packages and 17 direct dependencies were inventoried; available license texts were copied; no item remained `UNKNOWN`. |
| Workflow configuration | Passed | Tests confirmed read-only contents permission, Linux/macOS matrix, and no `pull_request_target`. |
| Qt smoke | Passed | PySide6 6.10.3 and pytest-qt created and processed a widget through the pre-pytest environment repair. |

Generated SBOM, audit, and license files remain under ignored `reports/generated/`; CI uploads them as short-lived evidence rather than committing machine-specific inventories.

## Failures Found and Repaired

| Failure | Repair |
|---|---|
| Ruff reported four long lines | Split messages and expressions; lint passed. |
| mypy saw the scripts twice under different module names | Added `scripts/__init__.py`; strict typing then exposed and drove fixes for metadata/path narrowing. |
| pytest could not import development scripts | Added an explicit repository-root `pythonpath` to pytest configuration without packaging scripts into the runtime. |
| PySide6 6.9.3 aborted when QtTest initialized an offscreen platform on macOS 26 | Raised the allowed baseline to PySide6 6.10; installed 6.10.3 and repeated the exact probe successfully. |
| `uv` extraction marked PySide6 platform plugins hidden on macOS | `scripts/run_tests.py` clears that flag before importing pytest/pytest-qt; conftest preserves the controlled Qt variables inside the suite. The repair is conditional to macOS. |
| Initial pytest 8.4.2 had `PYSEC-2026-1845` | Raised the floor to 9.0.3; installed 9.1.1; repeat audit passed. |
| CycloneDX received the interpreter path and found only pip/setuptools | Passed the virtual-environment root; the SBOM then contained 75 components and all direct dependencies. |
| Eight packages lacked modern license-expression metadata | Fell back to specific Trove license classifiers while preserving classifier and copied-text evidence; unknown count became zero. |

## Security and Privacy Review

No real-person image, model weight, engine, secret, project, diagnostic bundle, or external provider was added. CI has read-only repository contents permission. Fixtures are fully synthetic and generated locally. Dependency reports contain package metadata only and are ignored locally except when CI uploads them as time-limited artifacts.

## Platform Gaps

| Check | Status | Reason |
|---|---|---|
| Native Windows 10/11 quality lane | Not Run | No Windows runner or connected Windows machine is available yet. |
| Windows Qt plugin behavior | Not Run | macOS PySide6 evidence cannot establish Windows behavior. |
| Windows Credential Manager, process-tree, path, and packaging checks | Not Run | The corresponding adapters do not exist and require native Windows. |

## Gate Decision

B02 passes for portable implementation. The deterministic fixture, asset, lint, type, test, audit, SBOM, license, workflow, and Qt gates are satisfied on the connected macOS/Python 3.11.16 environment. B03 may begin. Windows-only evidence remains explicitly Not Run and must be added before a Windows-ready Stage 2 claim.

## Rollback

The B02 commit is the rollback point. Returning to the preceding B01 commit removes tests, generated fixtures, scripts, workflow, and B02 documentation without changing Stage 1 or any user data.
