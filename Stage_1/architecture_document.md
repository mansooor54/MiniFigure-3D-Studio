# MiniFigure 3D Studio — Stage 1 Architecture Document

**Author:** Manus AI  
**Status:** Proposed for approval  
**Scope:** Architecture and planning only; no application code has been implemented in Stage 1.

## 1. Executive Architecture Decision

MiniFigure 3D Studio should be built as a **local-first modular desktop application with supervised external processing engines**. The PySide6 desktop process owns the user experience, project state, consent decisions, orchestration, and result presentation. Computationally heavy or failure-prone components—including Hunyuan3D, Blender, and COLMAP—run outside the GUI process behind typed adapters and versioned result protocols.

This design is preferable to a single Python process because the required engines use incompatible or independently evolving runtimes, consume large amounts of memory, invoke native libraries, and have different cancellation semantics. Hunyuan3D 2.1 documents a Python 3.10 and CUDA-tested stack while the desktop application must use Python 3.11; it also reports materially different VRAM requirements for shape and texture stages.[1] Blender and COLMAP already expose command-line execution suitable for a supervised process boundary.[2] [3]

> **Primary architecture principle:** The desktop shell may coordinate an engine, but it must not trust an engine's exit code, stdout text, or file creation alone as proof of success. Every stage must produce a validated, typed result and verified artifacts.

## 2. Scope and Quality Goals

The architecture covers two generation modes, shared image preparation, an integrated offline viewer, Blender-based repair and styling, printability analysis, texture and printable-color workflows, multi-format export, project deletion, bilingual operation, and recoverable long-running jobs. Stage 1 defines these boundaries without claiming that the algorithms or external engines already work on a target workstation.

| Quality attribute | Required architectural behavior | Verification direction |
|---|---|---|
| Responsiveness | No long-running or blocking engine call runs on the Qt GUI thread. | UI heartbeat tests while mocked and real subprocesses run. |
| Truthfulness | Failure, cancellation, unsupported operation, warnings, and success are distinct states. | Fault-injection tests for non-zero exits, malformed results, empty outputs, and validation failures. |
| Recoverability | Every expensive stage has a durable checkpoint and atomic artifact commit. | Kill processes at controlled points and reopen the project. |
| Privacy | Photos stay local by default; every external transfer has a named provider and consent record. | Network-deny tests, log scans, and consent-gate integration tests. |
| Extensibility | Generation, masking, validation, color, and export capabilities sit behind typed interfaces. | Contract tests run against in-process fakes and each supported adapter. |
| Offline operation | Core UI, viewer, translations, help, presets, and local processing use bundled local assets. | Run with network access denied. |
| Internationalization | English LTR and Arabic RTL use externalized strings and locale-safe units and paths. | Screenshot, keyboard, truncation, and Arabic-path tests. |
| Print integrity | A written file is not considered printable until independent checks pass. | Reopen every exported format and compare geometry, units, parts, and material assignments. |
| Maintainability | Domain policy is independent of PySide6 widgets, Blender APIs, and provider SDKs. | Unit-test domain services without Qt or external programs. |

## 3. System Context

The user interacts only with MiniFigure 3D Studio. The application may use a local image-processing stack, an optional local AI engine, Blender, COLMAP, Windows credential services, and explicitly selected external APIs. The integrated viewer is local HTML/JavaScript hosted in Qt WebEngine; it must not navigate to remote sites or fetch libraries from a content-delivery network.

| External boundary | Direction | Sensitive data involved | Default policy |
|---|---|---|---|
| Local image and project folders | Read/write | Source photos, masks, textures, generated likeness | User-selected or application-managed local storage only. |
| Hunyuan3D worker | Local IPC/process | One selected primary image; optional derived color references kept separate | Disabled until installed, licensed, and preflighted. |
| Blender | Local process and files | Generated mesh, textures, project/model name | Only sanitized job paths and structured parameters; no API keys. |
| COLMAP | Local process and files | Full Accurate Scan photo set and reconstruction database | Local only. |
| Qt WebEngine viewer | Local resource bridge | Preview geometry, materials, issue overlays | Local resources only; network blocked. |
| External generator API | HTTPS | User-approved source image and request parameters | Opt-in per operation with provider disclosure and preview of what is sent. |
| Windows Credential Manager or DPAPI | Local OS service | External API key | Preferred persistence path; no key in project data. |

Microsoft recommends Windows Credential Manager or DPAPI for locally persisted secrets and warns against hard-coding keys.[4] The design will still support the required local `.env` configuration path, but will describe it accurately as a protected plaintext compatibility mechanism rather than a cryptographic vault.

## 4. Process Topology

The system uses **one trusted desktop orchestrator and several untrusted-or-failure-prone workers**. “Untrusted” here means that the orchestrator validates all messages and artifacts from the process; it does not imply malicious upstream software.

