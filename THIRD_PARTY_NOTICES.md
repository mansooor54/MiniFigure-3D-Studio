# Third-Party Notices

**Status:** Stage 2 foundation. This file is an index and does not claim that every planned component is currently installed or redistributed.

## Notice Policy

The release process must generate this notice set from the exact locked environment, vendored assets, optional engine packages, and packaged binaries. Software licenses and model-weight licenses are reviewed separately. An item is marked **Planned** until the exact redistributed artifact is selected and inventoried.

| Component family | Planned role | Current redistribution status | Notice action |
|---|---|---|---|
| Python 3.11 | Core runtime | Not packaged | Add exact Python license and bundled-runtime notices during packaging. |
| PySide6 / Qt 6 | Desktop UI and process control | Not installed or packaged by this repository yet | Record selected modules, LGPL/commercial path, Qt notices, and source/relinking information. |
| Qt WebEngine / Chromium | Offline viewer host | Deferred until viewer milestone | Include exact Qt WebEngine, Chromium, and third-party notice set for the selected build. |
| Blender | External mesh-processing engine | Not redistributed in Stage 2 foundation | Record tested version and Blender GPL notice. Publish Blender API scripts separately under a GPL-compatible license. |
| Three.js | Bundled offline 3D viewer | Deferred until viewer milestone | Vendor exact source/version and MIT license; no CDN dependency. |
| Pillow / NumPy / OpenCV / ImageHash | Image decoding and quality analysis | Deferred until image milestone | Collect exact wheel and bundled native/codecs notices. |
| ONNX Runtime | Local background inference | Deferred until mask milestone | Include exact runtime license and provider inventory. |
| Background-removal model weights | Person segmentation | No model selected or redistributed | Add exact source, revision, hash, license, and owner approval before installation. |
| Hunyuan3D or alternative generator | Image-to-3D generation | No engine selected, installed, or redistributed | Maintain a separate engine manifest, license, territory policy, model hashes, and notices. |
| PyInstaller | Development/Windows packaging | Deferred until hardening milestone | Include PyInstaller license/exception notice and the licenses of all bundled dependencies. |
| Test and audit tools | Development quality checks | Not runtime components | Record development SBOM separately; do not imply runtime redistribution. |

## Generated Notice Artifacts

The future release process will place exact notices and required source or written-offer material under `licenses/` and `packaging/licenses/`. A release is blocked when a packaged file cannot be mapped to the SBOM and its applicable notice/source obligation.
