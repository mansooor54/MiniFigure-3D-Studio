# MiniFigure 3D Studio — Stage 2 Environment and Dependency Plan

**Author:** Manus AI  
**Status:** Implementation plan; exact package locks are created only after native Windows compatibility tests

## 1. Environment Topology

MiniFigure 3D Studio requires multiple isolated environments because the Python 3.11 PySide6 desktop shell, Hunyuan's upstream-oriented Python/PyTorch/CUDA stack, Blender's embedded Python API, COLMAP, and the TypeScript viewer have different runtime and licensing constraints.

| Environment | Purpose | Included in core interpreter? | Stage 2 policy |
|---|---|---:|---|
| Core desktop | PySide6 UI, domain, storage, image quality, orchestration, validation, export coordination | Yes | Python 3.11 x64 virtual environment during development; later packaged by PyInstaller. |
| Image inference worker | ONNX background-removal inference | Prefer separate worker process; Python dependencies may share a managed package at first | CPU baseline; GPU provider optional and separately tested. |
| Hunyuan or alternative local generator | Shape/texture generation | **No** | Separate environment and process; exact runtime follows the selected engine's tested stack and license gate. |
| Blender | Mesh cleanup, base, scaling, renders, selected exports | **No** | External supported Blender LTS executable in background mode using separate GPL-compatible scripts. |
| Viewer build | Compile pinned TypeScript/Three.js assets | No runtime Node dependency | Node/pnpm only for development build; application ships local static viewer assets. |
| COLMAP | Deferred Stage 3 photogrammetry | No | No Stage 2 runtime requirement, though the adapter port and manifest schema may exist. |
| Test tools | pytest, pytest-qt, type/lint/audit/SBOM tools | Development only | Separate development dependency group; not shipped unless required by a runtime library. |

## 2. Supported Development Host

The authoritative build and integration environment is native Windows because the target product uses Qt WebEngine, Windows credential APIs, Windows process trees, PyInstaller, native DLLs, reparse points, and Windows path semantics. Linux may run portable unit tests, but it cannot satisfy a Windows milestone gate.

| Host item | Stage 2 baseline |
|---|---|
| Primary development OS | Windows 11 x64, current supported update level selected at M0. |
| Compatibility smoke OS | Windows 10 x64 supported build selected at M0. |
| Core Python | One Python 3.11 x64 patch version, pinned after PySide6 and native-wheel resolution. |
| Shell | PowerShell 7 preferred for scripts; Windows PowerShell compatibility only where required. |
| Version control | Git with long-path support documented; repository avoids path-depth excess. |
| GPU | Optional for core shell; mandatory only for a selected local generator that requires it. |
| Build architecture | x86-64 Stage 2 baseline. ARM64 is out of Stage 2 unless explicitly added. |
| Display | Test at 100%, 125%, 150%, and 200% scaling. |
| Locale/path cases | English LTR and Arabic RTL; Arabic, spaces, quotes, long names, and non-ASCII project paths. |

## 3. Repository Environment Files

| File | Role | Rule |
|---|---|---|
| `pyproject.toml` | Authoritative package metadata, dependency groups, pytest, Ruff, mypy, and coverage configuration | Human-reviewed and version controlled. |
| `requirements.txt` | Direct core dependencies for the requested project layout | Generated or synchronized from the authoritative metadata; no transitive version guesswork. |
| `requirements-dev.txt` | Development/test/build direct dependencies | Never imported by runtime modules. |
| `requirements-lock.txt` | Fully resolved and hashed core Windows lock | Created only after native Windows resolver and smoke tests. |
| `requirements-dev-lock.txt` | Fully resolved development lock | CI uses the same lock. |
| `.python-version` | Core development Python patch | Does not control Hunyuan or Blender Python. |
| `.env.example` | Provider variable names and comments only | Contains no values, secrets, personal endpoints, or enabled provider. |
| `packaging/engine_manifests/*.json` | Non-core executable/model/runtime provenance | Exact versions, hashes, licenses, regions, protocol range, and self-test. |
| `viewer/package.json` and lock | Viewer build dependency manifest | Lock exact Three.js/build tool graph; no runtime CDN. |