| Process | Runtime | Responsibility | Failure containment |
|---|---|---|---|
| Desktop shell | Python 3.11 + PySide6 | Windows, navigation, project model, consent, orchestration, progress, logs, localization | Must remain responsive and preserve the last committed project state. |
| Image-analysis worker | Python 3.11 worker process or bounded thread pool | Decode, thumbnails, blur, exposure, duplicate metrics, masks, color samples | Corrupt images and native decoder faults cannot take down the UI. |
| Hunyuan adapter worker | Separate engine environment, initially aligned to upstream tested stack | Shape and optional texture generation | GPU out-of-memory or native crashes terminate only the job worker. |
| Blender background process | Blender's bundled Python runtime | Mesh backup, cleanup, style transforms, base, keychain, previews, validation support, exports | One process per job or controlled stage; project artifacts committed only after validation. |
| COLMAP process chain | Pinned COLMAP binary | Feature extraction, matching, sparse reconstruction, dense reconstruction, meshing | Each command is a checkpoint with native logs and output validation. |
| Qt WebEngine renderer | Qt-managed sandboxed process | Render local Three.js viewer | Viewer crash can be recreated without losing project state. |

Blender officially supports background mode, command-line Python scripts, and a non-zero Python exception exit code; it also documents that argument order affects execution.[2] The launcher will therefore use an argument vector, set an explicit exception code, and require a separate structured result envelope.

## 5. Logical Architecture

The desktop codebase follows a **ports-and-adapters architecture** inside a modular monolith. The application can be distributed as one desktop product while preserving clear replacement boundaries.

| Layer | Responsibilities | Must not depend on |
|---|---|---|
| Presentation | PySide6 views, view models/controllers, navigation, translated formatting, accessible status, dialog orchestration | Blender APIs, COLMAP implementation, Hunyuan internals, provider SDK details. |
| Application | Use cases, pipeline orchestration, project commands, consent checks, task scheduling, progress aggregation, retry and recovery | Concrete widgets and unversioned subprocess text. |
| Domain | Projects, images, views, styles, dimensions, print profiles, artifacts, validation findings, palette assignments, job state machine | PySide6, filesystems, network clients, subprocesses. |
| Ports | Generator, masker, quality analyzer, mesh processor, validator, exporter, viewer bridge, secret store, clock, filesystem, telemetry-disabled policy | Concrete third-party libraries. |
| Adapters | Hunyuan, external APIs, COLMAP, Blender CLI, rembg/ONNX candidate, lib3mf, Three.js bridge, local filesystem, Windows secrets | Direct UI manipulation. |
| Infrastructure | Process supervision, atomic storage, hashing, log redaction, engine manifests, updater/installer integration | Domain policy decisions. |

Dependency injection should occur at the application composition root. This permits fakes for every external engine, deterministic unit tests, and future addition of Tripo, Meshy, or another engine without modifying the workflow screens.

## 6. Core Domain Model

The project model must represent provenance and state, not only a final mesh. Each artifact records how it was created and which inputs and settings produced it.

| Domain type | Key fields | Invariant |
|---|---|---|
| `Project` | Project UUID, project name, model name, locale, created/updated timestamps, schema version | Names are display values; filesystem paths are generated safely and need not equal names. |
| `SourceImage` | Image UUID, original path reference, imported copy path, SHA-256, dimensions, EXIF orientation, assigned view, quality findings, consent scope | The original is never modified. |
| `ViewAssignment` | Front, Back, Left, Right, Front Left, Front Right, Accurate Scan bin, confidence, source | Estimated and user-confirmed assignments remain distinguishable. |
| `MaskRevision` | Source image, model revision, generated mask, edit strokes/checkpoints, resulting alpha artifact | Manual corrections are non-destructive and reproducible. |
| `GenerationRequest` | Mode, adapter ID/version, primary image, reference-image roles, style, seed if supported, device mode, consent | An adapter receives only capabilities it declares. |
| `PrintProfile` | Machine/slicer profile, height, wall thickness, polygon target, solid/hollow, drain holes, base, name, keychain, colors | Height remains within 40–250 mm; profile defaults are editable and versioned. |
| `MeshArtifact` | UUID, role, format, path, hash, dimensions, polygon count, coordinate/unit convention, parent artifact | Immutable after commit; modifications create a new artifact. |
| `SurfaceAppearance` | PBR materials, textures, color space, maps, UV data | Never treated as directly printable filament allocation. |
| `PrintablePalette` | 1/4/8/16 slots, material colors, part assignments, minimum part thresholds | Every printable part maps to a valid slot or is explicitly unassigned. |
| `ValidationReport` | Validator versions, findings, metrics, status, blocking flag, orientation and support recommendations | Status is derived from findings, never manually typed. |
| `PipelineRun` | Run UUID, stage records, engine manifests, settings hash, checkpoints, timestamps, final state | A run can reference only committed input artifacts. |
| `ConsentRecord` | Purpose, provider, data categories, endpoint region if known, timestamp, policy/license version, decision | Consent applies to one described transfer or an explicitly bounded remembered scope. |

## 7. Project Workspace and Persistence

A project is a normal local directory with a human-inspectable manifest and immutable artifact store. The application writes metadata using a temporary file, flushes it, and atomically replaces the prior manifest. A small append-only job journal records transitions needed for crash recovery. Source images are imported as copies by default; an advanced option may reference originals, but a project cannot promise portability in that mode.

