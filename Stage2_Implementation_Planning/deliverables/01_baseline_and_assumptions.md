# MiniFigure 3D Studio — Stage 2 Baseline and Planning Assumptions

**Author:** Manus AI  
**Status:** Stage 2 implementation-planning baseline  
**Stage 1 approval recorded:** 2026-08-26  
**Coding status:** Application coding has not started.

## 1. Approved Baseline

The product owner approved the Stage 1 package without requested changes. The following decisions therefore form the baseline for Stage 2 planning.

| Area | Approved baseline |
|---|---|
| Architecture | Local-first Python 3.11/PySide6 modular monolith with heavy engines isolated behind versioned worker or CLI boundaries. |
| Project model | Schema-versioned project manifest, immutable input/raw artifacts, derived revisions, transactional staging, atomic commit, and recovery journal. |
| Fast AI input | One selected primary front or 45-degree image enters an adapter unless that adapter explicitly declares multi-image support. Other images are separate references for selection and color review. |
| Hunyuan | Optional isolated engine package with an explicit license/territory gate; never imported into the GUI interpreter and never treated as globally available under the reviewed license. |
| Background removal | Adapter architecture approved; exact redistributed model weights remain a separate license/quality decision. |
| Blender | External background process; automation scripts remain a separately distributed GPL-compatible source component. |
| Viewer | Pinned Three.js assets bundled locally inside Qt WebEngine; remote navigation and network requests denied. |
| Export | Write to staging, reopen independently, validate semantics, then atomically finalize. A successful process exit alone is insufficient. |
| Localization | Arabic RTL and English LTR are architectural requirements from the first shell; Arabic paths are mandatory integration cases. |
| Progress/errors | Structured stage events, real progress where available, truthful indeterminate states, cancellation, capability-gated Pause, retry rules, redacted logs, and causal technical details. |
| Stage boundary | Stage 2 ends with a working Fast AI MVP and real test evidence. Stage 3 remains blocked until Stage 2 is reviewed and approved. |

## 2. Stage 2 MVP Scope

Stage 2 planning targets a **working Fast AI vertical slice**. It includes project creation/recovery, image import and quality checks, primary-image selection, local background removal with manual correction, one legally usable generation adapter, offline 3D preview, Blender cleanup/base/scale/previews, minimum truthful validation, and transactional STL/GLB export.

| In Stage 2 | Deferred to Stage 3 |
|---|---|
| Home/New Project/Mode/Import/View/Quality/Mask/Basic Style/Print Settings/Generate/Preview/Repair/Basic Validate/Export flow | Full Accurate Scan execution, although its UI may remain visibly unavailable with an explanation. |
| One approved local or external Fast AI adapter | Multiple production provider integrations. |
| One approved background-removal model | Broad segmentation model marketplace. |
| Basic Realistic and parameter infrastructure needed by the MVP | Complete Chibi, Bobblehead, Bust, Keychain, Bas-Relief, hollowing, drain holes, advanced strengthening, and text/base variants. |
| Blender cleanup, simple base, unit scaling, Z=0, four renders | Full semantic fragile-feature processing and complete printability repair suite. |
| Material preview and part inventory needed for GLB | Filament palette separation, 4/8/16 colors, and 3MF slicer interoperability. |
| Minimum validation blockers and qualified statuses | Complete wall, internal geometry, orientation, support, and overhang analysis. |
| STL and GLB | OBJ, BLEND, and 3MF production exports. |
| English-complete shell with Arabic architecture, critical strings, paths, and RTL tests | Complete professional Arabic translation review of every advanced feature, help page, report, and installer screen. |
| Development run and Windows smoke packaging | Production signed EXE installer and optional managed engine packages. |

## 3. Non-Negotiable Stage 2 Exit Criteria

The MVP is not complete until all mandatory checks actually run in a supported Windows environment and any skipped or failing check is disclosed. A synthetic or approved test image must travel through the real implemented path to a non-empty model, an offline preview, a Blender-processed artifact, and reopened STL/GLB outputs.