## 4. Core Desktop Dependency Groups

The Stage 1 register approved dependency families, not arbitrary latest versions. Stage 2 first proves a minimal set and adds optional libraries only when their owning milestone needs them.

| Group | Candidate direct dependencies | Earliest milestone | Notes |
|---|---|---:|---|
| UI core | PySide6 modules for Core, Gui, Widgets, Test, Linguist tools as needed | M1–M3 | WebEngine and WebChannel enter at M7 rather than inflating the first shell. Qt module allowlist is tracked for notices.[1] [2] |
| Models/schemas | pydantic, jsonschema, PyYAML | M1–M2 | YAML uses safe loading and schema validation. |
| Paths/platform | platformdirs | M1–M2 | Windows storage roots are explicit and testable. |
| Logging/config | structlog, python-dotenv | M1–M2 | Redaction precedes every sink; `.env` is compatibility input, not a vault. |
| Credentials | keyring with verified Windows backend or direct Windows credential adapter | When an external provider is selected | No external provider means this dependency may remain optional in Stage 2. |
| Process/system | psutil | M4 | Used for process tree and resource inspection; `QProcess` remains the launch primitive. |
| Images | Pillow, NumPy | M5 | Minimal decoding and metrics baseline. |
| Image analysis | OpenCV headless, ImageHash | M5 | Add only after wheel/DLL/notice test. |
| Optional mask utilities | scikit-image | M6 only if needed | Prefer fewer native dependencies if equivalent tested operations exist. |
| Background inference | onnxruntime CPU | M6 | GPU provider is a distinct engine/package decision. |
| Mesh validation | trimesh, pygltflib | M7/M11 | Restrict optional importer paths; use independent reopen checks. |
| Compression | zstandard | Only if checkpoint size tests justify it | Avoid premature dependency. |

## 5. Version-Selection Workflow

No package is frozen merely because it is newest. Each native or UI dependency follows a compatibility record.

| Step | Action | Evidence |
|---:|---|---|
| 1 | Identify versions supporting the pinned Python 3.11 patch and Windows x64 | Package metadata and official documentation links. |
| 2 | Resolve the smallest direct dependency set for the milestone | Resolver output and dependency graph. |
| 3 | Install from clean cache into a clean Windows environment | Installation transcript and hashes. |
| 4 | Run import and minimal capability probes | Probe report for Qt plugins, WebEngine resources, codecs, DLLs, and selected providers. |
| 5 | Run milestone unit/integration/smoke tests | Test report with environment manifest. |
| 6 | Inventory licenses, notices, bundled DLLs/codecs, and known vulnerabilities | SBOM, license collector, and audit output. |
| 7 | Freeze resolved versions and hashes | Lock file committed with compatibility record. |
| 8 | Reproduce from lock on a second clean environment | Reproducibility report. |

Any dependency update re-enters at Step 3 and must rerun affected milestone gates. The plan does not permit a global automated “latest” update to alter Qt, NumPy/OpenCV, ONNX Runtime, PyInstaller, or viewer assets without integration evidence.

## 6. Hunyuan or Alternative Generator Environment

The official Hunyuan3D 2.1 repository documents a separate Python 3.10/PyTorch/CUDA-oriented setup and substantial VRAM requirements, which is incompatible with treating it as a normal core PySide6 import.[3] The selected generator environment is therefore an installable engine package with a narrow file/JSON protocol.