| Directory | Content | Retention |
|---|---|---|
| `project.json` | Versioned project metadata and artifact references | Life of project. |
| `inputs/originals/` | Imported source images with generated safe filenames | Until user deletes originals or project. |
| `inputs/metadata/` | Sanitized metadata, quality results, view assignments | Life of project. |
| `masks/` | Generated masks, revisions, and manual edit data | Life of project or until source deletion policy removes it. |
| `runs/<run-id>/` | Stage result envelopes, settings snapshots, checkpoints | Configurable history; last successful run retained by default. |
| `artifacts/raw/` | Raw engine outputs and checksums | Retain until user removes intermediates. |
| `artifacts/processed/` | Blender backups, repaired meshes, previews, palettes | Life of project. |
| `reports/` | Printability and export-validation reports | Life of project. |
| `exports/` | User-approved final files | User-controlled. |
| `logs/` | Redacted application and engine log views | Bounded retention and size. |
| `.staging/` | Uncommitted stage outputs | Removed after success; recoverable or removable after interruption. |

The manifest never stores API keys. Engine manifests include version, executable path identity, code/model revision, binary hash where practical, capability flags, license identifier/hash, and device information needed to reproduce a run.

## 8. Versioned Worker Protocol

Every external stage receives a job directory and a **versioned request document**, then emits progress events and one terminal **result envelope**. Stdout and stderr remain diagnostic channels only.

| Protocol element | Required information |
|---|---|
| Request | Protocol version, run and stage IDs, project-relative inputs, expected outputs, parameters, locale-neutral numeric units, cancellation token location, and redaction policy. |
| Progress event | Stage ID, monotonic sequence number, completed and total work units when known, localized-message key, safe parameters, optional warning code. |
| Result envelope | Protocol version, status, engine version, start/end times, artifacts with hashes and metrics, warnings, structured error, and checkpoint identity. |
| Error | Stable error code, category, user-message key, technical summary, remediation keys, retryability, and causal chain without secrets. |

A result is accepted only when the protocol version is supported, the terminal state matches process completion, each required file exists, hashes match, formats reopen successfully, and semantic validators pass. Missing or malformed envelopes are reported as `INFRASTRUCTURE_INVALID_RESULT`, even when the process exits with code zero.

## 9. Pipeline Orchestration

The orchestration engine executes a directed acyclic graph of stages. A stage declares prerequisites, inputs, outputs, cancellation and pause capabilities, retry policy, resource class, and validation gates. Completed stages can be reused only when the settings hash, input artifact hashes, engine manifest, and stage implementation version match.

| Job state | Meaning | UI behavior |
|---|---|---|
| Draft | Configuration is incomplete. | Generation action disabled with explicit missing fields. |
| Queued | Valid job awaits resources. | Show queue position and allow cancel. |
| Preflighting | Executables, model/license, disk, device, paths, and permissions are checked. | Show specific checks, not an indeterminate generic spinner. |
| Running | A stage is executing. | Stream real progress and safe logs. |
| Pause requested | Cooperative checkpoint request sent. | Explain that the stage is reaching a safe checkpoint. |
| Paused | Engine confirmed resumable state. | Offer resume or cancel. |
| Cancel requested | Cancellation initiated. | Prevent new stages; wait for cooperative stop before process-tree termination. |
| Cancelled | No uncommitted outputs are considered valid. | Offer cleanup, retry from checkpoint, or return to settings. |
| Succeeded | Required outputs and validators passed. | Advance automatically or await user review. |
| Succeeded with warnings | Outputs are usable but non-blocking findings exist. | Display warnings before the next irreversible action. |
| Failed | Stage or validation failed. | Show understandable reason, corrective actions, retry, and expandable details. |
| Blocked | License, consent, missing dependency, or incompatible hardware prevents execution. | Link to the exact resolution step; do not offer false retry. |

Progress must be computed from engine-reported work when available. When an engine cannot expose numeric progress, the UI shows the named active operation and elapsed time as an indeterminate stage; it must not fabricate percentages. Overall progress weights come from measured historical stage durations only after enough local observations exist, and are labeled estimates.

## 10. Fast AI Mode

Fast AI Mode accepts one to six photographs. Image analysis ranks candidates using quality, subject coverage, pose/view suitability, mask confidence, and user-assigned view. The application proposes a primary front or 45-degree image but allows the user to confirm or override it. The selected adapter receives only the inputs it declares.

The official Hunyuan3D 2.1 example passes one image into shape generation and one image path into texture generation; it does not document the requested group of photographs as a direct multi-image conditioning API.[1] MiniFigure 3D Studio will therefore state: **“One selected image is sent to the local generator. Other photos are used by MiniFigure 3D Studio as visual references for color and review.”**

