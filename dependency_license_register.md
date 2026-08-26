# MiniFigure 3D Studio — Proposed Dependency and License Register

**Author:** Manus AI  
**Status:** Stage 1 proposal; versions must be locked and re-audited in a reproducible Windows build before release.  
**Legal notice:** This is an engineering compliance plan, not legal advice.

## 1. Selection Principles

The desktop shell will target **Python 3.11** and keep heavy AI, Blender, and COLMAP runtimes outside the GUI interpreter. The release process will maintain separate manifests for the core application, background-removal model, Hunyuan3D engine environment, Blender runtime and scripts, COLMAP binary, Three.js viewer assets, fonts/icons, and optional external-provider adapters. This separation is necessary because packaging an application does not replace the license obligations of its dependencies.[1] [2]

All versions shown as “lock after spike” require a clean Windows 10/11 compatibility run before approval for implementation. Current package metadata was collected on 2026-08-26 to identify likely licenses and Python constraints, but metadata is not a substitute for reviewing the exact installed artifacts and their notice files.

## 2. Core Desktop Runtime

| Dependency | Proposed role | License posture | Version policy | Stage 1 decision |
|---|---|---|---|---|
| Python 3.11 | Desktop runtime | Python Software Foundation license; include Python notices | Pin one supported 3.11 patch release | **Approve** for the desktop shell. |
| PySide6 / Qt 6 | Widgets, localization, process control, settings, WebChannel, WebEngine | PySide6/Qt modules are available under LGPL/GPL/commercial combinations; exact module audit and LGPL compliance are mandatory.[3] [4] | Pin one tested Qt for Python release with Python 3.11 wheels | **Approve conditionally** under a documented dynamic-linking compliance path or commercial Qt license. |
| platformdirs | User data/cache/config locations | MIT according to current package metadata | Pin in lock file | **Approve**. |
| pydantic | Typed configuration and result-envelope validation | MIT according to current package metadata | Pin in lock file | **Approve**. |
| structlog | Structured event logging | MIT or Apache-2.0 according to current metadata | Pin in lock file | **Approve** with mandatory redaction processors. |
| python-dotenv | `.env` compatibility and import | BSD-3-Clause according to current metadata | Pin in lock file | **Approve**, but `.env` is not treated as a cryptographic vault. |
| keyring plus Windows credential backend | Preferred external-provider credential persistence | MIT for the Python package; Windows APIs remain platform services | Pin and test the selected backend | **Approve conditionally** after Windows Credential Manager integration tests. |
| psutil | Process tree, memory, and system capability inspection | BSD-3-Clause according to current metadata | Pin in lock file | **Approve**. |
| PyYAML | Human-editable presets | MIT according to current metadata | Pin in lock file; safe loader only | **Approve** with schema validation. |
| jsonschema | Versioned worker/result schemas and preset validation | MIT according to current metadata | Pin in lock file | **Approve**. |
| zstandard | Optional checkpoint and diagnostics compression | BSD-3-Clause according to current metadata | Pin in lock file | **Approve**. |

## 3. Imaging and Quality Analysis

| Dependency | Proposed role | License posture | Version policy | Stage 1 decision |
|---|---|---|---|---|
| Pillow | Image decoding, EXIF orientation, thumbnails, synthetic fixtures | MIT-CMU in current package metadata; bundled codecs require release audit | Lock a Python 3.11-compatible wheel | **Approve conditionally** after codec notice audit. |
| NumPy | Numeric arrays and image/mesh metrics | BSD family plus bundled third-party notices in current metadata | Do not take the newest release blindly; lock a release whose `Requires-Python` includes 3.11 | **Approve conditionally** after resolver and ABI test. |
| OpenCV headless | Blur/exposure/coverage metrics, feature-based duplicate detection | Apache-2.0 for current Python distribution metadata; native components require notices | Lock a Python 3.11-compatible headless wheel | **Approve conditionally** after DLL and codec inventory. |
| ImageHash | Perceptual near-duplicate screening | BSD-2-Clause according to current metadata | Pin in lock file | **Approve** as one signal, not the only duplicate test. |
| scikit-image | Optional morphology, exposure, and mask utilities | Primarily BSD with separately licensed incorporated files in current metadata | Lock a Python 3.11-compatible wheel | **Approve conditionally** after notice aggregation. |
| ONNX Runtime | Local background-removal inference | MIT according to current metadata | CPU is core; GPU provider is an optional engine package | **Approve conditionally** after Windows provider tests. |
| rembg software | Candidate background-removal adapter implementation | MIT for software, but model weights have independent licenses; current documentation warns that its default BRIA model needs a paid commercial agreement.[5] | Pin only after choosing an approved model | **Do not approve as a bundled model solution yet**. Approve the adapter concept, not the default weights. |
| Background segmentation weights | Person mask generation | Model-specific | Pin model ID, revision, hash, license hash, and source | **Open decision**. Requires quality and commercial-redistribution review. |

