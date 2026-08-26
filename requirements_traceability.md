# MiniFigure 3D Studio — Requirements Traceability Matrix

**Author:** Manus AI  
**Status:** Stage 1 planning traceability; no implementation tests are claimed.

## 1. Purpose

This matrix confirms that every major requirement group has an architectural owner, an implementation stage, and a future verification method. It does not treat a plan as evidence that the feature works.

## 2. Platform and Architecture

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Windows 10/11, Python 3.11, PySide6 | Core desktop shell and native Windows build | 2–3 | Clean Windows 10/11 VM startup, package manifest, UI smoke tests. |
| Blender background engine without manual opening | `blender_cli_adapter`, process supervisor, Blender scripts | 2 | Real background-process integration tests and result envelopes. |
| Modular future AI engines | Generator port, capability model, adapter registry | 2 | Contract tests with fake, local, and optional external adapters. |
| PyInstaller Windows EXE installer | `packaging/pyinstaller` and installer scripts | 3 | Signed installer build, install/upgrade/uninstall on clean VMs. |
| Arabic RTL and English LTR | Localization service, Qt translations, bidi helpers | 2 skeleton; 3 completion | RTL/LTR UI tests, screenshots, mixed-text and Arabic-path tests. |
| Offline operation except external API | Bundled viewer/assets and local adapters | 2 | Network-deny end-to-end test. |

## 3. Generation Modes

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Fast AI with 1–6 photos | `fast_ai_pipeline` | 2 | End-to-end run and invalid-input cases. |
| Hunyuan3D 2.1 default local engine | Separate Hunyuan worker plus license/territory gate | 2, subject to legal eligibility | Real engine test, manifest, license gate, VRAM error tests. |
| Best front/45-degree primary | `primary_image_selector` plus user confirmation | 2 | Deterministic ranking fixtures and UI override test. |
| Other photos used honestly as references | `reference_color_service`, capability-declared generator inputs | 2 | Adapter contract proves only primary image is sent when multi-image is unsupported. |
| Additional Tripo/Meshy adapters | Generator port and provider HTTP adapter | Deferred, after one working engine | Contract test and consent test per provider. |
| API keys from local `.env`, not hard-coded | dotenv source plus Windows secret store | 2 | Secret scan, configuration test, log/command-line scan. |
| External service disclosure and consent | Consent service and dialog | 2 for any external adapter | Network call impossible before matching consent. |
| CPU/GPU/Auto | Device capability service and adapter capabilities | 2 | Supported-mode matrix; unsupported selections disabled with explanation. |
| Insufficient VRAM fallback/error | Engine preflight and stable error codes | 2 | Fake and real capability tests. |
| Accurate Scan with 24–80 photos | `accurate_scan_pipeline` | 3 | End-to-end COLMAP fixture/reconstruction tests. |
| COLMAP cameras, sparse/dense points, mesh | Staged COLMAP CLI adapter | 3 | Output parsers and non-empty artifact validation. |
| Capture instructions | Mode-selection and capture-guide assets | 3 | Content review and UI test. |
| Blur/duplicate/exposure/resolution checks | Image quality service | 2 | Synthetic image tests. |
| Missing angles | Estimated bins, then reconstructed camera coverage | 3 | Coverage fixtures and labeling tests. |
| Actual reconstruction failure reason | Stage result/error mapping | 3 | Forced sparse/dense failures; no result promotion. |

## 4. User Interface and Asynchrony

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Navy/white/gold modern UI | Theme tokens and reusable widgets | 2 | UI review and contrast/accessibility tests. |
| Fifteen workflow steps | Navigation model and pages | 2–3 | Navigation tests and state screenshots. |
| Drag and drop | Image import page/drop zone | 2 | Qt drag/drop tests. |
| View assignments | View slots and source-image model | 2 | UI and persistence tests. |
| Mask correction | Mask canvas and revision store | 2 | Undo/redo/restart tests. |
| Progress per stage | Worker protocol and Activity Center | 2 | Fake and real process progress tests. |
| Cancel, Pause where supported, Retry | Task state machine and capability flags | 2 | Cancellation/process-tree tests; Pause hidden/disabled when unsupported. |
| Simplified log and expandable details | Structured logs, redactor, error panel | 2 | Seeded-secret scan and error UI tests. |
| UI never freezes | QProcess/worker boundaries | 2–3 | UI heartbeat tests around each adapter. |