| Manifest field | Required value |
|---|---|
| Engine identity | Stable adapter ID, display name, vendor/project, local/external classification. |
| Version provenance | Code commit/tag, model revisions, dependency lock, Python/runtime, build date. |
| Integrity | SHA-256 for package and model assets; optional code-signing identity. |
| License | SPDX where appropriate, full license path/hash, acceptance requirement, permitted territories. |
| Hardware | Supported CPU/GPU modes, CUDA/provider range, minimum/recommended VRAM/RAM/disk derived from tested configurations. |
| Capabilities | Single/multi-image, texture support, progress, cancel, resume/pause, output formats. |
| Protocol | Minimum/maximum worker protocol and request/result schema versions. |
| Self-test | Command, expected outputs, timeout, and last successful result. |

The core application does not activate a local generator solely because an executable exists. It validates the manifest, territory policy, protocol compatibility, hashes, self-test, and current resource preflight first.

## 7. Blender Environment

Blender is invoked using its direct command-line arguments for background execution and a Python script, not through a shell string.[4] Stage 2 begins with discovery of a supported user-installed Blender LTS rather than bundling a large managed runtime before compliance and installer work is proven.

| Check | Required behavior |
|---|---|
| Discovery | Search only approved locations and user-selected path; no arbitrary PATH trust without validation. |
| Version | Accept one tested LTS range; reject unsupported major/API versions with remediation. |
| Self-test | Launch background process, execute protocol script, write result, reopen result, verify version. |
| Isolation | Minimal environment and safe working directory outside untrusted project inputs. |
| Scripts | Separate GPL-compatible source component because Blender Python API scripts carry GPL-compatible publication requirements.[5] |
| Output | Staging only; application validates structured result and artifact before promotion. |

## 8. Background-Removal Model Environment

The model is an asset package independent of the adapter software. The rembg repository illustrates why software licensing cannot be used as a proxy for weight licensing: its current documentation warns that the default BRIA model needs separate commercial terms.[6]

| Gate | Requirement |
|---|---|
| Rights | Commercial use and redistribution conditions reviewed for the exact weights. |
| Identity | Model name, revision, source, file hashes, license hash, expected input/output. |
| Quality | Synthetic/licensed portrait benchmark covering hair edges, loose clothing, accessories, full body, and dark/light backgrounds. |
| Runtime | CPU timing/memory benchmark; optional GPU provider evaluated separately. |
| Install | Explicit user action, HTTPS source, expected size, checksum validation, atomic placement, rollback. |
| Offline | Once installed, inference works without network and makes no update/analytics request. |

## 9. Viewer Build Environment

Three.js is MIT-licensed and can be bundled locally.[7] Stage 2 uses a locked viewer source tree and creates a static distribution copied into the application asset directory.

| Build rule | Requirement |
|---|---|
| Package manager | One locked package manager and lockfile; no unpinned global plugin dependency. |
| Runtime assets | JavaScript, styles, loaders, controls, fonts/icons, and environment assets are local. |
| Source maps | Development builds only unless release policy approves redacted maps. |
| Content security | Default deny for remote sources, network requests, popups, navigation, and unapproved schemes. |
| Bridge | Versioned schema; no arbitrary file path, code evaluation, or general RPC. |
| Reproducibility | Clean build hash and asset manifest generated in CI. |

## 10. Test Environment Matrix

| Tier | Environment | Required tests | Stage 2 gate |
|---|---|---|---|
| T0 | Portable unit-test environment | Domain invariants, schemas, state machine, pure calculations, redaction, fixtures | Required on every change; not a substitute for Windows. |
| T1 | Native Windows 11 CPU | Core shell, project storage, image import/quality, mask CPU, fake processes, viewer, Blender CPU, exports, Arabic paths | Mandatory for each owning milestone. |
| T2 | Native Windows 11 supported NVIDIA GPU | Selected local generation engine and optional background GPU provider | Mandatory if Stage 2 uses that local GPU engine. |
| T3 | Clean Windows 10 x64 | Shell, file/process paths, viewer, Blender, export, development package smoke | Required before MVP approval where the declared target includes Windows 10. |
| T4 | Clean Windows 11 x64 | Installation/setup reproduction and development package smoke | Mandatory before MVP approval. |
| T5 | Network-denied Windows environment | Complete local workflow and viewer | Mandatory. |
| T6 | Fault-injection Windows environment | Process kill, child process, disk full, permission denied, locked files, malformed result, stale output | Mandatory by affected milestone. |

