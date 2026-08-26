# MiniFigure 3D Studio — Stage 2 Engine and Release-Safe Integration Strategy

**Author:** Manus AI  
**Status:** Implementation plan; production engine enablement remains conditional on the recorded gates

## 1. Strategy Summary

Stage 2 must deliver one real, legally usable Fast AI adapter without coupling the desktop application to one vendor, Python stack, GPU family, or territorial license. Every engine is represented by a capability declaration, validated manifest, preflight, versioned request/result protocol, and actual artifact checks.

The core shell ships and runs without an AI engine. An engine becomes usable only after its package, license, territory, dependencies, hardware, protocol, and self-test gates pass. This avoids misleading the user with an enabled Generate button backed by an ineligible or unverified runtime.

## 2. Generator Adapter Contract

| Contract area | Required declaration or behavior |
|---|---|
| Identity | Stable adapter ID, localized display name, vendor/project, version, local or external. |
| Inputs | Minimum/maximum photo count, single-image or true multi-image conditioning, mask support, accepted formats/resolution. |
| Appearance | Geometry-only, PBR texture, vertex/material color, or no texture. |
| Compute | CPU/GPU/Auto support, supported GPU provider, required VRAM/RAM/disk, known low-memory modes. |
| Progress | Numeric stages, indeterminate operations, cancellation, remote polling, checkpoint/resume, Pause capability. |
| Output | File formats, coordinate/unit declaration, material resources, expected object inventory. |
| Privacy | Local processing or named remote service; exact data categories and metadata sent. |
| License | Software/model licenses, territory rule, acceptance state, distribution mode. |
| Errors | Stable categories for missing engine, license block, insufficient resource, input rejection, process/transport failure, malformed result, cancellation. |

The UI consumes this declaration rather than hard-coding Hunyuan behavior. A single-image adapter receives only the selected primary image. Supplementary images may inform a separate local reference-color report but never enter the adapter request or staging directory unless the declared capability explicitly supports them.

## 3. Engine Eligibility Pipeline

| Gate order | Gate | Failure result |
|---:|---|---|
| 1 | Adapter and manifest schema valid | Adapter remains unavailable; technical manifest error shown. |
| 2 | Product policy permits adapter | Adapter hidden or disabled with product-policy explanation. |
| 3 | License accepted and territory eligible | Blocked before image staging; offer approved alternative. |
| 4 | Package and model hashes valid | Quarantine/rollback package; never execute. |
| 5 | Protocol range compatible | Require compatible engine/application version. |
| 6 | Runtime/dependencies present | Show installation or repair action. |
| 7 | Hardware/resource preflight passes | Offer actual supported low-memory/device alternative or explain requirement. |
| 8 | Engine self-test passes | Preserve diagnostic result; no user image is sent. |
| 9 | Input request validates | Return field/image-specific corrections. |
| 10 | User confirms external transfer when applicable | No transfer if declined; return to adapter selection. |

The eligibility result is cached only with the relevant engine/application versions, hardware fingerprint subset, license hash, and territory policy version. Any material change invalidates the cached decision.

## 4. Hunyuan3D 2.1 Path

Hunyuan3D remains the preferred local adapter where the reviewed license permits it, but it cannot be the only Stage 2 plan. The community license excludes the European Union, United Kingdom, and South Korea.[1] The official repository documents a separate model stack, one-image usage examples, and substantial shape/texture VRAM requirements.[2]

| Area | Stage 2 plan |
|---|---|
| Packaging | Optional engine package, never part of the universal core bundle under the reviewed license. |
| Environment | Isolated worker environment; the Python 3.11 GUI never imports Hunyuan/PyTorch. |
| Input truth | One primary image for the single-image adapter path; no claim that all 1–6 photos condition the model. |
| Geometry versus texture | Expose separate capabilities/stages and resource preflights; permit geometry-only result if that is an accepted, tested configuration. |
| Territory | Evaluate before installation/execution. No image copied to engine staging if blocked. |
| Hardware | Detect GPU/provider/VRAM/RAM/disk; show documented and tested requirements, not inferred optimism. |
| Failure | Preserve stdout/stderr in a bounded redacted technical log, but surface a stable application error and corrective action. |
| Provenance | Store commit, model revisions, parameters, device mode, run ID, output hashes, and warnings. |

### Hunyuan Go/No-Go Criteria

Hunyuan is enabled for the Stage 2 demonstration only if all conditions pass: territory is eligible or separate rights are documented; the exact code and model assets have verified hashes/licenses; the engine installs reproducibly; the selected Windows GPU environment passes self-test; at least one real success and controlled failure pass; cancellation does not promote artifacts; and output reopens with plausible geometry.