## 5. Styles and Printing Settings

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Eight styles | Figure-style definitions and Blender operations | Base style in 2; full set in 3 | Fixture and visual review per style. |
| Chibi head/body ratio | Chibi parameter and Blender transform | 3 | Ratio calculation and output metric tests. |
| Preserve facial characteristics | Protected face region and deviation checks | 2–3 | Synthetic/approved model comparison and threshold reports. |
| Strengthen hands/feet/accessories | Fragile-feature operation | 3 | Thin-feature fixtures and before/after metrics. |
| Both feet on base | Base-contact rule and validator | 3 | Geometry fixture tests. |
| Height 40–250 mm, default 100 | Print profile and dimension service | 2 | Boundary/property tests. |
| Wall, polygons, hollow/solid, drain holes | Print settings and Blender operations | Basic in 2; full in 3 | Parameter validation and geometry fixtures. |
| Base, name, keychain | Parametric Blender operations | Base in 2; full in 3 | Base/name/loop fixtures and Boolean failure tests. |
| 1/4/8/16 filament colors | Printable palette | 3 | Cardinality and 3MF fixtures. |
| Five printer/slicer presets | Versioned YAML presets | 2 skeleton; 3 validated | Schema tests and slicer/printer review. |

## 6. Blender Pipeline

| Pipeline requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Import and backup | `scene_io`, artifact store | 2 | Reopen and hash test. |
| Remove small disconnected artifacts | Connected-component operation | 2 | Synthetic disconnected mesh fixtures. |
| Merge by Distance | Dedicated Blender operation | 2 | Vertex-count and tolerance tests. |
| Recalculate normals | Normals operation | 2 | Inverted-normal fixtures. |
| Detect/close holes and repair non-manifold | Hole and repair modules | 2 | Open-boundary and non-manifold fixtures. |
| Conditional voxel remesh | `voxel_remesh` with policy | 2–3 | Trigger/non-trigger fixtures and deviation metrics. |
| Face-preserving decimation | Decimate plus face protection | 2–3 | Face-region surface deviation test. |
| Strengthen fragile details | Localized thickening | 3 | Thin-feature fixtures. |
| Boolean union body/base | Boolean operation with fallback | 2 | Success/failure fixtures and preserved checkpoint. |
| Remove intersections/floating/internal geometry | Validators and operations | 2 basic; 3 advanced | Known-geometry fixtures. |
| Z=0, millimeters, selected height | Unit-scale and build-plate operations | 2 | Dimension and tolerance tests. |
| Four preview renders | Fixed-camera render script | 2 | Four image outputs tied to artifact hash. |

## 7. Printability Validation

| Required report field | Planned validator | Stage | Future evidence |
|---|---|---:|---|
| Watertight and non-manifold | Topology validator | 2 basic; 3 complete | Synthetic topology fixtures. |
| Disconnected objects | Component validator | 2 | Fixture counts. |
| X/Y/Z dimensions and polygons | Dimension/artifact validator | 2 | Known mesh metrics. |
| Wall violations | Wall-thickness validator | 3 | Thin-wall fixtures and profile thresholds. |
| Floating parts and internal geometry | Dedicated validators | 3 | Floating/enclosed fixtures. |
| Overhangs, orientation, supports | Overhang/orientation scoring | 3 | Known-angle fixtures and documented qualitative estimate. |
| Base touches plate | Build-plate validator | 2 | Z/contact fixtures. |
| Export blocker | Report status policy | 2 | Severity/status derivation tests. |
| Three result states | Validation report model | 2 | Unit tests for all severity combinations. |

## 8. Texture and Filament Color

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Preserve PBR for GLB/OBJ/BLEND | Surface appearance model and exporters | GLB in 2; rest in 3 | Reopen material/texture inventory. |
| Limited printable palette | Color separator and palette editor | 3 | 4/8/16 palette tests. |
| Skin/hair/clothes/shoes/accessories/base parts | Semantic part model plus manual correction | 3 | Part assignment fixtures and UI tests. |
| Prevent tiny floating colors | Minimum region rules | 3 | Tiny-island fixtures. |
| Manual color changes and merging | Palette editor | 3 | UI/persistence tests. |
| Valid 3MF for Orca/Creality | lib3mf exporter and compatibility suite | 3 | Write-read validation and actual slicer matrix. |