If hardware or an OS tier is unavailable, its tests are reported as **Not Run** and the associated support claim remains unapproved.

## 11. CI and Local Quality Lanes

| Lane | Trigger | Scope |
|---|---|---|
| Fast | Every change | Ruff, mypy, schema/unit tests, asset/secret scan. |
| Windows integration | Merge request and milestone branch | PySide6, filesystem, `QProcess`, Arabic paths, fake engines, viewer tests. |
| Blender | Blender-script or mesh-pipeline changes | Supported real Blender plus fixture suite. |
| Viewer | Viewer/bridge changes | TypeScript tests, deterministic build, CSP/network-deny test. |
| Generator | Adapter/manifest changes and controlled environment | Real engine self-test, success/failure/resource/cancel tests; may be manually triggered due resource cost. |
| Security/compliance | Merge request and release candidate | Dependency audit, SBOM, notices, seeded-secret scan, binary/asset inventory. |
| Package smoke | Milestone candidate | PyInstaller development build on Windows, clean-machine startup, Qt plugin/WebEngine resource verification. |

## 12. Runtime Storage Separation

| Data | Proposed root | Backup/update behavior |
|---|---|---|
| Application settings | `%LOCALAPPDATA%\MiniFigure3DStudio\config` | Small, schema-versioned, no project images. |
| Credentials | Windows Credential Manager/DPAPI reference | Never in project, repository, command line, or diagnostic bundle. |
| Engines/models | `%LOCALAPPDATA%\MiniFigure3DStudio\engines\<id>\<version>` | Separate manifests, explicit install/uninstall, rollback. |
| Cache | `%LOCALAPPDATA%\MiniFigure3DStudio\cache` | Bounded and user-clearable; no authority for project artifacts. |
| Logs/recovery | `%LOCALAPPDATA%\MiniFigure3DStudio\logs` and `recovery` | Bounded/redacted; recovery references project IDs, not image content. |
| Projects | User-selected root; suggested Documents folder | Project-specific retention and explicit deletion inventory. |

## 13. Development Packaging Strategy

Stage 2 should create a **directory-based PyInstaller development bundle** before experimenting with a one-file executable. PyInstaller's exception permits packaging commercial applications, but dependency licenses still govern redistributed components.[8] A directory build makes Qt DLL/plugin replacement, WebEngine resource inspection, notices, debugging, and clean-machine diagnosis more transparent.

The Stage 2 package excludes Hunyuan weights, background-model weights, managed Blender, and COLMAP unless their separate package gates are explicitly completed. The final signed installer and optional engine packages remain Stage 3.

## 14. Environment Gate Checklist

Before application source implementation begins, the bound workspace, Windows environment, Python patch, repository status, and M0 decisions are recorded. Before each native dependency is added, its owner, minimal need, version-selection record, license posture, and test plan exist. Before a milestone closes, a clean environment reproduces its lock and tests.

## References

[1]: https://doc.qt.io/qtforpython-6/licenses.html "Licenses Used in Qt for Python"
[2]: https://doc.qt.io/qt-6/qtwebengine-licensing.html "Qt WebEngine Licensing"
[3]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Tencent Hunyuan3D 2.1 Repository"
[4]: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html "Blender Command-Line Arguments"
[5]: https://www.blender.org/about/license/ "Blender License"
[6]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
[7]: https://github.com/mrdoob/three.js "Three.js Repository"
[8]: https://pyinstaller.org/en/stable/license.html "PyInstaller License"