| Fast AI stage | Input | Output | Gate |
|---|---|---|---|
| Import and classify | 1–6 images | Imported images and assigned views | Valid decodes and accepted privacy reminder. |
| Quality analysis | Imported images | Blur, exposure, resolution, duplicate, coverage, and pose findings | At least one suitable primary candidate or explicit user override with warning. |
| Mask generation and correction | Primary plus optional references | Versioned foreground masks | User accepts mask; failures remain editable/retryable. |
| Reference analysis | Non-primary images | Skin/hair/clothing/accessory color samples with confidence | Presented as suggestions, never generator conditioning when unsupported. |
| Engine preflight | Settings and engine manifest | Capability report | Territory/license, installation, VRAM, disk, and device pass. |
| Shape generation | One primary prepared image | Raw untextured mesh | Non-empty geometry reopens and basic bounds are plausible. |
| Texture generation | Raw mesh and supported image input | PBR textured mesh | Optional when hardware/capabilities permit; texture files reopen. |
| Blender processing | Raw artifact and print/style settings | Backup, repaired model, base, previews | Structured pipeline result and validation pass. |
| Review and export | Processed artifact | Reports and selected exports | Format-specific reopen and semantic validation. |

Hunyuan3D reports approximately 10 GB VRAM for shape, 21 GB for texture, and 29 GB for shape plus texture in its documented configuration.[1] The application should present geometry-only, texture-after-geometry, and supported low-VRAM paths where available. “CPU mode” must not be advertised as a useful fallback until a Stage 2 benchmark proves it is supported and acceptably usable; otherwise the UI should explain that the selected engine requires a compatible GPU and offer a different adapter.

### Hunyuan3D License Gate

The reviewed Hunyuan3D 2.1 community license excludes the European Union, United Kingdom, and South Korea from its licensed territory and restricts use and distribution outside that territory.[5] Consequently, the engine cannot be bundled or enabled worldwide under that license. The architecture treats model installation as a separate signed package controlled by license eligibility, exact revision, acceptance record, and release-channel policy. A compliant alternative adapter is required for worldwide product claims.

## 11. Accurate Scan Mode

Accurate Scan Mode accepts 24–80 overlapping photographs and provides capture instructions before import. COLMAP's official documentation supports camera-pose recovery, sparse reconstruction, dense reconstruction, and meshing through graphical and command-line workflows.[3] The application will use explicit CLI stages so that each output can be checked and resumed.

| Accurate Scan stage | COLMAP or application operation | Required validated output |
|---|---|---|
| Capture readiness | Instructions, image count, resolution, blur, exposure, duplicate, and estimated angle coverage | Actionable preflight report. |
| Feature extraction | COLMAP feature extraction | Non-empty database with per-image features. |
| Matching | Strategy selected for photo order and count | Match statistics above configurable minimums. |
| Sparse mapping | Incremental or selected supported mapper | Registered cameras, poses, intrinsics, sparse points. |
| Coverage analysis | Application reads reconstructed camera centers | Actual angular and height coverage map with missing sectors. |
| Undistortion | COLMAP image undistortion | Valid undistorted workspace. |
| Dense stereo | PatchMatch stereo or supported CPU/GPU path | Depth/normal maps with completion metrics. |
| Stereo fusion | Dense point fusion | Non-empty dense point cloud with bounds and density metrics. |
| Meshing | Supported mesher | Reopenable mesh with non-zero faces. |
| Blender preparation | Cleanup, scale, base, previews, validation | Processed model and report. |

Before sparse reconstruction, missing angles are only **estimates** derived from user bins or a confidence-scored view estimator. After sparse reconstruction, the UI replaces them with **reconstructed camera coverage**. This distinction prevents the application from presenting guessed camera angles as measured facts.

If any stage fails, the application reports the actual failing command, categorized native reason, output completeness, and corrective steps. Examples include too few registered images, insufficient matches, weak texture, repeated patterns, subject motion, changing background, invalid camera model, unavailable GPU, disk exhaustion, or a terminated process. No placeholder mesh or inherited artifact may be promoted as the current run's result.

## 12. Image Quality and Background Masking

Quality checks produce independent findings rather than one opaque score. A hard block is reserved for inputs that cannot be decoded, fall below a configurable minimum, or cannot satisfy a required mode. Blur, exposure, partial-body coverage, duplicates, and uncertain view assignments are normally explainable warnings unless they make the selected stage impossible.

| Check | Proposed method | Output behavior |
|---|---|---|
| Decode and orientation | Pillow/OpenCV with EXIF orientation normalization | Preserve original; create normalized working copy. |
| Resolution | Pixel dimensions and subject bounding-box dimensions | Mode-specific minimum with exact measured values. |
| Blur | Multiple normalized focus metrics, including edge/gradient evidence | Confidence and threshold, not a universal binary truth. |
| Exposure | Luminance histogram, clipped shadow/highlight ratios, local contrast | Underexposed/overexposed warnings with preview. |
| Exact duplicate | Cryptographic file hash | Hard duplicate identity. |
| Near duplicate | Perceptual hash plus feature similarity | User-review group; do not auto-delete. |
| Full-body visibility | Optional pose/segmentation model plus border contact | Confidence-scored warning; allow override. |
| Angle coverage | User bins before reconstruction; reconstructed cameras afterward | Clearly label estimated versus measured coverage. |