## 4. 3D Processing, Viewer, and Export

| Dependency | Proposed role | License posture | Version policy | Stage 1 decision |
|---|---|---|---|---|
| Blender | Background mesh repair, modifiers, booleans, previews, BLEND/STL/OBJ/GLB support | GPL; official guidance states distributed Blender API scripts must use a GPL-compatible license.[6] | Choose a tested LTS release; do not follow `latest` automatically | **Approve conditionally** as an external process. Decide separate-install discovery versus managed runtime after licensing and installer-size spike. |
| Blender automation scripts | Deterministic pipeline executed inside Blender | GPL-compatible source component because it uses Blender's Python API.[6] | Version with a script protocol and minimum/maximum Blender range | **Approve conditionally** with separate source distribution, notices, and legal review. |
| trimesh | Lightweight mesh inspection, fixtures, independent validation | MIT according to current metadata | Pin in lock file and restrict optional importers | **Approve conditionally**; not a substitute for Blender validation. |
| pygltflib | Independent GLB/glTF structure checks | MIT according to current metadata | Pin in lock file | **Approve** for validation and metadata inspection. |
| lib3mf | Standards-focused 3MF creation, reading, and validation | BSD; third-party credits apply.[7] | Pin one Windows SDK/binding release in Stage 3 | **Approve conditionally** after Python binding and slicer round-trip spike. |
| Three.js | Offline integrated 3D viewer | MIT.[8] | Vendor one exact release plus required loaders and controls | **Approve** with CSP, navigation blocking, and no CDN. |
| Qt WebEngine / Chromium | Host for the local Three.js viewer | Qt and Chromium have multiple license obligations and a large notice set.[4] | Same tested Qt release as PySide6 | **Approve conditionally**; exact distribution notices and source/offer path are release gates. |
| Noto Sans Arabic / Noto Sans | Proposed bilingual fonts | SIL Open Font License for selected files, subject to exact asset verification | Vendor exact font files and license | **Approve conditionally** after asset-level verification. |

## 5. Generation and Photogrammetry Engines

| Dependency | Proposed role | License posture | Version policy | Stage 1 decision |
|---|---|---|---|---|
| Hunyuan3D 2.1 | Default local image-to-shape and PBR texture engine where licensed | Tencent Hunyuan 3D 2.1 Community License with material territorial restrictions and distribution/use conditions.[9] | Pin code commit, model revisions, hashes, upstream environment, and accepted license hash | **Blocked for universal distribution**. It cannot be enabled or distributed in the EU, UK, or South Korea under the reviewed community license. Obtain separate rights or provide a compliant alternative. |
| Hunyuan engine environment | Separate Python/PyTorch/CUDA/native stack | Mixed transitive licenses plus model license | Reproduce the upstream-tested Python 3.10/PyTorch/CUDA stack unless a Stage 2 test validates another combination | **Approve architecture only**. Never merge into the Python 3.11 GUI process. |
| COLMAP | Structure-from-Motion and Multi-View Stereo | New BSD for COLMAP itself; upstream warns its third-party dependencies can affect a particular build's obligations.[10] | Pin one binary/source provenance and feature set | **Approve conditionally** as an external supervised CLI after a Windows dependency audit. |
| Optional external generator SDKs | Tripo, Meshy, or future providers | Provider-specific SDK/API terms | Prefer internal HTTP adapters to unnecessary vendor SDKs | **Deferred** until a provider is selected. Explicit consent and service disclosure remain mandatory. |

## 6. Build, Test, and Compliance Tooling