## 9. Viewer and Export

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Rotate/zoom/pan | Three.js controls | 2 | Viewer interaction tests. |
| Wireframe/material/color | View modes | 2 basic; 3 full color | UI tests. |
| Separate parts | Scene tree | 2 | Part visibility tests. |
| Red problem highlights | Issue overlay | 3 | Finding-to-geometry fixtures. |
| Before/after and four views | Comparison and camera controllers | 2 | Synchronized view tests. |
| Screenshot export | Viewer screenshot module | 2 | File and transparency tests. |
| No internet JS | Bundled viewer and request interceptor | 2 | Network-deny test. |
| STL/GLB | Transactional exporters | 2 | Independent reopen tests. |
| 3MF/OBJ/BLEND | Format adapters | 3 | Independent reopen and slicer tests. |
| Validate dimensions/manifold/objects before export | Export pipeline gates | 2–3 | Invalid fixture blocks finalization. |
| Written file is not proof | Reopen, semantic validation, atomic finalize | 2–3 | Empty/stale/malformed output tests. |

## 10. Privacy, Consent, Errors, and Deletion

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Local default | Adapter registry and network policy | 2 | Network-deny tests. |
| Explicit external consent and service name | Consent service/dialog | When external adapter exists | Consent-gate tests. |
| Delete originals/project and confirmation | Project/deletion services and dialogs | 2 | Inventory, locked-file, and cancel tests. |
| No analytics or image collection by default | No telemetry module; deny policy | 2 | Network audit. |
| No images or keys in logs | Redactor and content policy | 2 | Seeded-secret/image-marker scans. |
| Remove temp files on secure deletion choice | Managed cleanup with truthful best-effort label | 2 | Staging/cache deletion and remaining-item report. |
| Bilingual understandable errors | Stable codes and translation keys | 2 skeleton; 3 completion | Error catalog coverage and UI tests. |
| All listed missing-engine/input/pipeline/export errors | Error taxonomy and adapter mapping | 2–3 | Fault injection per code. |
| Never hide error or create empty success | Result protocol and artifact validator | 2 | Zero-exit/missing-output and empty-file tests. |

## 11. Engineering and Test Requirements

| Requirement | Planned component | Stage | Future evidence |
|---|---|---:|---|
| Type hints/dataclasses/interfaces/DI | Domain, ports, composition root | 2 | mypy and architecture tests. |
| Structured logging | Logging package | 2 | Schema and redaction tests. |
| Pytest and focused functions/files | Test hierarchy and code review standard | 2–3 | CI results and coverage report. |
| No `?:` ternary operator | Python implementation uses explicit `if`/`else`; language does not have C-style `?:` | 2–3 | Lint/review. |
| All specified automated tests | Unit, contract, integration, UI, E2E suites | 2–3 | Actual test reports; skipped tests listed. |
| No real-person repository photos | Fixture policy and manifest | 2–3 | Asset and binary scan. |
| Install/run instructions and modified-file list | Stage closeout template | 2–3 | Release/stage report. |
| Stop after each stage | Approval gate in roadmap | 1–3 | Explicit owner approval before next-stage branch/work. |

## 12. Stage 1 Deliverable Trace

| Required Stage 1 item | Delivered artifact |
|---|---|
| Architecture document | `architecture_document.md` |
| Data-flow diagram | `data_flow.png`, `data_flow.mmd`, and `diagrams.md` |
| User-interface design | `ui_ux_design.md`, `ui_workflow.png`, and source diagram |
| Dependency and license list | `dependency_license_register.md` |
| Security and privacy plan | `security_privacy_plan.md` |
| Implementation roadmap | `implementation_roadmap.md` |
| Proposed project structure | `proposed_project_structure.md` |
| Risks | `risk_register.md` |

## 13. Approval Interpretation

Approving Stage 1 authorizes implementation planning to become Stage 2 source work. It does not waive open license blockers, guarantee Hunyuan availability, approve a background model, or claim any runtime test. Those decisions remain explicit entry gates in the roadmap and risk register.