Background removal sits behind a `BackgroundRemovalAdapter`. The software library and model weights are approved separately because rembg's own documentation warns that model weights have independent licenses and that its current default BRIA model requires commercial terms for commercial use.[6] Automatic first-use model downloads are prohibited; every model asset is installed through the engine manager with a license and checksum.

Manual correction uses brush add, erase, edge refine, pan, zoom, before/after, undo/redo, and mask revision history. Edits are stored as non-destructive strokes or checkpoints so that a new automatic model can be tried without losing user work.

## 13. Style and Print Settings Model

Styles are parameter presets plus optional Blender operations, not separate ad hoc pipelines. Each style declares compatible generator capabilities, geometric transforms, fragile-feature rules, default print settings, and validation thresholds. A custom style is a validated parameter set, not arbitrary executable code.

| Style | Core architectural rule |
|---|---|
| Realistic Full Body | Preserve proportions and facial region; conservative face-aware decimation. |
| Cartoon | Controlled simplification and proportion presets; preview before destructive processing. |
| Chibi Miniature | Adjustable head-to-body ratio, thicker hands/feet/accessories, simplified fragile details, and preferred dual-foot base contact. |
| Bobblehead | Oversized head plus printable neck/connector policy; physical spring hardware is deferred unless explicitly designed and validated. |
| Bust | Crop/close torso, add stable plinth, validate bottom plane. |
| Keychain | Add reinforced loop and user-set hole diameter with wall-thickness checks. |
| Bas-Relief | Project or derive depth against a backing plate with minimum relief and backing thickness. |
| Custom Style | Combine approved parameters and operations; no untrusted Python execution. |

Printer presets seed editable values rather than assert guaranteed compatibility. Every profile records a version, target process, default height, wall thickness, base, overhang/support assumptions, hollow/drain-hole policy, color slots, and export defaults. Creality K2 with CFS, Orca Slicer, Creality Print, Generic FDM, and Resin Printer profiles require real slicer/printer validation during implementation.

## 14. Blender Processing Architecture

The Blender pipeline operates on an immutable raw artifact and writes a new staged artifact. Every script is small, focused, callable by a pipeline runner, and independently testable inside a supported Blender version. Published Blender API scripts must follow a GPL-compatible distribution plan because Blender treats its Python API as an integral part of the GPL program.[7]

| Pipeline operation | Design safeguard | Verification metric |
|---|---|---|
| Import raw mesh | Explicit importer and unit convention | Object count, face count, bounds, material and texture inventory. |
| Backup | Save untouched raw copy and initial `.blend` | Hash and reopen test. |
| Remove artifacts | Connected-component analysis with relative volume/area thresholds and protected semantic parts | Removed components recorded; preview and undo artifact available. |
| Merge by distance | Scale-relative threshold bounded by a maximum | Vertex delta and geometry-change warning. |
| Correct normals | Recalculate outward and detect inconsistent islands | Remaining inverted/ambiguous faces. |
| Close holes / repair non-manifold | Bounded passes with before/after metrics | Boundary loops and non-manifold edge counts. |
| Voxel remesh when necessary | Conditional, face-region-aware resolution, backup preserved | Facial-region deviation and global surface-distance estimates. |
| Decimate | Target polygons with protected face vertex group or conservative local thresholds | Polygon target and deviation metrics. |
| Strengthen fragile features | Thickness analysis plus selected semantic/manual regions | Violations before/after; no automatic claim when semantics are uncertain. |
| Add base | Parametric circle/square and Boolean union with fallback strategy | Union success, single connected result where intended, base dimensions. |
| Add name/keychain | Printable text/loop parameters and minimum-feature checks | Geometry union, hole diameter, legibility and thickness warnings. |
| Remove internal/floating geometry | Multi-signal detection with reviewable list | Components and internal shells recorded. |
| Place and scale | Compute world bounds, translate minimum Z to zero, scale to millimeters and selected height | Final X/Y/Z dimensions, Z-min tolerance. |
| Preview renders | Fixed cameras and lighting for front/back/left/right | Four valid images tied to artifact hash. |

“Preserve the face” is enforced by policy and measurable checks, not a single modifier setting. The design retains the raw and pre-decimation meshes, creates or imports a facial protection region when reliable, uses localized simplification limits, computes surface deviation in the face region, and marks the output for review when the region is missing or deviation exceeds a threshold.

## 15. Printability Validation

Printability validation is a composition of independent validators. Each finding includes severity, geometry reference, measured value, threshold/profile source, explanation, suggested repair, and whether automatic repair exists. The viewer can select a finding and highlight the associated mesh region in red.