If any condition fails, Stage 2 switches to an approved alternative adapter. The application architecture and fake Hunyuan contract tests remain, but a fake engine cannot satisfy the Stage 2 definition of done.

## 5. Alternative Local Generator Path

The alternative local engine is not preselected in this plan because model quality, commercial rights, Windows support, input semantics, and hardware requirements require evidence. The selection process uses the same contract and a scored gate.

| Criterion | Minimum condition |
|---|---|
| Rights | Commercial application use and intended distribution territory allowed for code and weights. |
| Windows operation | Reproducible installation or supported executable/API path on the target Windows hardware. |
| Isolation | Can run out of process and return a versioned result. |
| Input semantics | Truthfully declared single/multi-image behavior. |
| Output | Reopenable non-empty mesh, usable units/bounds, and optional texture resources. |
| Reliability | Controlled invalid input, resource failure, cancellation, and malformed output handled. |
| Privacy | Local operation has no required image upload or silent analytics. |
| Maintainability | Versioned releases/commits, documented dependencies, and a feasible update/rollback model. |

A candidate that is technically impressive but lacks clear weight rights or reproducible Windows support does not become the MVP engine.

## 6. External Generator Fallback

An external provider may satisfy the real-engine requirement only if the owner selects it and accepts its service terms, data handling, and costs. The application should prefer a small internal HTTP adapter to a large vendor SDK unless the SDK is necessary.

| Control | Required implementation |
|---|---|
| Configuration | Provider endpoint/domain and credential reference; no hard-coded key. |
| Secret storage | Windows Credential Manager/DPAPI preferred; optional user-local `.env` import with migration prompt. |
| Disclosure | Named provider, exact image count, purpose, metadata stripping, and remote cancellation limitation. |
| Consent | Matching explicit consent immediately before first transfer or after material provider/policy change. |
| Data minimization | Selected primary image and necessary parameters only for a single-image API. |
| Transport | HTTPS with normal certificate validation; no bypass option. |
| Cost/duplicate safety | Idempotency key or provider job ID where supported; retries cannot silently duplicate paid jobs. |
| Cancellation | Distinguish cancelling local polling from cancelling the remote job. |
| Result | Size/content/schema limits, safe archive extraction, independent mesh validation, and provenance. |

The local-only product must remain usable for project, image, mask, viewer, Blender, and export fixture workflows even if no external provider is configured.

## 7. Background-Removal Engine

Automatic background removal is a separate engine family. The adapter may use ONNX Runtime, but the exact model is selected only after license and quality approval. The rembg software's license does not grant rights to every model it can obtain; its documentation warns that the current default model requires separate commercial terms.[3]

| Lifecycle state | User-visible behavior |
|---|---|
| Not installed | Automatic removal unavailable; Manual Mask remains available; Settings explains required model. |
| Candidate unapproved | Developer-only benchmark; never offered as a production model. |
| Download available | Show model name, source, size, license, and install action. |
| Installed unverified | Verify hash and run synthetic self-test before enabling. |
| Ready | Display revision and CPU/GPU capability; run locally without network. |
| Failed/corrupt | Disable, preserve failure details, offer repair/reinstall, keep Manual Mask. |
| Superseded | Retain current validated version until the new version passes self-test; allow rollback. |

## 8. Blender Runtime Strategy

Blender is both an engine and a licensing boundary. It supports background command-line Python execution,[4] and published scripts using its Python API must remain GPL-compatible under Blender's official guidance.[5]

| Stage 2 decision | Behavior |
|---|---|
| Acquisition | Discover one supported separately installed Blender LTS first. |
| User experience | Blender is never opened manually; the application discovers/configures and launches it in background mode. |
| Version control | Accept a narrow tested version range and record the exact version on every run. |
| Script distribution | Separate source component with its own license/readme and protocol. |
| Invocation | Direct executable plus argument vector; request/result paths are generated and validated. |
| Mutation policy | Raw artifact immutable; each operation writes to a new staging artifact/checkpoint. |
| Success policy | Validate result JSON, run/stage identity, output existence, reopen, non-empty geometry, and metrics. |
| Failure policy | Preserve last checkpoint, show actual failing operation, recommend parameter/repair alternative. |

## 9. Engine Package Layout