| Exit area | Required evidence |
|---|---|
| Responsiveness | Qt heartbeat remains responsive during every long-running operation. |
| Recovery | Forced process termination leaves the last committed manifest and artifacts readable. |
| Truthful failure | Missing engine, insufficient capability, malformed output, process crash, cancellation, and unwritable export all produce actual failure states without stale or placeholder success. |
| Privacy | Local workflow emits no network traffic; logs and diagnostic copies contain no image data, secrets, or unsafe full paths. |
| Unicode | Arabic project/model names and Arabic-containing paths pass import, process invocation, viewer loading, and export. |
| Generator | One adapter succeeds and fails under controlled tests; it accepts only capabilities it declares. |
| Blender | Synthetic broken-mesh fixtures prove backup, cleanup, metrics, base union behavior, scale, Z=0, and previews. |
| Export | STL and GLB reopen independently, have non-empty geometry, preserve expected dimensions, and match the current run provenance. |
| Documentation | Setup/run instructions, exact versions, changed-file list, known limitations, test report, and licensing status are current. |

## 4. External Constraints Preserved from Stage 1

The reviewed Hunyuan3D 2.1 community license excludes the European Union, United Kingdom, and South Korea from its licensed territory, so its package must remain gated and cannot be the only worldwide plan.[1] Its official repository documents a separate Python 3.10/PyTorch/CUDA-oriented environment and material VRAM demand, supporting process isolation and a preflight-first design.[2]

Qt/PySide6 development will follow the approved dynamic LGPL-compliance architecture unless the product owner later selects commercial Qt terms; exact redistributed modules and Qt WebEngine/Chromium notices remain release gates.[3] [4] Blender automation scripts that use Blender's Python API stay in the separate GPL-compatible component.[5]

Background-removal software and model weights remain separate approvals. The rembg project is not treated as permission to redistribute whichever weights it selects by default.[6]

## 5. Owner Inputs Still Needed Before Related Code Is Enabled

These inputs do not block writing the implementation plan, domain contracts, fake-engine tests, or local shell. They do block enabling the corresponding production integration.

| Input | Decision needed | Blocking point |
|---|---|---|
| Intended development and distribution territories | Confirm whether development/distribution includes the EU, UK, or South Korea | Hunyuan engine installation or execution. |
| Application-shell license | Proprietary/commercial or an identified open-source license | Public repository/release metadata and notice strategy. |
| Qt path | Dynamic LGPL compliance or commercial Qt | Release packaging; development may proceed under the approved LGPL-oriented architecture. |
| Background model | Exact model, revision, license, checksum, and redistribution approval | Real automatic background removal. |
| Generation engine | Hunyuan where eligible, a compliant alternative, or an explicitly selected external provider | End-to-end real generation acceptance test. |
| Blender runtime | Supported user-installed Blender LTS discovery first, or managed runtime | Real Blender integration setup. The approved default is discovery first. |
| Development workspace | Bound folder in Manus Desktop or an explicit local/repository path | Creation of application source files. |

## 6. Planning Assumptions Used Unless Changed

| Topic | Planning assumption |
|---|---|
| MVP operating-system matrix | Native Windows 11 development/test plus Windows 10 clean-machine smoke coverage where infrastructure is available. |
| Core dependency policy | Exact versions are selected through a compatibility spike and frozen only after Windows tests; no untested newest-version lock. |
| Background inference | ONNX Runtime CPU is the baseline packaging concept; GPU provider remains optional until tested. |
| Blender | Begin with discovery and validation of one supported Blender LTS installation. |
| Hunyuan | Use a fake adapter and protocol test first; real Hunyuan work begins only when territory, license, hardware, and environment gates pass. |
| External APIs | No provider integration is assumed. If chosen, credentials and consent are implemented before the first network request. |
| Test assets | Synthetic images/meshes only in the repository. Any real-person image remains outside version control and requires permission. |
| Installer | Stage 2 produces a development build/smoke package, not the final signed installer. |
| Branching | One milestone branch at a time; no later milestone begins while its prerequisite acceptance gate fails. |

## 7. Workspace Gate

No development folder is currently bound to this task. Stage 2 planning can be completed in the sandbox, but application source must not be created in an arbitrary temporary location. Before implementation begins, the owner should bind the intended project folder in Manus Desktop or provide the exact repository/path and confirm whether it is new or existing.

## References

[1]: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE "Tencent Hunyuan 3D 2.1 Community License"
[2]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Tencent Hunyuan3D 2.1 Repository"
[3]: https://www.qt.io/development/open-source-lgpl-obligations "Qt GPL and LGPL Obligations"
[4]: https://doc.qt.io/qt-6/qtwebengine-licensing.html "Qt WebEngine Licensing"
[5]: https://www.blender.org/about/license/ "Blender License"
[6]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