| Required report field | Proposed validation source |
|---|---|
| Watertight | Boundary-edge and volume checks, cross-checked by independent parser where practical. |
| Non-manifold edges | Topological edge incidence analysis. |
| Disconnected objects | Object and connected-component inventory with intended-part classification. |
| X/Y/Z dimensions | World-space bounds after unit normalization. |
| Polygon count | Triangle and source-face counts. |
| Minimum wall thickness | Sampled or ray-based thickness analysis with printer-profile threshold; known approximation disclosed. |
| Floating parts | Components not attached to intended body/base graph and not explicitly marked separate printable parts. |
| Internal geometry | Enclosed shell/intersection tests with uncertainty reported. |
| Difficult overhangs | Face-normal analysis against candidate build direction using profile angle. |
| Base touches build plate | Minimum Z and base-contact-area tolerance. |
| Export blocker | Derived from blocking findings, missing artifacts, or invalid target semantics. |
| Recommended orientation | Candidate orientation scoring by contact area, overhang, height, face visibility, and supports. |
| Support estimate | Qualitative none/low/medium/high plus measured unsupported area; not an exact slicer prediction. |

The overall states are derived as follows: **Ready to Print** means no blocking errors and no material warnings under the selected profile; **Ready with Warnings** means no blockers but one or more review findings; **Repair Required** means at least one blocking finding. Even “Ready to Print” means “passes MiniFigure 3D Studio's declared checks,” not a guarantee of printer outcome.

## 16. Texture and Printable Color Architecture

Texture appearance and printable color are separate domain paths from the first processed mesh onward. A `SurfaceAppearance` retains PBR textures and maps for GLB, OBJ/MTL, and BLEND. A `PrintablePalette` represents a limited number of filament slots and the mesh regions or separate parts assigned to them.

| Concern | Texture mode | Filament color mode |
|---|---|---|
| Representation | UVs, image textures, PBR maps, material parameters | 1/4/8/16 discrete palette slots and printable parts/regions. |
| Primary exports | GLB, OBJ/MTL/textures, BLEND | 3MF; STL only for a single-color merged result. |
| Small details | May remain in textures | Must meet minimum printable area/volume or be merged into a neighboring color. |
| Manual editing | Material and texture preview | Part list, visibility, slot color editor, merge/split/reassign controls. |
| Validation | Missing textures, UVs, map references, color space | Unassigned parts, tiny islands, duplicate materials, floating color components, slicer recognition. |

Color separation is explicitly semi-automatic. Candidate regions can be derived from texture clustering, material boundaries, semantic hints, and connected regions, but the user must be able to correct skin, hair, clothing, shoes, accessories, and base assignments. Very small color regions are merged according to a visible threshold rule or require user review; they are never silently emitted as floating printable fragments.

The 3MF specification includes a Materials and Properties Extension for full-color and multi-material definitions, and lib3mf provides read, write, conversion, and validation support.[8] [9] The export adapter should use lib3mf, reopen the result, enumerate build items, validate units and assignments, and then run compatibility fixtures against supported Orca Slicer and Creality Print releases.

## 17. Integrated 3D Viewer

The viewer is a local Three.js application bundled with the desktop product and hosted in Qt WebEngine. Three.js is MIT-licensed, while Qt WebEngine incorporates Chromium and requires its own extensive license and notice handling.[10] [11] The viewer receives a read-only model descriptor and communicates through a narrow, schema-validated Qt WebChannel API.

| Viewer function | Design behavior |
|---|---|
| Rotate, zoom, pan | Orbit controls with keyboard and mouse help; controls remain spatially consistent in RTL. |
| Wireframe/material/color | Explicit display modes with preserved camera. |
| Separate parts | Visibility tree grouped by semantic part and printable slot. |
| Problem highlighting | Validation findings map to object IDs or face/vertex index ranges and display in red overlay. |
| Before/after | Synchronized cameras with split or toggle comparison. |
| Orthographic views | Front, back, left, right buttons using model coordinate convention. |
| Screenshot export | User-selected local path, current mode, optional transparent background and issue legend. |

Runtime networking is denied. Remote navigation, popups, arbitrary downloads, untrusted HTML insertion, and unrestricted local-file browsing are disabled. A restrictive content-security policy permits only bundled scripts/styles and project-local model blobs made available through the controlled bridge.

## 18. Export Architecture

Export is a transactional pipeline: create in staging, reopen with an independent parser or the originating library, validate semantic contents, write an export report, and atomically move the verified file set into the destination. If the destination is not writable or validation fails, the staging result remains clearly marked invalid and is not reported as success.

| Format | Required semantics | Post-write validation |
|---|---|---|
| STL | Single-color triangle mesh, intended units recorded in report, no texture claim | Reopen, non-zero triangles, dimensions, manifold policy, object count expectation. |
| GLB | Geometry, PBR materials/textures where supported, scene graph | Reopen independently, enumerate meshes/materials/images, verify buffers and dimensions. |
| OBJ/MTL | Geometry plus relative MTL and texture references | Reopen all files, verify references exist, package safely without absolute paths. |
| BLEND | Editable source with named collections, units, materials, preserved backup where configured | Open in supported Blender background process and inventory expected objects. |
| 3MF | Correct units, build items, parts/components, material/slot assignments | lib3mf read/validate, semantic checks, then slicer compatibility fixtures. |

The export report records source artifact hash, exporter and engine versions, dimensions, part count, material count, validation status, warnings, and file hashes. Successful file creation is only one step in this report.

## 19. Error and Recovery Model

Errors use stable categories and codes, while user-facing text is localized through message keys. The UI displays a one-sentence explanation, the affected stage, recommended next actions, and expandable technical details. Copying an error copies a redacted summary by default.