| Dependency | Proposed role | License posture | Version policy | Stage 1 decision |
|---|---|---|---|---|
| PyInstaller | Windows application bundle | GPL with an official exception allowing commercial bundles, subject to dependency licenses.[2] | Pin and build on native Windows CI | **Approve**. |
| pytest / pytest-qt | Unit, integration, and UI tests | MIT according to current metadata | Pin development lock | **Approve**. |
| Hypothesis | Property-based tests for dimensions, paths, schemas, and cancellation state | MPL-2.0 according to current metadata | Development dependency only | **Approve**. |
| Ruff / mypy | Formatting, linting, and static type checks | MIT according to current metadata | Development dependency only | **Approve**. |
| coverage.py | Coverage measurement | Apache-2.0 according to current metadata | Development dependency only | **Approve**. |
| pip-audit | Known-vulnerability scanning | Apache-2.0 according to current metadata | CI tool | **Approve**. |
| CycloneDX Python tooling | SBOM generation | Apache-2.0 according to current metadata | CI/release tool | **Approve**. |

## 7. Explicitly Rejected or Deferred Defaults

| Candidate | Decision | Reason |
|---|---|---|
| Fetching Three.js from a CDN | **Reject** | Violates the offline-runtime requirement and adds supply-chain and privacy exposure. |
| Importing Hunyuan3D into the PySide6 interpreter | **Reject** | Upstream tested a different Python/PyTorch stack, and engine failures or GPU exhaustion must not destabilize the GUI.[9] |
| Calling Blender through an unquoted shell command | **Reject** | Increases injection and Unicode-path risk; use an executable plus argument vector through `QProcess`. Blender provides direct background and Python-script arguments.[11] |
| Treating `rembg`'s default model as automatically redistributable | **Reject** | The software and model licenses are separate; the documented current default requires commercial terms for commercial use.[5] |
| Hand-writing 3MF ZIP/XML without a standards library | **Reject for Stage 3 default** | lib3mf provides read, write, conversion, and validation support, while the specification defines dedicated multi-material resources.[7] [12] |
| One-file PyInstaller bundle for all engines and weights | **Reject** | It produces poor update, rollback, startup, notice, territory-control, and installer-size characteristics. Use a core installer plus optional signed engine packages. |

## 8. Release Compliance Gate

A release is blocked unless the build produces an SBOM, license and notice bundle, exact engine/model manifest, hashes for vendored assets, corresponding-source or written-offer materials required by applicable LGPL/GPL components, Blender script source, a COLMAP third-party dependency inventory, and a territory/license decision for Hunyuan3D. Qt modules and Chromium notices must be derived from the exact shipped Qt build.[3] [4]

The release candidate must also pass clean-machine tests on supported Windows versions, Python-free startup tests, Qt DLL replacement/relinking documentation review, offline viewer tests with all networking denied, signed installer and binary checks, Arabic-path tests, and exporter round-trip tests.

## 9. Current Critical Decisions Requiring Owner Approval

| Decision | Recommended option |
|---|---|
| Hunyuan3D excluded territories | Approve a territory-gated optional engine package and commission a compliant alternative local adapter before claiming worldwide local AI support. |
| Qt license path | Use dynamic LGPL compliance for development unless the business selects commercial Qt terms; perform legal review before public distribution. |
| Blender distribution | Begin Stage 2 with discovery of a supported separately installed Blender LTS. Evaluate an optional managed Blender package only after size, source-offer, update, and license work is proven. |
| Background model | Run a Stage 2 benchmark and license review across candidate portrait segmentation weights; do not let a library's default choose the product's legal posture. |
| COLMAP distribution | Use one pinned official or reproducibly built Windows package with a generated third-party manifest. |
| 3MF target | Use lib3mf and test both standards validity and actual Orca Slicer/Creality Print recognition with synthetic fixtures. |

## References

[1]: https://doc.qt.io/qtforpython-6/licenses.html "Licenses Used in Qt for Python"
[2]: https://pyinstaller.org/en/stable/license.html "PyInstaller License"
[3]: https://www.qt.io/development/open-source-lgpl-obligations "Qt GPL and LGPL Obligations"
[4]: https://doc.qt.io/qt-6/qtwebengine-licensing.html "Qt WebEngine Licensing"
[5]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
[6]: https://www.blender.org/about/license/ "Blender License"
[7]: https://github.com/3MFConsortium/lib3mf "lib3mf Repository"
[8]: https://github.com/mrdoob/three.js "Three.js Repository"
[9]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Hunyuan3D 2.1 Repository"
[10]: https://github.com/colmap/colmap "COLMAP Repository"
[11]: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html "Blender Command-Line Arguments"
[12]: https://3mf.io/spec/ "3MF Specification Suite"
