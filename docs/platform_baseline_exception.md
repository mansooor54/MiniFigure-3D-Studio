# Platform Baseline Exception — Stage 2 Repair

**Recorded:** 2026-08-26  
**Owner direction:** Repair the blocked workflow and continue  
**Connected development computer:** macOS 26.5.2, Apple Silicon ARM64  
**Target product platforms:** Windows 10 and Windows 11

## Decision

Stage 2 implementation may proceed on the connected macOS development computer after B01's portable and target-Python checks pass. This exception changes the execution order only; it does not change the product target or convert macOS results into Windows evidence.

| Area | Treatment |
|---|---|
| Python | Use an isolated Python 3.11.16 environment on the connected desktop. |
| PySide6/core dependencies | Install, import, audit, and test on macOS now; repeat on native Windows before any Windows-support or release claim. |
| GitHub | Develop and publish through the connected desktop's authorized repository credentials. |
| UI/domain/process tests | Run portable and Qt offscreen tests on macOS during implementation. |
| Windows path/process/packaging behavior | Keep explicit platform markers and report as Not Run until a native Windows environment is attached. |
| PyInstaller installer | Do not build or claim the Windows EXE from macOS. |
| Blender/generator | Test only configurations actually available; do not infer Windows compatibility. |
| Stage 2 approval | May report a macOS development MVP with named Windows gaps, but cannot report Windows-ready status until native gates pass. |

## Repair Evidence

The connected desktop preserved the Stage 1 `main` history and provided authenticated Git write access. `uv` 0.12.6 installed an isolated Python 3.11.16 runtime after the Homebrew `python@3.11` formula failed with an unsupported installation step. The project dependencies installed successfully, PySide6 6.9.3 created and processed an offscreen Qt widget, an Arabic filename round-tripped, and the dependency audit passed after pytest was upgraded from vulnerable 8.4.2 to a fixed 9.x release.

## Non-Negotiable Limits

No Windows-only test is marked Passed from macOS. No Windows installer, Blender Windows integration, GPU support, or Windows 10/11 support claim is allowed without native evidence. Any platform-specific defect discovered later reopens the owning milestone.