| Category | Example codes | Default recovery |
|---|---|---|
| Dependency | `BLENDER_NOT_FOUND`, `BLENDER_UNSUPPORTED`, `COLMAP_NOT_FOUND` | Open dependency settings and rescan. |
| Hardware | `GPU_NOT_FOUND`, `VRAM_INSUFFICIENT`, `CUDA_INCOMPATIBLE` | Change device/engine, use supported low-memory path, or stop. |
| Input | `IMAGE_LOW_RESOLUTION`, `IMAGE_BLURRY`, `FULL_BODY_NOT_VISIBLE`, `DUPLICATE_IMAGES` | Select/replace images or explicitly accept a warning where permitted. |
| Privacy/license | `EXTERNAL_CONSENT_REQUIRED`, `ENGINE_TERRITORY_BLOCKED`, `MODEL_LICENSE_NOT_ACCEPTED` | Complete disclosure/consent or choose another engine. |
| Engine | `AI_GENERATION_FAILED`, `COLMAP_SPARSE_FAILED`, `COLMAP_DENSE_FAILED`, `BLENDER_SCRIPT_FAILED` | Show actual cause, preserve checkpoint, retry only when safe. |
| Geometry | `BOOLEAN_FAILED`, `REPAIR_INCOMPLETE`, `NON_MANIFOLD_BLOCKER`, `BASE_NOT_CONNECTED` | Retry alternative repair, review issue overlay, or export blocked. |
| Export | `DESTINATION_NOT_WRITABLE`, `EXPORT_WRITE_FAILED`, `EXPORT_REOPEN_FAILED`, `THREEMF_ASSIGNMENT_INVALID` | Choose path or fix model; never leave a falsely successful empty file. |
| User action | `JOB_CANCELLED`, `PROJECT_DELETE_CANCELLED` | Return to last committed state. |
| Infrastructure | `RESULT_PROTOCOL_INVALID`, `CHECKPOINT_CORRUPT`, `DISK_FULL` | Preserve diagnostics and last valid artifacts; offer safe cleanup/retry. |

Logs are structured, bounded, and redacted. OWASP recommends excluding or sanitizing access tokens, keys, sensitive personal data, unconsented data, and sometimes file paths.[12] The normal log therefore uses project-relative IDs, stable event codes, engine versions, timings, and numeric metrics but excludes source images, thumbnails, masks, textures, API keys, authorization headers, environment dumps, and external response bodies.

## 20. Privacy, Consent, and Deletion

Photos and generated likenesses are classified as sensitive project data. The default workflow is fully local. External processing introduces a hard gate that names the service, describes which files and fields will be transmitted, identifies why they are needed, links to provider terms where available, and asks for explicit consent before network transfer.

| Privacy control | Required behavior |
|---|---|
| Permission reminder | New-project flow requires acknowledgment that the user has permission to process the photographed person. |
| Local default | External adapters are disabled until configured and selected. No analytics or image collection is enabled by default. |
| Data minimization | Send only the chosen image and necessary parameters; strip unneeded EXIF metadata before external upload. |
| Consent audit | Store provider, purpose, data categories, policy/adapter version, decision, and time without storing the secret. |
| External disclosure | Confirmation names the actual service and distinguishes local from remote stages. |
| Log redaction | Secrets and human images never enter logs. |
| Original deletion | User may remove imported originals after generation; the UI explains which derived masks/textures/previews remain likeness data. |
| Project deletion | Show categorized contents, request confirmation, stop active jobs, close viewer handles, delete managed files, and report failures. |
| Temporary cleanup | Clear known staging, engine temporary, and cache paths after commit/cancel according to retention settings. |

NIST defines media sanitization as rendering target data access infeasible for a chosen effort level and treats it as a media-aware program.[13] MiniFigure 3D Studio will not claim that overwriting and deleting individual files guarantees device sanitization on SSDs, snapshots, backups, or synced folders. “Enhanced Local Cleanup” is labeled best-effort; stronger assurance should rely on full-disk encryption, deletion of backups/sync copies, or device-level sanitization appropriate to the threat model.

## 21. Localization and Accessibility

All user-facing text—including error titles, remediation steps, printability findings, presets, and capture instructions—uses translation keys. English is LTR and Arabic is RTL. Layout direction mirrors navigation and aligned content, but 3D axes, rotation direction, numeric signs, file extensions, and technical identifiers retain their domain conventions.

Arabic file and folder names are mandatory automated cases across project creation, image import, Blender and COLMAP invocation, viewer URLs, export, and deletion. The process layer passes Unicode argument vectors rather than shell-escaped strings. Logs and JSON use UTF-8. Unit values are stored as locale-neutral numbers and formatted for display using the active locale.

Accessibility requires keyboard navigation, visible focus, text alternatives for icons, scalable text, non-color-only status cues, and screen-reader labels. Gold, red, and green statuses must also use icons and explicit text because color alone is insufficient.

## 22. Windows Packaging and Engine Management

