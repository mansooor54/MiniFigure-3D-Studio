# B01 Repository Metadata and Quality Foundation Report

**Milestone:** M1 — Repository and Quality Foundation  
**Batch:** B01  
**Branch:** `stage2/m0-b01`  
**Date:** 2026-08-26  
**Gate result:** **Passed for portable Stage 2 implementation; Windows-only evidence remains Not Run**

## Objective

B01 establishes repository metadata, policy, direct dependency inputs, tool configuration, an isolated target-Python environment, and a reversible Git baseline. It does not claim that application features, AI engines, model weights, Blender integration, a Windows installer, or Windows support are implemented.

## Files Created

| File | Purpose |
|---|---|
| `.env.example` | External-provider variable names without values or an enabled service. |
| `.gitattributes` | UTF-8/text normalization and binary-asset declarations. |
| `.gitignore` | Exclude secrets, environments, models, engines, projects, generated viewer output, diagnostics, and build artifacts. |
| `.python-version` | Target interpreter patch used by the repaired environment: Python 3.11.16. |
| `CHANGELOG.md` | Truthful Stage 2 foundation history. |
| `CONTRIBUTING.md` | Milestone, type, test, privacy, dependency, and file-reporting rules. |
| `LICENSE` | Temporary private-development notice; no public application-shell license inferred. |
| `PRIVACY.md` | Local-first sensitive-data, consent, retention, deletion, and diagnostics policy. |
| `README_AR.md` | Arabic project status and safety documentation. |
| `README_EN.md` | English project status and safety documentation. |
| `SECURITY.md` | Security reporting and development controls. |
| `THIRD_PARTY_NOTICES.md` | Planned component notice index with no false redistribution claim. |
| `docs/m0_decision_record.md` | Approved baseline and open product/engine decisions. |
| `docs/platform_baseline_exception.md` | Authorization to continue portable work on macOS while keeping Windows-only evidence explicit. |
| `pyproject.toml` | Authoritative package metadata and pytest/Ruff/mypy/coverage configuration. |
| `requirements.txt` | Direct core dependency ranges. |
| `requirements-dev.txt` | Direct development, test, audit, and SBOM dependency ranges. |

This report is also B01 evidence.

## Repair Summary

The first isolated Linux clone could not publish because its GitHub integration lacked `contents:write`, and it could not provide target-platform evidence. The connected desktop repository was then inspected. Its Stage 1 `main` history was clean and preserved, `stage2/m0-b01` already existed remotely at the Stage 1 head, and the desktop Git identity and HTTPS transport were available.

The connected computer is macOS 26.5.2 on Apple Silicon. Homebrew's direct `python@3.11` installation failed with an unsupported `bootstrap_cpython` step after dependency installation. The repair installed `uv` 0.12.6, which installed an isolated Python 3.11.16 runtime. PySide6 6.9.3 passed a direct Qt smoke but reproducibly aborted when QtTest initialized the offscreen platform; PySide6 6.10.3 resolved that failure. These repairs change the development baseline only and are not Windows evidence.

## Checks Executed

| Check | Environment | Result | Evidence summary |
|---|---|---|---|
| Stage 1 preservation | Connected desktop Git | Passed | `README.md`, `Stage_1/`, and `Stage2_Implementation_Planning/` remained intact; `main` was not modified. |
| Branch isolation | Connected desktop Git | Passed | `stage2/m0-b01` tracks `origin/stage2/m0-b01`. |
| Whitespace/config diff | macOS ARM64 | Passed | `git diff --check` returned no error. |
| Ignore policy | macOS ARM64, Git | Passed | `.env`, model weights, project photos, generated viewer assets, and temporary probes matched the intended ignore rules. |
| Secret-pattern scan | macOS ARM64 | Passed | No suspected access key, provider key, private key, or populated API value was detected outside ignored environments. |
| Project metadata | Python 3.11.16 | Passed | `pyproject.toml` parsed and enforced `>=3.11,<3.12`. |
| Dependency installation | macOS ARM64, Python 3.11.16 | Passed | Runtime and development dependencies installed in ignored `.venv`; the project installed editable. |
| Core imports | macOS ARM64, Python 3.11.16 | Passed | PySide6, jsonschema, platformdirs, psutil, Pydantic, python-dotenv, PyYAML, and structlog imported. |
| Qt plugin visibility repair | macOS ARM64, ignored `.venv` | Passed | `uv`-extracted PySide6 plugins carried the macOS hidden file flag, so Qt scanned the directory but did not recognize platform plugins. Clearing the hidden flag on the ignored plugin tree restored discovery. |
| Qt smoke test | macOS ARM64, PySide6 6.10.3 | Passed | With the explicit installed plugin root, an offscreen `QApplication` created, displayed, processed, and closed a widget. |
| Arabic path round trip | macOS ARM64 | Passed | An Arabic directory and filename were created, written, read, and removed successfully. |
| Dependency audit, initial | Installed environment | Failed then repaired | `pip-audit` found `PYSEC-2026-1845` in pytest 8.4.2 with fixed release 9.0.3. |
| Dependency audit, final | Installed environment with pytest 9.1.1 | Passed | No known dependency vulnerabilities were reported; the unpublished local project was correctly skipped as non-PyPI. |
| Windows CPython 3.11 wheel resolution | Cross-platform resolver targeting `win_amd64`, CPython 3.11 | Passed as availability only | All direct/development requirements resolved to binary distributions. This is not native Windows execution. |

## Installed Candidate Snapshot

The repaired environment includes Python 3.11.16, PySide6 6.10.3, pytest 9.1.1, pytest-qt 4.5.0, Ruff 0.16.4, mypy 1.20.2, Pydantic 2.13.4, psutil 7.2.2, PyYAML 6.0.3, structlog 25.5.0, and python-dotenv 1.2.3. These are Stage 2 development candidates. Exact Windows locks, Qt plugin inventory, SBOM, notices, and vulnerability results must be regenerated on native Windows before a release claim.

## Not Executed

| Required check | Status | Reason |
|---|---|---|
| Native Windows 10/11 environment creation | Not Run | The connected development computer is macOS ARM64. |
| Native Windows dependency installation and Qt plugin smoke | Not Run | No Windows workspace is attached. |
| Windows path, process-tree, DPAPI/Credential Manager, PyInstaller, and clean-machine checks | Not Run | These require native Windows and remain mandatory before Windows support is claimed. |
| Ruff, mypy, and pytest against application source | Not Run in B01 | B01 intentionally contains no application package; B02 owns the first executable test foundation. |
| Final SBOM and complete packaged-license collection | Not Run | No runtime package or release artifact exists. |

## Gate Decision

B01 passes for portable Stage 2 implementation under `docs/platform_baseline_exception.md`. B02 may begin on the connected desktop because the target Python series, dependencies, core imports, Qt startup, Arabic path behavior, secret/ignore controls, and dependency audit pass. Windows-only tests remain explicitly Not Run and cannot be inferred from macOS results.

## Remaining Product Gates

| Input | Blocking point |
|---|---|
| Intended distribution territories | Hunyuan installation, execution, or packaging. |
| Final application-shell license | Public distribution and contribution acceptance. |
| Approved background-removal model | Real automatic background removal. |
| Legally usable real Fast AI adapter | Stage 2 generation completion. |
| Native Windows CPU/GPU/Blender test access | Windows support, packaging, and release approval. |

## Rollback

The branch starts from the preserved Stage 1 head. The B01 commit created on the connected desktop is the rollback checkpoint. Returning to `main` leaves Stage 1 unchanged. No real-person images, model weights, engines, or user projects were added.
