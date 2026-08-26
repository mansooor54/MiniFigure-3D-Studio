# M0 Decision Record — Stage 2 Implementation Baseline

**Project:** MiniFigure 3D Studio  
**Repository:** `https://github.com/mansooor54/MiniFigure-3D-Studio.git`  
**Repository state at repair:** Stage 1 history preserved on `main`; `stage2/m0-b01` starts from the same Stage 1 commit  
**Implementation branch:** `stage2/m0-b01`  
**Recorded:** 2026-08-26  
**Status:** Core foundation may proceed; production engine/model enablement remains gated

## Approved Decisions

| Decision | Recorded outcome |
|---|---|
| Stage 1 | Approved by the product owner. |
| Stage 2 implementation plan | Approved by the product owner. |
| Workspace | Owner-provided repository is connected at `/Users/mansoor_almarzooqi/Documents/MiniFigure-3D-Studio`; Stage 1 content remains on `main` and implementation uses `stage2/m0-b01`. |
| Architecture | Local-first Python 3.11/PySide6 shell with heavy engines in separate processes/environments. |
| Blender | Discovery-first support for a separately installed, validated Blender LTS; no manual Blender opening required. |
| Qt development | LGPL-oriented dynamic packaging architecture unless the owner later selects commercial Qt. |
| Hunyuan | Optional isolated adapter only where the exact license/territory and hardware gates pass. |
| Background removal | Adapter and benchmark work may proceed; no model weights are enabled or redistributed before exact model approval. |
| Test assets | Synthetic or explicitly licensed fixtures only; no real-person photograph in the repository. |
| Stage progression | Portable work may continue on the repaired macOS/Python 3.11.16 baseline under `platform_baseline_exception.md`; Windows-only results remain Not Run and cannot support a Windows claim. No automatic Stage 3 work. |

## Open Owner Inputs

| Input | Current implementation treatment | Blocking point |
|---|---|---|
| Intended distribution territories | Unknown; do not enable or package Hunyuan | Real Hunyuan installation or execution. |
| Application-shell license | Private-development placeholder notice only; no public license grant inferred | Public distribution or open-source release. |
| Qt commercial versus LGPL | Use LGPL-oriented architecture for development; no release claim | Production installer release. |
| Background-removal model | No weights selected; fake/manual path only | Real automatic background removal. |
| Real Fast AI adapter | No production engine selected; contract/fake path only | Stage 2 real-generation gate. |
| Windows/GPU test hardware | Unavailable in the connected macOS workspace | Native Windows, GPU, Blender Windows, PyInstaller Windows, and clean-machine release gates. |
| Git author identity and push authorization | Connected desktop uses `mansooor54 <uaeriver@hotmail.com>` with authenticated Git transport | Available for publishing the isolated Stage 2 branch. |

## Implementation Authorization

B01 repository metadata and quality foundation may be created using conservative private-development defaults. No production image upload, external provider integration, Hunyuan execution, background-model download, or engine redistribution is authorized by this record.

## Revisit Triggers

This record must be updated before adding a public license grant, enabling external network transfer, installing model weights, enabling a real generator, publishing a package, or claiming Windows 10/11 support. Branch commits may be pushed through the connected desktop's authenticated Git transport.