The product should use a **small core installer plus optional engine packages**, not one enormous one-file executable. PyInstaller's official license exception permits commercial application bundles subject to dependency licenses.[14] The core installer contains the Python desktop runtime, PySide6/Qt modules, local viewer, translations, approved small libraries, documentation, and presets.

| Package | Proposed contents | Installation rule |
|---|---|---|
| Core application | EXE, Python runtime, Qt DLLs/plugins, Three.js viewer, translations, schemas, notices | Required; signed and built on native Windows CI. |
| Background model pack | Approved ONNX model, hash, license, model card | Optional or selected during setup; no silent download. |
| Hunyuan engine pack | Separate runtime, code/model revisions, native extensions, weights, notices | Territory/license-gated; not in universal installer. |
| Blender runtime pack | Tested Blender LTS and notices, if managed distribution is approved | Initially prefer discovering a supported installation; optional later. |
| COLMAP runtime pack | Pinned binary and complete third-party notices | Optional; installed for Accurate Scan Mode. |

Engine packages use signed manifests, checksums, resumable download, available disk preflight, post-install self-test, rollback, and explicit license display. The application can also discover user-installed Blender and COLMAP, but must validate version and capabilities before use.

Qt's official LGPL guidance requires notices, source or offer arrangements, and user replacement/relinking rights under the open-source path; Qt WebEngine also carries Chromium license obligations.[11] [15] The installer design must preserve these obligations or use properly acquired commercial terms.

## 23. Testing Architecture

Tests are divided by speed and external dependency. Domain and application tests run without Blender, COLMAP, GPU, or Qt widgets. Contract tests exercise adapters against deterministic fake executables. Integration tests use synthetic images and generated geometric fixtures. Clean-machine Windows tests cover real engines where licenses and hardware permit.

| Test level | Coverage |
|---|---|
| Unit | Image thresholds, dimension conversion, status derivation, project schema migration, adapter capability negotiation, log redaction. |
| Property-based | Millimeter scaling, bounds, safe filenames, Unicode paths, palette cardinality, state-machine transitions. |
| Contract | Generator request/result protocol, Blender result envelope, COLMAP stage parser, exporter interface, external-consent gate. |
| Fixture integration | Synthetic blur/exposure/duplicates, disconnected meshes, non-manifold fixtures, bases, keychain loops, color islands, corrupt exports. |
| Engine integration | Supported Blender LTS scripts, selected background model, Hunyuan where licensed/hardware permits, pinned COLMAP. |
| UI | Drag/drop, RTL/LTR, navigation guards, progress, cancellation, retries, error expansion/copy, mask editing. |
| Recovery | Forced termination at each stage, disk-full simulation, invalid checkpoint, app restart and resume. |
| Packaging | Windows 10/11 clean VM, no Python installed, offline startup, DLL/plugin discovery, installer upgrade/uninstall. |
| Interoperability | Reopen STL/GLB/OBJ/BLEND/3MF; import current 3MF fixtures in supported slicers and inspect part/material recognition. |

No real-person photographs will be committed. Test assets will be programmatically generated or properly licensed, with an asset manifest and proof of origin.

## 24. Architecture Acceptance Criteria

Stage 1 architecture is ready for approval when the product owner accepts the process isolation model, project workspace, adapter contracts, truthful job state machine, separate texture/filament domains, transactional export policy, Hunyuan territorial restriction handling, Qt/Blender license boundaries, privacy and deletion wording, and the staged implementation plan.

The following points remain deliberately unresolved until implementation spikes: exact supported Blender and COLMAP versions; the commercially acceptable background-removal model; a worldwide Hunyuan alternative; useful CPU behavior for local AI generation; facial-region preservation thresholds; 3MF behavior in specific slicer versions; and whether Blender/COLMAP are discovered or distributed as managed runtimes.

## References

[1]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 "Tencent Hunyuan3D 2.1 Repository"
[2]: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html "Blender Command-Line Arguments"
[3]: https://colmap.github.io/index.html "COLMAP — Structure-from-Motion and Multi-View Stereo"
[4]: https://learn.microsoft.com/en-us/windows/win32/secbp/handling-passwords "Microsoft: Handling Passwords"
[5]: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE "Tencent Hunyuan 3D 2.1 Community License"
[6]: https://github.com/danielgatis/rembg "rembg Repository and Model-License Warning"
[7]: https://www.blender.org/about/license/ "Blender License"
[8]: https://3mf.io/spec/ "3MF Specification Suite"
[9]: https://github.com/3MFConsortium/lib3mf "lib3mf Repository"
[10]: https://github.com/mrdoob/three.js "Three.js Repository"
[11]: https://doc.qt.io/qt-6/qtwebengine-licensing.html "Qt WebEngine Licensing"
[12]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html "OWASP Logging Cheat Sheet"
[13]: https://csrc.nist.gov/pubs/sp/800/88/r2/final "NIST SP 800-88 Rev. 2: Guidelines for Media Sanitization"
[14]: https://pyinstaller.org/en/stable/license.html "PyInstaller License"
[15]: https://www.qt.io/development/open-source-lgpl-obligations "Qt GPL and LGPL Obligations"