```text
%LOCALAPPDATA%\MiniFigure3DStudio\engines\
├── background-person-mask\
│   └── <version>\
│       ├── manifest.json
│       ├── LICENSE.txt
│       ├── model.onnx
│       └── self_test.json
├── hunyuan3d-2.1\
│   └── <version>\
│       ├── manifest.json
│       ├── LICENSE.txt
│       ├── environment\
│       ├── models\
│       └── self_test.json
└── <alternative-generator>\
    └── <version>\
        ├── manifest.json
        ├── licenses\
        ├── runtime\
        ├── models\
        └── self_test.json
```

A discovered Blender installation is represented by a local validated registration record rather than copied into this directory during Stage 2.

## 10. Installation, Update, and Rollback

| Phase | Rule |
|---|---|
| Discover | Load a signed/embedded catalog or user-supplied package manifest; catalog does not auto-install. |
| Disclose | Show size, source, license, territories, hardware, and network need. |
| Stage | Download/copy into a temporary package directory with quota and resume support where applicable. |
| Verify | Validate expected size, hashes, schema, license files, safe paths, and signature if used. |
| Install | Atomically move to versioned engine location; do not replace last valid version. |
| Self-test | Run without user images; validate structured result. |
| Activate | Update registry only after self-test passes. |
| Roll back | Reactivate previous compatible version if new version fails. |
| Uninstall | Refuse while jobs use it; remove version and report locked/remaining files. |

Stage 2 may use a developer-assisted installation for the real engine, but the same manifest, hash, self-test, and activation rules must be exercised. Silent manual copying followed by an unrecorded success is not acceptable evidence.

## 11. Engine Protocol Files

Each run creates a private stage directory containing an immutable request, bounded events stream or event transport, terminal result, engine technical log, and expected artifact staging paths.

| File | Authority |
|---|---|
| `request.json` | Application-authored, schema-valid, includes run/stage/protocol IDs and relative artifact references. |
| `events.jsonl` or structured IPC | Worker-authored progress/log events; every event carries run/stage identity. |
| `result.json` | Worker-authored terminal status, outputs, metrics, warnings, error chain, and versions. |
| `engine.log` | Bounded/redacted local diagnostic output; never authoritative for success. |
| `artifacts/` | Staged outputs; promoted only after application validation. |

The result cannot reference an absolute path outside the stage directory or a previous run. Hash and provenance checks occur before project commit.

## 12. Resource and Device Policy

| Selection | Semantics |
|---|---|
| Automatic | Adapter chooses only among its verified modes using current preflight; choice is recorded. |
| CPU | Enabled only if the adapter has a tested CPU path. “Try anyway” is not shown for a GPU-only engine. |
| GPU | Enabled only when provider, driver/runtime, model, VRAM, and self-test pass. |
| Low memory | Exposed only if upstream/implementation supports it and Stage 2 has tested output and failure behavior. |
| Fallback | Explicit transition to another mode/adapter; never silently changes an external/local privacy boundary. |

A VRAM warning must distinguish documented minimums, tested minimums, current free memory, and uncertainty. The application does not promise that a nominally adequate GPU guarantees success.

## 13. Provenance and Reproducibility

Every generated artifact records adapter and engine versions, model revisions, request schema/protocol, parameters, primary image hash alias, mask revision, selected device, relevant hardware summary, timing, warnings, output hashes, and parent artifact lineage. Secrets, raw credentials, full personal paths, and image pixels are excluded.

Reprocessing after an engine/model change creates a new run. It never overwrites the prior result or implies byte-identical reproducibility where GPU/numeric nondeterminism exists.

## 14. Release-Safe Feature Flags

| Flag/state | Purpose |
|---|---|
| Adapter registered | Code exists, but UI need not expose it. |
| Development only | Available only in explicitly marked development configuration; cannot satisfy release gate. |
| Eligible | License/territory/product policy allows consideration. |
| Installed | Files are present and verified. |
| Self-tested | Engine passed current-version capability test. |
| Ready | All gates pass for current environment; UI may enable selection. |
| Disabled by policy | Product or territory policy blocks it with a stable reason. |
| Quarantined | Integrity/self-test failure blocks execution pending repair. |

The feature state is calculated, not stored as a single editable boolean.

## 15. Stage 2 Engine Decision Record Template

For each real engine/model, the implementation closeout records the selected version, why it was selected, alternatives rejected, license/source links, territory decision, hashes, install method, hardware tested, supported modes, known limits, self-test result, real success/failure/cancel evidence, data sent, fallback, update/rollback process, and owner approval.

## References

[1]: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE "Tencent Hunyuan 3D 2.1 Community License"
[2]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Tencent Hunyuan3D 2.1 Repository"
[3]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
[4]: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html "Blender Command-Line Arguments"
[5]: https://www.blender.org/about/license/ "Blender License"
